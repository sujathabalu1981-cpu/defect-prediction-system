package com.defectprediction.backend.metrics;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class CyclomaticComplexityCalculator {

    public int calculateComplexity(String filePath) throws IOException {

        Path path = Path.of(filePath);

        List<String> lines = Files.readAllLines(path);

        int complexity = 1;

        for (String line : lines) {

            String code = line.trim();

            if (code.startsWith("//")) {
                continue;
            }

            if (code.contains("if (")
                    || code.contains("if(")) {
                complexity++;
            }

            if (code.contains("else if")
                    || code.contains("for (")
                    || code.contains("for(")
                    || code.contains("while (")
                    || code.contains("while(")
                    || code.contains("case ")
                    || code.contains("catch (")
                    || code.contains("catch(")
                    || code.contains("&&")
                    || code.contains("||")
                    || code.contains("?")) {

                complexity++;
            }
        }

        return complexity;
    }
}