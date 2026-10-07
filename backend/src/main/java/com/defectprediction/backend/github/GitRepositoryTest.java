package com.defectprediction.backend.github;

public class GitRepositoryTest {

    public static void main(String[] args)
            throws Exception {

        GitRepositoryService service =
                new GitRepositoryService();

        String repositoryUrl =
                "https://github.com/sujathabalu1981-cpu/defect-prediction-system.git";

        String commitId =
                "c069f4aff1b4dacc5aba750bdd2cc90dd7acc6a0";

        String path =
                service.cloneRepository(
                        repositoryUrl,
                        commitId);

        System.out.println(
                "Repository downloaded to:");

        System.out.println(path);
    }
}