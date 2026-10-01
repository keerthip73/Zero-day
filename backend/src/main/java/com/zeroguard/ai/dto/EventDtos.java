package com.zeroguard.ai.dto;

import com.zeroguard.ai.entity.AlertStatus;
import com.zeroguard.ai.entity.Severity;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

public class EventDtos {
    public record EventRequest(
            Instant timestamp,
            @NotBlank String sourceIdentifier,
            @NotBlank String destinationIdentifier,
            @NotBlank String protocol,
            @Min(0) @Max(65535) Integer sourcePort,
            @Min(0) @Max(65535) Integer destinationPort,
            @Min(0) Double durationMs,
            @Min(0) Double forwardPackets,
            @Min(0) Double backwardPackets,
            @Min(0) Double forwardBytes,
            @Min(0) Double backwardBytes,
            @Min(0) Double flowBytesPerSec,
            @Min(0) Double flowPacketsPerSec,
            @Min(0) Double packetLengthMean,
            @Min(0) Double packetLengthStd,
            @Min(0) Double flowIatMeanMs,
            @Min(0) Double tcpSynCount,
            @Min(0) Double tcpAckCount,
            @Min(0) Double tcpRstCount
    ) {}

    public record BatchEventRequest(@NotEmpty List<@Valid EventRequest> events) {}
    public record DetectionResponse(UUID id, String modelName, String modelVersion, Double anomalyScore, Double riskScore, Severity severity, Boolean anomaly, List<String> reasons, Instant createdAt) {}
    public record EventResponse(UUID id, Instant timestamp, String sourceIdentifier, String destinationIdentifier, String protocol, Integer sourcePort, Integer destinationPort, DetectionResponse detection) {}
    public record AlertResponse(UUID id, UUID eventId, Severity severity, AlertStatus status, String title, String description, Instant createdAt) {}
    public record DashboardSummary(long totalEvents, long normalEvents, long suspiciousEvents, long highRiskEvents, long criticalAlerts, double averageRiskScore) {}
    public record AnalystNoteRequest(@NotBlank @Size(max = 2000) String note) {}
    public record AnalystNoteResponse(UUID id, UUID eventId, String authorEmail, String note, Instant createdAt) {}
}
