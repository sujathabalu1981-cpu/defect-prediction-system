package com.defectprediction.backend.metrics;

public class MetricResult {

    private String filePath;
    private int loc;
    private int cyclomaticComplexity;
    private int coupling;
    private double cohesion;
    private int codeChurn;
    private int inheritanceDepth;

    public MetricResult(
            String filePath,
            int loc,
            int cyclomaticComplexity,
            int coupling,
            double cohesion,
            int codeChurn,
            int inheritanceDepth) {

        this.filePath = filePath;
        this.loc = loc;
        this.cyclomaticComplexity = cyclomaticComplexity;
        this.coupling = coupling;
        this.cohesion = cohesion;
        this.codeChurn = codeChurn;
        this.inheritanceDepth = inheritanceDepth;
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
}