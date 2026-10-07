package com.defectprediction.backend.metrics;

import java.util.List;

public class MetricExtractorTest {

    public static void main(String[] args) throws Exception {

        MetricExtractor extractor =
                new MetricExtractor();

        List<MetricResult> results =
                extractor.extractMetrics(".");

        System.out.println(
                "===== SOFTWARE METRICS =====");

        for (MetricResult result : results) {

            System.out.println(
                    "File: " + result.getFilePath());

            System.out.println(
                    "LOC: " + result.getLoc());

            System.out.println(
                    "Cyclomatic Complexity: "
                    + result.getCyclomaticComplexity());

            System.out.println(
                    "Coupling: "
                    + result.getCoupling());

            System.out.println(
                    "Cohesion: "
                    + result.getCohesion());

            System.out.println(
                    "Code Churn: "
                    + result.getCodeChurn());

            System.out.println(
                    "Inheritance Depth: "
                    + result.getInheritanceDepth());

            System.out.println(
                    "---------------------------");
        }

        System.out.println(
                "Total files analyzed: "
                + results.size());
    }
}