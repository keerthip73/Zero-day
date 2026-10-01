package com.zeroguard.ai.service;

import com.zeroguard.ai.client.MlServiceClient;
import com.zeroguard.ai.dto.EventDtos.*;
import com.zeroguard.ai.dto.MlDtos.MlPredictionResponse;
import com.zeroguard.ai.entity.*;
import com.zeroguard.ai.repository.*;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class EventService {
    private final SecurityEventRepository eventRepository;
    private final DetectionRepository detectionRepository;
    private final AlertRepository alertRepository;
    private final AnalystNoteRepository noteRepository;
    private final UserRepository userRepository;
    private final MlServiceClient mlServiceClient;
    private final double alertRiskThreshold;

    public EventService(SecurityEventRepository eventRepository, DetectionRepository detectionRepository, AlertRepository alertRepository,
                        AnalystNoteRepository noteRepository, UserRepository userRepository, MlServiceClient mlServiceClient,
                        @Value("${zeroguard.alert-risk-threshold}") double alertRiskThreshold) {
        this.eventRepository = eventRepository;
        this.detectionRepository = detectionRepository;
        this.alertRepository = alertRepository;
        this.noteRepository = noteRepository;
        this.userRepository = userRepository;
        this.mlServiceClient = mlServiceClient;
        this.alertRiskThreshold = alertRiskThreshold;
    }

    @Transactional
    public EventResponse create(EventRequest request) {
        SecurityEvent event = eventRepository.save(EventMapper.toEntity(request));
        MlPredictionResponse prediction;
        try {
            prediction = mlServiceClient.predict(EventMapper.toMlRequest(event));
        } catch (Exception ex) {
            prediction = mlServiceClient.fallbackPrediction();
        }

        Detection detection = new Detection();
        detection.setEvent(event);
        detection.setModelName(prediction.modelName());
        detection.setModelVersion(prediction.modelVersion());
        detection.setAnomalyScore(prediction.anomalyScore());
        detection.setRiskScore(prediction.riskScore());
        detection.setSeverity(parseSeverity(prediction.severity()));
        detection.setAnomaly(prediction.anomaly());
        detection.setExplanation(String.join("\n", prediction.reasons() == null ? List.of() : prediction.reasons()));
        Detection savedDetection = detectionRepository.save(detection);

        if (savedDetection.getRiskScore() != null && savedDetection.getRiskScore() >= alertRiskThreshold) {
            Alert alert = new Alert();
            alert.setDetection(savedDetection);
            alert.setSeverity(savedDetection.getSeverity());
            alert.setTitle("High-risk network anomaly");
            alert.setDescription("Risk score " + savedDetection.getRiskScore() + " requires analyst review.");
            alertRepository.save(alert);
        }

        return EventMapper.toResponse(event, savedDetection);
    }

    public List<EventResponse> createBatch(BatchEventRequest request) {
        return request.events().stream().map(this::create).toList();
    }

    public Page<EventResponse> list(Pageable pageable) {
        return eventRepository.findAll(pageable).map(event -> EventMapper.toResponse(event, event.getDetection()));
    }

    public EventResponse get(UUID id) {
        SecurityEvent event = eventRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("Event not found"));
        return EventMapper.toResponse(event, event.getDetection());
    }

    public List<AlertResponse> alerts() {
        return alertRepository.findTop10ByOrderByCreatedAtDesc().stream().map(this::toAlertResponse).toList();
    }

    public DashboardSummary summary() {
        long total = eventRepository.count();
        long normal = detectionRepository.countBySeverity(Severity.NORMAL);
        long suspicious = detectionRepository.countBySeverity(Severity.SUSPICIOUS);
        long highRisk = detectionRepository.countBySeverity(Severity.HIGH_RISK);
        long critical = alertRepository.countByStatus(AlertStatus.OPEN);
        double average = detectionRepository.findAll().stream().map(Detection::getRiskScore).filter(java.util.Objects::nonNull).mapToDouble(Double::doubleValue).average().orElse(0.0);
        return new DashboardSummary(total, normal, suspicious, highRisk, critical, average);
    }

    @Transactional
    public AnalystNoteResponse addNote(UUID eventId, AnalystNoteRequest request, String email) {
        SecurityEvent event = eventRepository.findById(eventId).orElseThrow(() -> new IllegalArgumentException("Event not found"));
        User author = userRepository.findByEmail(email).orElseThrow();
        AnalystNote note = new AnalystNote();
        note.setEvent(event);
        note.setAuthor(author);
        note.setNote(request.note());
        AnalystNote saved = noteRepository.save(note);
        return new AnalystNoteResponse(saved.getId(), event.getId(), author.getEmail(), saved.getNote(), saved.getCreatedAt());
    }

    @Transactional
    public AlertResponse updateAlert(UUID alertId, AlertStatus status) {
        Alert alert = alertRepository.findById(alertId).orElseThrow(() -> new IllegalArgumentException("Alert not found"));
        alert.setStatus(status);
        if (status == AlertStatus.INVESTIGATING) {
            alert.setAcknowledgedAt(Instant.now());
        }
        if (status == AlertStatus.RESOLVED || status == AlertStatus.FALSE_POSITIVE) {
            alert.setResolvedAt(Instant.now());
        }
        return toAlertResponse(alert);
    }

    private AlertResponse toAlertResponse(Alert alert) {
        return new AlertResponse(alert.getId(), alert.getDetection().getEvent().getId(), alert.getSeverity(), alert.getStatus(), alert.getTitle(), alert.getDescription(), alert.getCreatedAt());
    }

    private Severity parseSeverity(String value) {
        try {
            return Severity.valueOf(value);
        } catch (Exception ex) {
            return Severity.SUSPICIOUS;
        }
    }
}

