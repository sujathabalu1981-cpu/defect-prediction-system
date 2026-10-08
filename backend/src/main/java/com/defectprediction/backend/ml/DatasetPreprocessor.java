package com.defectprediction.backend.ml;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class DatasetPreprocessor {

    public List<TrainingRecord> loadAllDatasets(
            String datasetFolder) throws IOException {

        List<TrainingRecord> records = new ArrayList<>();

        records.addAll(
                loadDataset(
                        datasetFolder + "\\cm1.csv",
                        false));

        records.addAll(
                loadDataset(
                        datasetFolder + "\\jm1.csv",
                        false));

        records.addAll(
                loadDataset(
                        datasetFolder + "\\kc1.csv",
                        false));

        records.addAll(
                loadDataset(
                        datasetFolder + "\\kc2.csv",
                        true));

        records.addAll(
                loadDataset(
                        datasetFolder + "\\pc1.csv",
                        false));

        return records;
    }

    private List<TrainingRecord> loadDataset(
            String filePath,
            boolean kc2Dataset) throws IOException {

        List<TrainingRecord> records =
                new ArrayList<>();

        try (BufferedReader reader =
                     new BufferedReader(
                             new FileReader(filePath))) {

            String header = reader.readLine();

            if (header == null) {
                return records;
            }

            String line;

            while ((line = reader.readLine()) != null) {

                if (line.trim().isEmpty()) {
                    continue;
                }

                try {

                    String[] values = line.split(",");

                    double loc =
                            Double.parseDouble(values[0]);

                    double cyclomaticComplexity =
                            Double.parseDouble(values[1]);

                    double essentialComplexity =
                            Double.parseDouble(values[2]);

                    double designComplexity =
                            Double.parseDouble(values[3]);

                    double halsteadVolume =
                            Double.parseDouble(values[5]);

                    double halsteadDifficulty =
                            Double.parseDouble(values[7]);

                    double halsteadEffort =
                            Double.parseDouble(values[9]);

                    double branchCount =
                            Double.parseDouble(values[20]);

                    String defectValue =
                            values[21].trim();

                    boolean defects;

                    if (kc2Dataset) {

                        defects =
                                defectValue.equalsIgnoreCase("yes");

                    } else {

                        defects =
                                defectValue.equalsIgnoreCase("true");
                    }

                    TrainingRecord record =
                            new TrainingRecord(
                                    loc,
                                    cyclomaticComplexity,
                                    essentialComplexity,
                                    designComplexity,
                                    halsteadVolume,
                                    halsteadDifficulty,
                                    halsteadEffort,
                                    branchCount,
                                    defects);

                    records.add(record);

                } catch (Exception e) {

                    System.out.println(
                            "Skipping invalid row in: "
                            + filePath);
                }
            }
        }

        return records;
    }
}