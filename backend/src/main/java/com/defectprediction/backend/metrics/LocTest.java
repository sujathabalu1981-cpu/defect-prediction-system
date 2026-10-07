package com.defectprediction.backend.metrics;

public class LocTest {

    public static void main(String[] args) throws Exception {

        LocCalculator calculator = new LocCalculator();

        String filePath = "src/main/java/com/defectprediction/backend/metrics/LocCalculator.java";

        int loc = calculator.calculateLOC(filePath);

        System.out.println("Lines of Code: " + loc);
    }
}