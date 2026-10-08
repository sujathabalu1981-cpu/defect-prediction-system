package com.defectprediction.backend.ml;

import org.springframework.http.MediaType;
import org.springframework.web.client.RestClient;

public class BayesianPredictionClient {

    private final RestClient restClient;

    public BayesianPredictionClient() {

        restClient = RestClient.builder()
                .baseUrl("http://localhost:8000")
                .build();
    }

    public String predict(MetricFeature feature) {

        return restClient.post()
                .uri("/predict")
                .contentType(MediaType.APPLICATION_JSON)
                .body(feature)
                .retrieve()
                .body(String.class);
    }
}