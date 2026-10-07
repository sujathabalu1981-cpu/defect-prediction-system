package com.defectprediction.backend.metrics;

import java.io.IOException;
import java.util.List;

public class ProjectMetricsCalculator {

    public void calculateProjectLOC(String projectPath) throws IOException {

        ProjectScanner scanner = new ProjectScanner();

        LocCalculator locCalculator = new LocCalculator();

        List<String> javaFiles = scanner.findJavaFiles(projectPath);

        System.out.println("===== PROJECT METRICS =====");

        for (String file : javaFiles) {

            int loc = locCalculator.calculateLOC(file);

            System.out.println("File: " + file);
            System.out.println("LOC: " + loc);
            System.out.println("---------------------------");
        }

        System.out.println("Total Java files: " + javaFiles.size());
    }
}