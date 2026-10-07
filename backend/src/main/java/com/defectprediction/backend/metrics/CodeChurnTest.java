package com.defectprediction.backend.metrics;

public class CodeChurnTest {

    public static void main(String[] args) throws Exception {

        CodeChurnCalculator calculator =
                new CodeChurnCalculator();

        String filePath =
                "src/main/java/com/defectprediction/backend/AnalysisController.java";

        int churn =
        calculator.calculateChurn(
                filePath,
                ".");

        System.out.println(
                "Code Churn: " + churn);
    }
}