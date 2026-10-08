package com.defectprediction.backend.ml;

public class MetricFeature {

    private int LOC;
    private int Cyclomatic;
    private int Essential;
    private int Design;

    private double HalsteadVolume;
    private double HalsteadDifficulty;
    private double HalsteadEffort;

    private int BranchCount;

    public MetricFeature(
            int LOC,
            int Cyclomatic,
            int Essential,
            int Design,
            double HalsteadVolume,
            double HalsteadDifficulty,
            double HalsteadEffort,
            int BranchCount) {

        this.LOC = LOC;
        this.Cyclomatic = Cyclomatic;
        this.Essential = Essential;
        this.Design = Design;
        this.HalsteadVolume = HalsteadVolume;
        this.HalsteadDifficulty = HalsteadDifficulty;
        this.HalsteadEffort = HalsteadEffort;
        this.BranchCount = BranchCount;
    }

    public int getLOC() {
        return LOC;
    }

    public int getCyclomatic() {
        return Cyclomatic;
    }

    public int getEssential() {
        return Essential;
    }

    public int getDesign() {
        return Design;
    }

    public double getHalsteadVolume() {
        return HalsteadVolume;
    }

    public double getHalsteadDifficulty() {
        return HalsteadDifficulty;
    }

    public double getHalsteadEffort() {
        return HalsteadEffort;
    }

    public int getBranchCount() {
        return BranchCount;
    }
}