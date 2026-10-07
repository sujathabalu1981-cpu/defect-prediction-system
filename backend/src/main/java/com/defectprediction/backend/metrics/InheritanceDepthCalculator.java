package com.defectprediction.backend.metrics;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class InheritanceDepthCalculator {

    public int calculateDepth(
            String filePath,
            List<String> allJavaFiles) throws IOException {

        Map<String, String> parentMap = new HashMap<>();

        // Build class -> parent relationship
        for (String file : allJavaFiles) {

            Path path = Path.of(file);

            List<String> lines = Files.readAllLines(path);

            for (String line : lines) {

                String code = line.trim();

                if (code.startsWith("public class ")
                        || code.startsWith("class ")
                        || code.startsWith("public abstract class ")
                        || code.startsWith("abstract class ")) {

                    String className = extractClassName(code);
                    String parentName = extractParentName(code);

                    if (className != null) {
                        parentMap.put(className, parentName);
                    }

                    break;
                }
            }
        }

        String currentClass =
                Path.of(filePath)
                        .getFileName()
                        .toString()
                        .replace(".java", "");

        int depth = 0;

        String parent = parentMap.get(currentClass);

        while (parent != null && !parent.equals("Object")) {

            depth++;

            parent = parentMap.get(parent);
        }

        return depth;
    }

    private String extractClassName(String code) {

        String[] parts = code.split("\\s+");

        for (int i = 0; i < parts.length - 1; i++) {

            if (parts[i].equals("class")) {
                return parts[i + 1];
            }
        }

        return null;
    }

    private String extractParentName(String code) {

        if (!code.contains("extends")) {
            return null;
        }

        String[] parts = code.split("\\s+");

        for (int i = 0; i < parts.length - 1; i++) {

            if (parts[i].equals("extends")) {
                return parts[i + 1];
            }
        }

        return null;
    }
}