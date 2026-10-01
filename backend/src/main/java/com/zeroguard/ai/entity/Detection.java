package com.zeroguard.ai.entity;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "detections", indexes = @Index(name = "idx_detections_risk", columnList = "risk_score"))
public class Detection {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @OneToOne(optional = false)
    @JoinColumn(name = "event_id")
    private SecurityEvent event;

    private String modelName;
    private String modelVersion;
    private Double anomalyScore;
    private Double riskScore;

    @Enumerated(EnumType.STRING)
    private Severity severity;

    private Boolean anomaly;

    @Column(length = 2000)
    private String explanation;

    @Column(nullable = false)
    private Instant createdAt = Instant.now();

    public UUID getId() { return id; }
    public SecurityEvent getEvent() { return event; }
    public void setEvent(SecurityEvent event) { this.event = event; }
    public String getModelName() { return modelName; }
    public void setModelName(String modelName) { this.modelName = modelName; }
    public String getModelVersion() { return modelVersion; }
    public void setModelVersion(String modelVersion) { this.modelVersion = modelVersion; }
    public Double getAnomalyScore() { return anomalyScore; }
    public void setAnomalyScore(Double anomalyScore) { this.anomalyScore = anomalyScore; }
    public Double getRiskScore() { return riskScore; }
    public void setRiskScore(Double riskScore) { this.riskScore = riskScore; }
    public Severity getSeverity() { return severity; }
    public void setSeverity(Severity severity) { this.severity = severity; }
    public Boolean getAnomaly() { return anomaly; }
    public void setAnomaly(Boolean anomaly) { this.anomaly = anomaly; }
    public String getExplanation() { return explanation; }
    public void setExplanation(String explanation) { this.explanation = explanation; }
    public Instant getCreatedAt() { return createdAt; }
}
