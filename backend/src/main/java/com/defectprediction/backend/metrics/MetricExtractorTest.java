package com.defectprediction.backend.metrics;

import java.util.List;

public class MetricExtractorTest {

    public static void main(String[] args)
            throws Exception {

        MetricExtractor extractor =
                new MetricExtractor();

        List<MetricResult> results =
                extractor.extractMetrics(".");

        System.out.println();
        System.out.println(
                "========================================");

        System.out.println(
                "     COMPLETE SOFTWARE METRICS");

        System.out.println(
                "========================================");

        for (MetricResult result : results) {

            System.out.println();

            System.out.println(
                    "File: "
                    + result.getFilePath());

            System.out.println(
                    "----------------------------------------");

            // Existing metrics

            System.out.println(
                    "LOC: "
                    + result.getLoc());

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

            // Bayesian Network metrics

            System.out.println();

            System.out.println(
                    "Essential Complexity: "
                    + result.getEssentialComplexity());

            System.out.println(
                    "Design Complexity: "
                    + result.getDesignComplexity());

            System.out.println(
                    "Halstead Volume: "
                    + result.getHalsteadVolume());

            System.out.println(
                    "Halstead Difficulty: "
                    + result.getHalsteadDifficulty());

            System.out.println(
                    "Halstead Effort: "
                    + result.getHalsteadEffort());

            System.out.println(
                    "Branch Count: "
                    + result.getBranchCount());

            System.out.println(
                    "========================================");
        }

        System.out.println();

        System.out.println(
                "Total files analyzed: "
                + results.size());
    }
}