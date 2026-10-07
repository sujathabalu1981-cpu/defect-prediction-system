package com.defectprediction.backend.metrics;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class MetricExtractor {

    public List<MetricResult> extractMetrics(String projectPath)
            throws IOException {

        ProjectScanner scanner = new ProjectScanner();

        LocCalculator locCalculator =
                new LocCalculator();

        CyclomaticComplexityCalculator complexityCalculator =
                new CyclomaticComplexityCalculator();

        CouplingCalculator couplingCalculator =
                new CouplingCalculator();

        CohesionCalculator cohesionCalculator =
                new CohesionCalculator();

        CodeChurnCalculator churnCalculator =
                new CodeChurnCalculator();

        InheritanceDepthCalculator inheritanceCalculator =
                new InheritanceDepthCalculator();

        List<String> javaFiles =
                scanner.findJavaFiles(projectPath);

        List<MetricResult> results =
                new ArrayList<>();

        for (String file : javaFiles) {

            int loc =
                    locCalculator.calculateLOC(file);

            int complexity =
                    complexityCalculator.calculateComplexity(file);

            int coupling =
                    couplingCalculator.calculateCoupling(
                            file,
                            javaFiles);

            double cohesion =
                    cohesionCalculator.calculateCohesion(file);

            int codeChurn =
        churnCalculator.calculateChurn(
                file,
                projectPath);

            int inheritanceDepth =
                    inheritanceCalculator.calculateDepth(
                            file,
                            javaFiles);

            MetricResult result =
                    new MetricResult(
                            file,
                            loc,
                            complexity,
                            coupling,
                            cohesion,
                            codeChurn,
                            inheritanceDepth);

            results.add(result);
        }

        return results;
    }
}