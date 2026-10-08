package com.defectprediction.backend;

import java.util.ArrayList;
import java.util.List;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.defectprediction.backend.github.GitRepositoryService;
import com.defectprediction.backend.metrics.MetricExtractor;
import com.defectprediction.backend.metrics.MetricResult;
import com.defectprediction.backend.ml.BayesianPredictionClient;
import com.defectprediction.backend.ml.MetricFeature;

@RestController
public class AnalysisController {

    @PostMapping("/analyze")
    public AnalysisResponse analyze(
            @RequestBody AnalysisRequest request)
            throws Exception {

        System.out.println();
        System.out.println("========================================");
        System.out.println("STARTING SOFTWARE DEFECT ANALYSIS");
        System.out.println("========================================");

        System.out.println(
                "Repository: " + request.getRepository());

        System.out.println(
                "Commit: " + request.getCommitId());

        GitRepositoryService gitService =
                new GitRepositoryService();

        String repositoryPath =
                gitService.cloneRepository(
                        request.getRepository(),
                        request.getCommitId()
                );

        System.out.println(
                "Repository cloned to: "
                + repositoryPath);

        MetricExtractor extractor =
                new MetricExtractor();

        List<MetricResult> metricResults =
                extractor.extractMetrics(repositoryPath);

        System.out.println(
                "Files analyzed: "
                + metricResults.size());

        BayesianPredictionClient client =
                new BayesianPredictionClient();

        List<String> predictions =
                new ArrayList<>();

        int highRiskFiles = 0;
        int mediumRiskFiles = 0;
        int lowRiskFiles = 0;

        for (MetricResult result : metricResults) {

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

            String prediction =
                    client.predict(feature);

            predictions.add(
                    "File: "
                    + result.getFilePath()
                    + "\n"
                    + prediction
            );

            /*
             * Determine risk level from
             * the Bayesian prediction.
             */
            if (prediction.contains("\"risk_level\":\"HIGH\"")) {

                highRiskFiles++;

            } else if (prediction.contains("\"risk_level\":\"MEDIUM\"")) {

                mediumRiskFiles++;

            } else {

                lowRiskFiles++;
            }
        }

        /*
         * Overall pipeline decision.
         *
         * HIGH risk file → BLOCK
         * MEDIUM risk only → WARN
         * LOW risk only → ALLOW
         */
        String pipelineAction;

        if (highRiskFiles > 0) {

            pipelineAction = "BLOCK";

        } else if (mediumRiskFiles > 0) {

            pipelineAction = "WARN";

        } else {

            pipelineAction = "ALLOW";
        }

        System.out.println();
        System.out.println("========================================");
        System.out.println("PIPELINE DECISION");
        System.out.println("========================================");

        System.out.println(
                "High Risk Files: "
                + highRiskFiles);

        System.out.println(
                "Medium Risk Files: "
                + mediumRiskFiles);

        System.out.println(
                "Low Risk Files: "
                + lowRiskFiles);

        System.out.println(
                "Pipeline Action: "
                + pipelineAction);

        System.out.println(
                "========================================");

        return new AnalysisResponse(
                request.getRepository(),
                request.getCommitId(),
                metricResults.size(),
                highRiskFiles,
                mediumRiskFiles,
                lowRiskFiles,
                pipelineAction,
                predictions
        );
    }
}