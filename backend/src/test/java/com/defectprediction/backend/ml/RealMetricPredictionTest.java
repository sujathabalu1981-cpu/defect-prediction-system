package com.defectprediction.backend.ml;

import java.util.List;

import org.junit.jupiter.api.Test;

import com.defectprediction.backend.metrics.MetricExtractor;
import com.defectprediction.backend.metrics.MetricResult;

public class RealMetricPredictionTest {

    @Test
    void testRealMetricPrediction()
            throws Exception {

        // --------------------------------------
        // 1. Extract real metrics from project
        // --------------------------------------

        MetricExtractor extractor =
                new MetricExtractor();

        List<MetricResult> results =
                extractor.extractMetrics(".");

        System.out.println();
        System.out.println(
                "========================================"
        );

        System.out.println(
                "REAL METRIC → BAYESIAN PREDICTION"
        );

        System.out.println(
                "========================================"
        );


        // --------------------------------------
        // 2. Check whether files were found
        // --------------------------------------

        if (results.isEmpty()) {

            System.out.println(
                    "No Java files found."
            );

            return;
        }


        // --------------------------------------
        // 3. Take the first real Java file
        // --------------------------------------

        MetricResult result =
                results.get(0);


        System.out.println();
        System.out.println(
                "File: "
                + result.getFilePath()
        );


        // --------------------------------------
        // 4. Convert MetricResult
        //    into MetricFeature
        // --------------------------------------

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


        // --------------------------------------
        // 5. Send real metrics to
        //    Bayesian Network API
        // --------------------------------------

        BayesianPredictionClient client =
                new BayesianPredictionClient();

        String response =
                client.predict(feature);


        // --------------------------------------
        // 6. Display result
        // --------------------------------------

        System.out.println();

        System.out.println(
                "Real Metrics:"
        );

        System.out.println(
                "LOC: "
                + feature.getLOC()
        );

        System.out.println(
                "Cyclomatic: "
                + feature.getCyclomatic()
        );

        System.out.println(
                "Essential: "
                + feature.getEssential()
        );

        System.out.println(
                "Design: "
                + feature.getDesign()
        );

        System.out.println(
                "Halstead Volume: "
                + feature.getHalsteadVolume()
        );

        System.out.println(
                "Halstead Difficulty: "
                + feature.getHalsteadDifficulty()
        );

        System.out.println(
                "Halstead Effort: "
                + feature.getHalsteadEffort()
        );

        System.out.println(
                "Branch Count: "
                + feature.getBranchCount()
        );


        System.out.println();

        System.out.println(
                "========================================"
        );

        System.out.println(
                "BAYESIAN PREDICTION"
        );

        System.out.println(
                "========================================"
        );

        System.out.println(response);

        System.out.println(
                "========================================"
        );
    }
}