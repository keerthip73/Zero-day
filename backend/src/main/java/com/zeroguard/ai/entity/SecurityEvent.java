package com.zeroguard.ai.entity;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "security_events", indexes = {
        @Index(name = "idx_events_timestamp", columnList = "event_timestamp"),
        @Index(name = "idx_events_protocol", columnList = "protocol")
})
public class SecurityEvent {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    private Instant eventTimestamp;
    private String sourceIdentifier;
    private String destinationIdentifier;
    private String protocol;
    private Integer sourcePort;
    private Integer destinationPort;
    private Double durationMs;
    private Double forwardPackets;
    private Double backwardPackets;
    private Double forwardBytes;
    private Double backwardBytes;
    private Double flowBytesPerSec;
    private Double flowPacketsPerSec;
    private Double packetLengthMean;
    private Double packetLengthStd;
    private Double flowIatMeanMs;
    private Double tcpSynCount;
    private Double tcpAckCount;
    private Double tcpRstCount;

    @Column(nullable = false)
    private Instant createdAt = Instant.now();

    @OneToOne(mappedBy = "event", cascade = CascadeType.ALL)
    private Detection detection;

    public UUID getId() { return id; }
    public Instant getEventTimestamp() { return eventTimestamp; }
    public void setEventTimestamp(Instant eventTimestamp) { this.eventTimestamp = eventTimestamp; }
    public String getSourceIdentifier() { return sourceIdentifier; }
    public void setSourceIdentifier(String sourceIdentifier) { this.sourceIdentifier = sourceIdentifier; }
    public String getDestinationIdentifier() { return destinationIdentifier; }
    public void setDestinationIdentifier(String destinationIdentifier) { this.destinationIdentifier = destinationIdentifier; }
    public String getProtocol() { return protocol; }
    public void setProtocol(String protocol) { this.protocol = protocol; }
    public Integer getSourcePort() { return sourcePort; }
    public void setSourcePort(Integer sourcePort) { this.sourcePort = sourcePort; }
    public Integer getDestinationPort() { return destinationPort; }
    public void setDestinationPort(Integer destinationPort) { this.destinationPort = destinationPort; }
    public Double getDurationMs() { return durationMs; }
    public void setDurationMs(Double durationMs) { this.durationMs = durationMs; }
    public Double getForwardPackets() { return forwardPackets; }
    public void setForwardPackets(Double forwardPackets) { this.forwardPackets = forwardPackets; }
    public Double getBackwardPackets() { return backwardPackets; }
    public void setBackwardPackets(Double backwardPackets) { this.backwardPackets = backwardPackets; }
    public Double getForwardBytes() { return forwardBytes; }
    public void setForwardBytes(Double forwardBytes) { this.forwardBytes = forwardBytes; }
    public Double getBackwardBytes() { return backwardBytes; }
    public void setBackwardBytes(Double backwardBytes) { this.backwardBytes = backwardBytes; }
    public Double getFlowBytesPerSec() { return flowBytesPerSec; }
    public void setFlowBytesPerSec(Double flowBytesPerSec) { this.flowBytesPerSec = flowBytesPerSec; }
    public Double getFlowPacketsPerSec() { return flowPacketsPerSec; }
    public void setFlowPacketsPerSec(Double flowPacketsPerSec) { this.flowPacketsPerSec = flowPacketsPerSec; }
    public Double getPacketLengthMean() { return packetLengthMean; }
    public void setPacketLengthMean(Double packetLengthMean) { this.packetLengthMean = packetLengthMean; }
    public Double getPacketLengthStd() { return packetLengthStd; }
    public void setPacketLengthStd(Double packetLengthStd) { this.packetLengthStd = packetLengthStd; }
    public Double getFlowIatMeanMs() { return flowIatMeanMs; }
    public void setFlowIatMeanMs(Double flowIatMeanMs) { this.flowIatMeanMs = flowIatMeanMs; }
    public Double getTcpSynCount() { return tcpSynCount; }
    public void setTcpSynCount(Double tcpSynCount) { this.tcpSynCount = tcpSynCount; }
    public Double getTcpAckCount() { return tcpAckCount; }
    public void setTcpAckCount(Double tcpAckCount) { this.tcpAckCount = tcpAckCount; }
    public Double getTcpRstCount() { return tcpRstCount; }
    public void setTcpRstCount(Double tcpRstCount) { this.tcpRstCount = tcpRstCount; }
    public Instant getCreatedAt() { return createdAt; }
    public Detection getDetection() { return detection; }
}
