package com.defectprediction.backend.metrics;

public class HalsteadMetricsTest {

    public static void main(String[] args)
            throws Exception {

        String filePath =
                "src/main/java/com/defectprediction/backend/metrics/Hello.java";

        HalsteadMetrics calculator =
                new HalsteadMetrics();

        double volume =
                calculator.calculateVolume(filePath);

        double difficulty =
                calculator.calculateDifficulty(filePath);

        double effort =
                calculator.calculateEffort(filePath);

        System.out.println(
                "===== HALSTEAD METRICS =====");

        System.out.println(
                "Halstead Volume: "
                + volume);

        System.out.println(
                "Halstead Difficulty: "
                + difficulty);

        System.out.println(
                "Halstead Effort: "
                + effort);
    }
}