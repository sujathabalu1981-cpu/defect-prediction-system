package com.defectprediction.backend.metrics;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class CohesionCalculator {

    public double calculateCohesion(String filePath)
            throws IOException {

        Path path = Path.of(filePath);

        List<String> lines = Files.readAllLines(path);

        Set<String> fields = new HashSet<>();
        int methodCount = 0;
        int methodsUsingFields = 0;

        boolean insideMethod = false;
        Set<String> currentMethodFields = new HashSet<>();

        for (String line : lines) {

            String code = line.trim();

            if (code.startsWith("//") || code.isEmpty()) {
                continue;
            }

            if (code.contains("private ")
                    || code.contains("protected ")
                    || code.contains("public ")) {

                if (code.contains(";")
                        && !code.contains("(")) {

                    String[] parts = code.split("\\s+");

                    if (parts.length >= 2) {
                        fields.add(parts[parts.length - 1]
                                .replace(";", ""));
                    }
                }
            }

            if (code.contains("(")
                    && code.contains(")")
                    && code.endsWith("{")) {

                methodCount++;

                insideMethod = true;

                currentMethodFields.clear();
            }

            if (insideMethod) {

                for (String field : fields) {

                    if (code.contains(field)) {
                        currentMethodFields.add(field);
                    }
                }
            }

            if (insideMethod && code.equals("}")) {

                if (!currentMethodFields.isEmpty()) {
                    methodsUsingFields++;
                }

                insideMethod = false;
            }
        }

        if (methodCount == 0) {
            return 1.0;
        }

        return (double) methodsUsingFields / methodCount;
    }
}