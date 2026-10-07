package com.defectprediction.backend.metrics;

import java.util.List;

public class CouplingTest {

    public static void main(String[] args) throws Exception {

        ProjectScanner scanner = new ProjectScanner();

        List<String> javaFiles =
                scanner.findJavaFiles(".");

        CouplingCalculator calculator =
                new CouplingCalculator();

        String filePath =
                "src/main/java/com/defectprediction/backend/metrics/MetricExtractor.java";

        int coupling =
                calculator.calculateCoupling(
                        filePath,
                        javaFiles);

        System.out.println(
                "Coupling: " + coupling);
    }
}