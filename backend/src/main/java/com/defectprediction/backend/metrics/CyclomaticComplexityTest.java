package com.defectprediction.backend.metrics;

public class CyclomaticComplexityTest {

    public static void main(String[] args) throws Exception {

        CyclomaticComplexityCalculator calculator =
                new CyclomaticComplexityCalculator();

        String filePath =
                "src/main/java/com/defectprediction/backend/metrics/LocCalculator.java";

        int complexity =
                calculator.calculateComplexity(filePath);

        System.out.println("Cyclomatic Complexity: " + complexity);
    }
}