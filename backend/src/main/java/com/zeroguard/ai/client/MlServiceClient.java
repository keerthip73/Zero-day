package com.zeroguard.ai.client;

import com.zeroguard.ai.dto.MlDtos.MlPredictionRequest;
import com.zeroguard.ai.dto.MlDtos.MlPredictionResponse;
import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class MlServiceClient {
    private final RestClient restClient;

    public MlServiceClient(@Value("${zeroguard.ml-service-url}") String mlServiceUrl) {
        this.restClient = RestClient.builder().baseUrl(mlServiceUrl).build();
    }

    public MlPredictionResponse predict(MlPredictionRequest request) {
        return restClient.post()
                .uri("/predict")
                .body(request)
                .retrieve()
                .body(MlPredictionResponse.class);
    }

    public MlPredictionResponse fallbackPrediction() {
        return new MlPredictionResponse(
                true,
                45.0,
                "SUSPICIOUS",
                "ML service unavailable fallback",
                "fallback",
                0.25,
                List.of("ML service unavailable; event stored for analyst review"),
                0.0
        );
    }
}

