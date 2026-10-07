package com.defectprediction.backend.metrics;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class CouplingCalculator {

    public int calculateCoupling(
            String filePath,
            List<String> allJavaFiles) throws IOException {

        Path path = Path.of(filePath);

        List<String> lines = Files.readAllLines(path);

        Set<String> projectClasses = new HashSet<>();

        for (String file : allJavaFiles) {

            Path javaFile = Path.of(file);

            String fileName = javaFile.getFileName().toString();

            if (fileName.endsWith(".java")) {

                String className =
                        fileName.substring(0, fileName.length() - 5);

                projectClasses.add(className);
            }
        }

        StringBuilder content = new StringBuilder();

        for (String line : lines) {

            String trimmedLine = line.trim();

            if (!trimmedLine.startsWith("//")) {
                content.append(trimmedLine).append(" ");
            }
        }

        Set<String> dependencies = new HashSet<>();

        for (String className : projectClasses) {

            if (content.toString().contains(className)
                    && !className.equals(
                            getCurrentClassName(filePath))) {

                dependencies.add(className);
            }
        }

        return dependencies.size();
    }

    private String getCurrentClassName(String filePath) {

        Path path = Path.of(filePath);

        String fileName =
                path.getFileName().toString();

        return fileName.substring(
                0,
                fileName.length() - 5);
    }
}