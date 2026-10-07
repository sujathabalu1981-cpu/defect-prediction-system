package com.defectprediction.backend.metrics;

import java.util.List;

public class InheritanceDepthTest {

    public static void main(String[] args) throws Exception {

        ProjectScanner scanner =
                new ProjectScanner();

        List<String> javaFiles =
                scanner.findJavaFiles(".");

        InheritanceDepthCalculator calculator =
                new InheritanceDepthCalculator();

        String filePath =
                "src/main/java/com/defectprediction/backend/AnalysisController.java";

        int depth =
                calculator.calculateDepth(
                        filePath,
                        javaFiles);

        System.out.println(
                "Depth of Inheritance: " + depth);
    }
}