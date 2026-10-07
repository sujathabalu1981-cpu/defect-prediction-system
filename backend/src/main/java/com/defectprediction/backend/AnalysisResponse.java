package com.defectprediction.backend;

import java.util.List;

import com.defectprediction.backend.metrics.MetricResult;

public class AnalysisResponse {

    private String repository;
    private String commitId;
    private int totalFiles;
    private List<MetricResult> metrics;

    public AnalysisResponse(
            String repository,
            String commitId,
            int totalFiles,
            List<MetricResult> metrics) {

        this.repository = repository;
        this.commitId = commitId;
        this.totalFiles = totalFiles;
        this.metrics = metrics;
    }

    public String getRepository() {
        return repository;
    }

    public String getCommitId() {
        return commitId;
    }

    public int getTotalFiles() {
        return totalFiles;
    }

    public List<MetricResult> getMetrics() {
        return metrics;
    }
}