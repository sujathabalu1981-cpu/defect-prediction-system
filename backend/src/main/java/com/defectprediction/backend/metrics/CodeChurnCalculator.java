package com.defectprediction.backend.metrics;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class CodeChurnCalculator {

    public int calculateChurn(
            String filePath,
            String repositoryPath) throws IOException {

        ProcessBuilder processBuilder =
                new ProcessBuilder(
                        "git",
                        "-C",
                        repositoryPath,
                        "log",
                        "--numstat",
                        "--format=",
                        "--",
                        filePath
                );

        processBuilder.redirectErrorStream(true);

        Process process =
                processBuilder.start();

        BufferedReader reader =
                new BufferedReader(
                        new InputStreamReader(
                                process.getInputStream()));

        int addedLines = 0;
        int deletedLines = 0;

        String line;

        while ((line = reader.readLine()) != null) {

            line = line.trim();

            if (line.isEmpty()) {
                continue;
            }

            String[] parts = line.split("\\s+");

            if (parts.length >= 2) {

                try {

                    addedLines += Integer.parseInt(parts[0]);
                    deletedLines += Integer.parseInt(parts[1]);

                } catch (NumberFormatException e) {

                    // Ignore non-numeric Git output
                }
            }
        }

        return addedLines + deletedLines;
    }
}