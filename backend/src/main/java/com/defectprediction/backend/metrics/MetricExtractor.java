package com.defectprediction.backend.metrics;

import java.util.ArrayList;
import java.util.List;

public class MetricExtractor {

    public List<MetricResult> extractMetrics(String projectPath)
            throws Exception {

        ProjectScanner scanner =
                new ProjectScanner();

        LocCalculator locCalculator =
                new LocCalculator();

        JavaParserCyclomaticComplexityCalculator
                complexityCalculator =
                new JavaParserCyclomaticComplexityCalculator();

        BranchCountCalculator branchCalculator =
                new BranchCountCalculator();

        HalsteadMetrics halsteadCalculator =
                new HalsteadMetrics();

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

            // Existing metrics
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

            // Bayesian Network metrics
            int branchCount =
                    branchCalculator.calculateBranchCount(file);

            double halsteadVolume =
                    halsteadCalculator.calculateVolume(file);

            double halsteadDifficulty =
                    halsteadCalculator.calculateDifficulty(file);

            double halsteadEffort =
                    halsteadCalculator.calculateEffort(file);

            // Temporary AST-based approximations
            int essentialComplexity =
                    complexity;

            int designComplexity =
                    complexity;

            MetricResult result =
                    new MetricResult(
                            file,
                            loc,
                            complexity,
                            coupling,
                            cohesion,
                            codeChurn,
                            inheritanceDepth,
                            essentialComplexity,
                            designComplexity,
                            halsteadVolume,
                            halsteadDifficulty,
                            halsteadEffort,
                            branchCount
                    );

            results.add(result);
        }

        return results;
    }
}