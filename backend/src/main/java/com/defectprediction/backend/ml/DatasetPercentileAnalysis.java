package com.defectprediction.backend.ml;

import java.util.Arrays;
import java.util.List;

public class DatasetPercentileAnalysis {

    public static void main(String[] args) throws Exception {

        DatasetPreprocessor preprocessor =
                new DatasetPreprocessor();

        String datasetFolder =
                "D:\\Fourth year projects\\Sw metrics\\NASA-promise-dataset-repository-main";

        List<TrainingRecord> records =
                preprocessor.loadAllDatasets(datasetFolder);

        System.out.println(
                "===== NASA PERCENTILE ANALYSIS =====");

        System.out.println(
                "Total records: " + records.size());

        calculatePercentiles(
                "LOC",
                records.stream()
                        .mapToDouble(TrainingRecord::getLoc)
                        .toArray());

        calculatePercentiles(
                "Cyclomatic Complexity",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getCyclomaticComplexity)
                        .toArray());

        calculatePercentiles(
                "Essential Complexity",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getEssentialComplexity)
                        .toArray());

        calculatePercentiles(
                "Design Complexity",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getDesignComplexity)
                        .toArray());

        calculatePercentiles(
                "Halstead Volume",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getHalsteadVolume)
                        .toArray());

        calculatePercentiles(
                "Halstead Difficulty",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getHalsteadDifficulty)
                        .toArray());

        calculatePercentiles(
                "Halstead Effort",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getHalsteadEffort)
                        .toArray());

        calculatePercentiles(
                "Branch Count",
                records.stream()
                        .mapToDouble(
                                TrainingRecord::getBranchCount)
                        .toArray());

        System.out.println(
                "====================================");
    }

    private static void calculatePercentiles(
            String metricName,
            double[] values) {

        Arrays.sort(values);

        double p25 =
                percentile(values, 25);

        double p50 =
                percentile(values, 50);

        double p75 =
                percentile(values, 75);

        double p90 =
                percentile(values, 90);

        System.out.println();

        System.out.println(
                "Metric: " + metricName);

        System.out.println(
                "25th Percentile: " + p25);

        System.out.println(
                "50th Percentile: " + p50);

        System.out.println(
                "75th Percentile: " + p75);

        System.out.println(
                "90th Percentile: " + p90);
    }

    private static double percentile(
            double[] values,
            double percentile) {

        if (values.length == 0) {
            return 0;
        }

        double position =
                (percentile / 100.0)
                * (values.length - 1);

        int lower =
                (int) Math.floor(position);

        int upper =
                (int) Math.ceil(position);

        if (lower == upper) {
            return values[lower];
        }

        double weight =
                position - lower;

        return values[lower]
                + weight
                * (values[upper] - values[lower]);
    }
}