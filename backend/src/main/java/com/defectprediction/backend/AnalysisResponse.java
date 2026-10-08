package com.defectprediction.backend;

import java.util.List;

public class AnalysisResponse {

    private String repository;
    private String commitId;

    private int filesAnalyzed;
    private int highRiskFiles;
    private int mediumRiskFiles;
    private int lowRiskFiles;

    private String pipelineAction;

    private List<String> predictions;

    public AnalysisResponse(
            String repository,
            String commitId,
            int filesAnalyzed,
            int highRiskFiles,
            int mediumRiskFiles,
            int lowRiskFiles,
            String pipelineAction,
            List<String> predictions) {

        this.repository = repository;
        this.commitId = commitId;
        this.filesAnalyzed = filesAnalyzed;
        this.highRiskFiles = highRiskFiles;
        this.mediumRiskFiles = mediumRiskFiles;
        this.lowRiskFiles = lowRiskFiles;
        this.pipelineAction = pipelineAction;
        this.predictions = predictions;
    }

    public String getRepository() {
        return repository;
    }

    public String getCommitId() {
        return commitId;
    }

    public int getFilesAnalyzed() {
        return filesAnalyzed;
    }

    public int getHighRiskFiles() {
        return highRiskFiles;
    }

    public int getMediumRiskFiles() {
        return mediumRiskFiles;
    }

    public int getLowRiskFiles() {
        return lowRiskFiles;
    }

    public String getPipelineAction() {
        return pipelineAction;
    }

    public List<String> getPredictions() {
        return predictions;
    }
}