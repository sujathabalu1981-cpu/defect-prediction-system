package com.defectprediction.backend.ml;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertFalse;
import org.junit.jupiter.api.Test;

import com.defectprediction.backend.metrics.MetricExtractor;
import com.defectprediction.backend.metrics.MetricResult;

public class MetricFeatureTest {

    @Test
    void testMetricFeatureConversion()
            throws Exception {

        MetricExtractor extractor =
                new MetricExtractor();

        List<MetricResult> results =
                extractor.extractMetrics(".");

        assertFalse(
                results.isEmpty(),
                "No files were analyzed"
        );

        for (MetricResult result : results) {

            MetricFeature feature =
                    new MetricFeature(
                            result.getLoc(),
                            result.getCyclomaticComplexity(),
                            result.getEssentialComplexity(),
                            result.getDesignComplexity(),
                            result.getHalsteadVolume(),
                            result.getHalsteadDifficulty(),
                            result.getHalsteadEffort(),
                            result.getBranchCount()
                    );

            System.out.println();
            System.out.println(
                    "File: " + result.getFilePath());

            System.out.println(
                    "LOC: " + feature.getLOC());

            System.out.println(
                    "Cyclomatic: "
                    + feature.getCyclomatic());

            System.out.println(
                    "Essential: "
                    + feature.getEssential());

            System.out.println(
                    "Design: "
                    + feature.getDesign());

            System.out.println(
                    "Halstead Volume: "
                    + feature.getHalsteadVolume());

            System.out.println(
                    "Halstead Difficulty: "
                    + feature.getHalsteadDifficulty());

            System.out.println(
                    "Halstead Effort: "
                    + feature.getHalsteadEffort());

            System.out.println(
                    "Branch Count: "
                    + feature.getBranchCount());
        }

        System.out.println();
        System.out.println(
                "MetricFeature conversion successful."
        );
    }
}