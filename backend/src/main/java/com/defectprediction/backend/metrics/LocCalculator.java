package com.defectprediction.backend.metrics;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class LocCalculator {

    public int calculateLOC(String filePath) throws IOException {

        Path path = Path.of(filePath);

        List<String> lines = Files.readAllLines(path);

        int loc = 0;

        for (String line : lines) {

            String trimmedLine = line.trim();

            if (!trimmedLine.isEmpty()
                    && !trimmedLine.startsWith("//")) {

                loc++;
            }
        }

        return loc;
    }
}