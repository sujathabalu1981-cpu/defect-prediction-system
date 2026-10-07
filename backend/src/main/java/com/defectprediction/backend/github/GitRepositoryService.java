package com.defectprediction.backend.github;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;

public class GitRepositoryService {

    public String cloneRepository(
            String repositoryUrl,
            String commitId) throws Exception {

        Path tempDirectory =
                Files.createTempDirectory("defect-analysis-");

        String repositoryPath =
                tempDirectory.toAbsolutePath().toString();

        runCommand(
                "git",
                "clone",
                repositoryUrl,
                repositoryPath
        );

        runCommand(
                "git",
                "-C",
                repositoryPath,
                "checkout",
                commitId
        );

        return repositoryPath;
    }

    private void runCommand(String... command)
            throws IOException, InterruptedException {

        ProcessBuilder processBuilder =
                new ProcessBuilder(command);

        processBuilder.redirectErrorStream(true);

        Process process =
                processBuilder.start();

        BufferedReader reader =
                new BufferedReader(
                        new InputStreamReader(
                                process.getInputStream()));

        String line;

        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }

        int exitCode =
                process.waitFor();

        if (exitCode != 0) {

            throw new RuntimeException(
                    "Git command failed with exit code: "
                    + exitCode);
        }
    }
}