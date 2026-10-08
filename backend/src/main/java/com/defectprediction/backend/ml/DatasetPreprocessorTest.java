package com.defectprediction.backend.ml;

import java.util.List;

public class DatasetPreprocessorTest {

    public static void main(String[] args) throws Exception {

        DatasetPreprocessor preprocessor =
                new DatasetPreprocessor();

        String datasetFolder =
                "D:\\Fourth year projects\\Sw metrics\\NASA-promise-dataset-repository-main";

        List<TrainingRecord> records =
                preprocessor.loadAllDatasets(datasetFolder);

        int defective = 0;
        int nonDefective = 0;

        for (TrainingRecord record : records) {

            if (record.isDefects()) {
                defective++;
            } else {
                nonDefective++;
            }
        }

        System.out.println(
                "===== NASA DATASET =====");

        System.out.println(
                "Total records: "
                + records.size());

        System.out.println(
                "Defective records: "
                + defective);

        System.out.println(
                "Non-defective records: "
                + nonDefective);

        System.out.println(
                "========================");
    }
}