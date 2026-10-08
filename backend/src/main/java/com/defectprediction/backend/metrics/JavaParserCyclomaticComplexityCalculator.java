package com.defectprediction.backend.metrics;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.expr.BinaryExpr;
import com.github.javaparser.ast.expr.ConditionalExpr;
import com.github.javaparser.ast.stmt.CatchClause;
import com.github.javaparser.ast.stmt.DoStmt;
import com.github.javaparser.ast.stmt.ForStmt;
import com.github.javaparser.ast.stmt.IfStmt;
import com.github.javaparser.ast.stmt.SwitchEntry;
import com.github.javaparser.ast.stmt.WhileStmt;

public class JavaParserCyclomaticComplexityCalculator {

    private final JavaSourceParser sourceParser;

    public JavaParserCyclomaticComplexityCalculator() {
        sourceParser = new JavaSourceParser();
    }

    public int calculateComplexity(String filePath)
            throws Exception {

        CompilationUnit compilationUnit =
                sourceParser.parse(filePath);

        // Every method starts with complexity 1.
        int methodCount =
                compilationUnit.findAll(
                        com.github.javaparser.ast.body.MethodDeclaration.class
                ).size();

        int complexity = methodCount;

        // If statements
        complexity +=
                compilationUnit.findAll(IfStmt.class).size();

        // For loops
        complexity +=
                compilationUnit.findAll(ForStmt.class).size();

        // While loops
        complexity +=
                compilationUnit.findAll(WhileStmt.class).size();

        // Do-while loops
        complexity +=
                compilationUnit.findAll(DoStmt.class).size();

        // Catch blocks
        complexity +=
                compilationUnit.findAll(CatchClause.class).size();

        // Ternary operator
        complexity +=
                compilationUnit.findAll(ConditionalExpr.class).size();

        // switch cases
        for (SwitchEntry entry :
                compilationUnit.findAll(SwitchEntry.class)) {

            if (!entry.getLabels().isEmpty()) {
                complexity++;
            }
        }

        // Logical AND / OR
        for (BinaryExpr expression :
                compilationUnit.findAll(BinaryExpr.class)) {

            if (expression.getOperator()
                    == BinaryExpr.Operator.AND) {

                complexity++;
            }

            if (expression.getOperator()
                    == BinaryExpr.Operator.OR) {

                complexity++;
            }
        }

        return complexity;
    }
}