package com.defectprediction.backend.metrics;

public class CohesionTest {

    public static void main(String[] args) throws Exception {

        CohesionCalculator calculator =
                new CohesionCalculator();

        String filePath =
                "src/main/java/com/defectprediction/backend/metrics/MetricResult.java";

        double cohesion =
                calculator.calculateCohesion(filePath);

        System.out.println(
                "Cohesion: " + cohesion);
    }
}