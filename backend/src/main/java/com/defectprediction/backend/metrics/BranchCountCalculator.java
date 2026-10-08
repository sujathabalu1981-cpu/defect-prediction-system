package com.defectprediction.backend.metrics;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.expr.ConditionalExpr;
import com.github.javaparser.ast.stmt.CatchClause;
import com.github.javaparser.ast.stmt.DoStmt;
import com.github.javaparser.ast.stmt.ForStmt;
import com.github.javaparser.ast.stmt.IfStmt;
import com.github.javaparser.ast.stmt.SwitchEntry;
import com.github.javaparser.ast.stmt.WhileStmt;

public class BranchCountCalculator {

    private final JavaSourceParser sourceParser;

    public BranchCountCalculator() {
        sourceParser = new JavaSourceParser();
    }

    public int calculateBranchCount(String filePath)
            throws Exception {

        CompilationUnit compilationUnit =
                sourceParser.parse(filePath);

        int branchCount = 0;

        branchCount +=
                compilationUnit.findAll(IfStmt.class).size();

        branchCount +=
                compilationUnit.findAll(ForStmt.class).size();

        branchCount +=
                compilationUnit.findAll(WhileStmt.class).size();

        branchCount +=
                compilationUnit.findAll(DoStmt.class).size();

        branchCount +=
                compilationUnit.findAll(CatchClause.class).size();

        branchCount +=
                compilationUnit.findAll(ConditionalExpr.class).size();

        for (SwitchEntry entry :
                compilationUnit.findAll(SwitchEntry.class)) {

            if (!entry.getLabels().isEmpty()) {
                branchCount++;
            }
        }

        return branchCount;
    }
}