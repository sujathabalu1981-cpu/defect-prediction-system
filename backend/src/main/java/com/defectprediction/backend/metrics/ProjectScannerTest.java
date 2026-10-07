package com.defectprediction.backend.metrics;

import java.util.List;

public class ProjectScannerTest {

    public static void main(String[] args) throws Exception {

        ProjectScanner scanner = new ProjectScanner();

        String projectPath = ".";

        List<String> javaFiles = scanner.findJavaFiles(projectPath);

        System.out.println("Java files found:");

        for (String file : javaFiles) {
            System.out.println(file);
        }

        System.out.println("Total Java files: " + javaFiles.size());
    }
}