package com.defectprediction.backend.metrics;

import java.io.IOException;
import java.nio.file.Path;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;

public class JavaSourceParser {

    private final JavaParser parser;

    public JavaSourceParser() {
        parser = new JavaParser();
    }

    public CompilationUnit parse(String filePath)
            throws IOException {

        Path path = Path.of(filePath);

        return parser.parse(path)
                .getResult()
                .orElseThrow(
                        () -> new IOException(
                                "Unable to parse Java file: "
                                + filePath));
    }
}