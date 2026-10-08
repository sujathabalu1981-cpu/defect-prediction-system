package com.defectprediction.backend.ml;

import java.util.List;

public class DatasetStatistics {

    public static void main(String[] args) throws Exception {

        DatasetPreprocessor preprocessor =
                new DatasetPreprocessor();

        String datasetFolder =
                "D:\\Fourth year projects\\Sw metrics\\NASA-promise-dataset-repository-main";

        List<TrainingRecord> records =
                preprocessor.loadAllDatasets(datasetFolder);

        System.out.println("===== NASA DATASET STATISTICS =====");

        System.out.println(
                "Total records: " + records.size());

        calculateStatistics(
                "LOC",
                records.stream()
                        .mapToDouble(TrainingRecord::getLoc)
                        .toArray());

        calculateStatistics(
                "Cyclomatic Complexity",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getCyclomaticComplexity)
                        .toArray());

        calculateStatistics(
                "Essential Complexity",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getEssentialComplexity)
                        .toArray());

        calculateStatistics(
                "Design Complexity",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getDesignComplexity)
                        .toArray());

        calculateStatistics(
                "Halstead Volume",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getHalsteadVolume)
                        .toArray());

        calculateStatistics(
                "Halstead Difficulty",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getHalsteadDifficulty)
                        .toArray());

        calculateStatistics(
                "Halstead Effort",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getHalsteadEffort)
                        .toArray());

        calculateStatistics(
                "Branch Count",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getBranchCount)
                        .toArray());

        System.out.println(
                "==================================");
    }

    private static void calculateStatistics(
            String metricName,
            double[] values) {

        double minimum = Double.MAX_VALUE;
        double maximum = Double.MIN_VALUE;

        double sum = 0;

        for (double value : values) {

            if (value < minimum) {
                minimum = value;
            }

            if (value > maximum) {
                maximum = value;
            }

            sum += value;
        }

        double average =
                sum / values.length;

        System.out.println();

        System.out.println(
                "Metric: " + metricName);

        System.out.println(
                "Minimum: " + minimum);

        System.out.println(
                "Maximum: " + maximum);

        System.out.println(
                "Average: " + average);
    }
}