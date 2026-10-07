package com.defectprediction.backend.metrics;

public class ProjectMetricsCalculatorTest {

    public static void main(String[] args) throws Exception {

        ProjectMetricsCalculator calculator =
                new ProjectMetricsCalculator();

        calculator.calculateProjectLOC(".");
    }
}