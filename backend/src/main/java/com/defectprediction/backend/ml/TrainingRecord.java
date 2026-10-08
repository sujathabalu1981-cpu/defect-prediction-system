package com.defectprediction.backend.ml;

public class TrainingRecord {

    private double loc;
    private double cyclomaticComplexity;
    private double essentialComplexity;
    private double designComplexity;
    private double halsteadVolume;
    private double halsteadDifficulty;
    private double halsteadEffort;
    private double branchCount;
    private boolean defects;

    public TrainingRecord(
            double loc,
            double cyclomaticComplexity,
            double essentialComplexity,
            double designComplexity,
            double halsteadVolume,
            double halsteadDifficulty,
            double halsteadEffort,
            double branchCount,
            boolean defects) {

        this.loc = loc;
        this.cyclomaticComplexity = cyclomaticComplexity;
        this.essentialComplexity = essentialComplexity;
        this.designComplexity = designComplexity;
        this.halsteadVolume = halsteadVolume;
        this.halsteadDifficulty = halsteadDifficulty;
        this.halsteadEffort = halsteadEffort;
        this.branchCount = branchCount;
        this.defects = defects;
    }

    public double getLoc() {
        return loc;
    }

    public double getCyclomaticComplexity() {
        return cyclomaticComplexity;
    }

    public double getEssentialComplexity() {
        return essentialComplexity;
    }

    public double getDesignComplexity() {
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

    public double getBranchCount() {
        return branchCount;
    }

    public boolean isDefects() {
        return defects;
    }
}