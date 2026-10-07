package com.defectprediction.backend;

import java.util.List;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.defectprediction.backend.github.GitRepositoryService;
import com.defectprediction.backend.metrics.MetricExtractor;
import com.defectprediction.backend.metrics.MetricResult;

@RestController
public class AnalysisController {

    @PostMapping("/analyze")
    public AnalysisResponse analyze(
            @RequestBody AnalysisRequest request)
            throws Exception {

        // Step 1: Download the requested GitHub repository
        GitRepositoryService gitService =
                new GitRepositoryService();

        String repositoryPath =
                gitService.cloneRepository(
                        request.getRepositoryUrl(),
                        request.getCommitId());

        // Step 2: Extract metrics from the downloaded repository
        MetricExtractor extractor =
                new MetricExtractor();

        List<MetricResult> results =
                extractor.extractMetrics(repositoryPath);

        // Step 3: Return the metrics
        return new AnalysisResponse(
                request.getRepository(),
                request.getCommitId(),
                results.size(),
                results);
    }
}