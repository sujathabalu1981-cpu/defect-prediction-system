package com.defectprediction.backend.ml;

import org.junit.jupiter.api.Test;

public class BayesianPredictionClientTest {

    @Test
    void testPredictionRequest() {

        MetricFeature feature =
                new MetricFeature(
                        31,
                        1,
                        1,
                        1,
                        66.6079,
                        5.8333,
                        388.5462,
                        0
                );

        BayesianPredictionClient client =
                new BayesianPredictionClient();

        String response =
                client.predict(feature);

        System.out.println();
        System.out.println(
                "========================================");

        System.out.println(
                "BAYESIAN NETWORK RESPONSE");

        System.out.println(
                "========================================");

        System.out.println(response);

        System.out.println(
                "========================================");
    }
}