package com.zeroguard.ai.dto;

import java.time.Instant;
import java.util.List;

public class MlDtos {
    public record MlPredictionRequest(
            String event_id,
            Instant timestamp,
            String source_identifier,
            String destination_identifier,
            String protocol,
            Integer source_port,
            Integer destination_port,
            Double duration_ms,
            Double forward_packets,
            Double backward_packets,
            Double forward_bytes,
            Double backward_bytes,
            Double flow_bytes_per_sec,
            Double flow_packets_per_sec,
            Double packet_length_mean,
            Double packet_length_std,
            Double flow_iat_mean_ms,
            Double tcp_syn_count,
            Double tcp_ack_count,
            Double tcp_rst_count
    ) {}

    public record MlPredictionResponse(
            Boolean anomaly,
            Double riskScore,
            String severity,
            String modelName,
            String modelVersion,
            Double confidence,
            List<String> reasons,
            Double anomalyScore
    ) {}
}

