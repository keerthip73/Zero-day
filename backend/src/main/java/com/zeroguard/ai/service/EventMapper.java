package com.zeroguard.ai.service;

import com.zeroguard.ai.dto.EventDtos.DetectionResponse;
import com.zeroguard.ai.dto.EventDtos.EventRequest;
import com.zeroguard.ai.dto.EventDtos.EventResponse;
import com.zeroguard.ai.dto.MlDtos.MlPredictionRequest;
import com.zeroguard.ai.entity.Detection;
import com.zeroguard.ai.entity.SecurityEvent;
import java.time.Instant;
import java.util.Arrays;

public final class EventMapper {
    private EventMapper() {}

    public static SecurityEvent toEntity(EventRequest request) {
        SecurityEvent event = new SecurityEvent();
        event.setEventTimestamp(request.timestamp() == null ? Instant.now() : request.timestamp());
        event.setSourceIdentifier(request.sourceIdentifier());
        event.setDestinationIdentifier(request.destinationIdentifier());
        event.setProtocol(request.protocol().toUpperCase());
        event.setSourcePort(request.sourcePort());
        event.setDestinationPort(request.destinationPort());
        event.setDurationMs(request.durationMs());
        event.setForwardPackets(request.forwardPackets());
        event.setBackwardPackets(request.backwardPackets());
        event.setForwardBytes(request.forwardBytes());
        event.setBackwardBytes(request.backwardBytes());
        event.setFlowBytesPerSec(request.flowBytesPerSec());
        event.setFlowPacketsPerSec(request.flowPacketsPerSec());
        event.setPacketLengthMean(request.packetLengthMean());
        event.setPacketLengthStd(request.packetLengthStd());
        event.setFlowIatMeanMs(request.flowIatMeanMs());
        event.setTcpSynCount(request.tcpSynCount());
        event.setTcpAckCount(request.tcpAckCount());
        event.setTcpRstCount(request.tcpRstCount());
        return event;
    }

    public static MlPredictionRequest toMlRequest(SecurityEvent event) {
        return new MlPredictionRequest(
                event.getId() == null ? null : event.getId().toString(),
                event.getEventTimestamp(),
                event.getSourceIdentifier(),
                event.getDestinationIdentifier(),
                event.getProtocol(),
                event.getSourcePort(),
                event.getDestinationPort(),
                event.getDurationMs(),
                event.getForwardPackets(),
                event.getBackwardPackets(),
                event.getForwardBytes(),
                event.getBackwardBytes(),
                event.getFlowBytesPerSec(),
                event.getFlowPacketsPerSec(),
                event.getPacketLengthMean(),
                event.getPacketLengthStd(),
                event.getFlowIatMeanMs(),
                event.getTcpSynCount(),
                event.getTcpAckCount(),
                event.getTcpRstCount()
        );
    }

    public static EventResponse toResponse(SecurityEvent event, Detection detection) {
        DetectionResponse detectionResponse = null;
        if (detection != null) {
            String[] reasons = detection.getExplanation() == null
                    ? new String[0]
                    : detection.getExplanation().split("\\n");
            detectionResponse = new DetectionResponse(
                    detection.getId(),
                    detection.getModelName(),
                    detection.getModelVersion(),
                    detection.getAnomalyScore(),
                    detection.getRiskScore(),
                    detection.getSeverity(),
                    detection.getAnomaly(),
                    Arrays.stream(reasons).filter(s -> !s.isBlank()).toList(),
                    detection.getCreatedAt()
            );
        }
        return new EventResponse(
                event.getId(),
                event.getEventTimestamp(),
                event.getSourceIdentifier(),
                event.getDestinationIdentifier(),
                event.getProtocol(),
                event.getSourcePort(),
                event.getDestinationPort(),
                detectionResponse
        );
    }
}
