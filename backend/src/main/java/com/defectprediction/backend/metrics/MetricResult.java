package com.defectprediction.backend.metrics;

public class MetricResult {

    private String filePath;

    // Existing metrics
    private int loc;
    private int cyclomaticComplexity;
    private int coupling;
    private double cohesion;
    private int codeChurn;
    private int inheritanceDepth;

    // Bayesian Network metrics
    private int essentialComplexity;
    private int designComplexity;
    private double halsteadVolume;
    private double halsteadDifficulty;
    private double halsteadEffort;
    private int branchCount;

    public MetricResult(
            String filePath,
            int loc,
            int cyclomaticComplexity,
            int coupling,
            double cohesion,
            int codeChurn,
            int inheritanceDepth,
            int essentialComplexity,
            int designComplexity,
            double halsteadVolume,
            double halsteadDifficulty,
            double halsteadEffort,
            int branchCount) {

        this.filePath = filePath;

        this.loc = loc;
        this.cyclomaticComplexity = cyclomaticComplexity;
        this.coupling = coupling;
        this.cohesion = cohesion;
        this.codeChurn = codeChurn;
        this.inheritanceDepth = inheritanceDepth;

        this.essentialComplexity = essentialComplexity;
        this.designComplexity = designComplexity;
        this.halsteadVolume = halsteadVolume;
        this.halsteadDifficulty = halsteadDifficulty;
        this.halsteadEffort = halsteadEffort;
        this.branchCount = branchCount;
    }

    public String getFilePath() {
        return filePath;
    }

    public int getLoc() {
        return loc;
    }

    public int getCyclomaticComplexity() {
        return cyclomaticComplexity;
    }

    public int getCoupling() {
        return coupling;
    }

    public double getCohesion() {
        return cohesion;
    }

    public int getCodeChurn() {
        return codeChurn;
    }

    public int getInheritanceDepth() {
        return inheritanceDepth;
    }

    public int getEssentialComplexity() {
        return essentialComplexity;
    }

    public int getDesignComplexity() {
        return designComplexity;
    }

    public double getHalsteadVolume() {
        return halsteadVolume;
    }

    public double getHalsteadDifficulty() {
        return halsteadDifficulty;
    }

    public double getHalsteadEffort() {
        return halsteadEffort;
    }

    public int getBranchCount() {
        return branchCount;
    }
}