package com.defectprediction.backend.metrics;

import java.util.HashSet;
import java.util.Set;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.expr.AssignExpr;
import com.github.javaparser.ast.expr.BinaryExpr;
import com.github.javaparser.ast.expr.BooleanLiteralExpr;
import com.github.javaparser.ast.expr.DoubleLiteralExpr;
import com.github.javaparser.ast.expr.FieldAccessExpr;
import com.github.javaparser.ast.expr.IntegerLiteralExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.expr.StringLiteralExpr;
import com.github.javaparser.ast.expr.UnaryExpr;
import com.github.javaparser.ast.stmt.ForStmt;
import com.github.javaparser.ast.stmt.IfStmt;
import com.github.javaparser.ast.stmt.ReturnStmt;
import com.github.javaparser.ast.stmt.WhileStmt;

public class HalsteadMetrics {

    private final JavaSourceParser sourceParser;

    public HalsteadMetrics() {
        sourceParser = new JavaSourceParser();
    }

    public double calculateVolume(String filePath)
            throws Exception {

        Counts counts = analyze(filePath);

        int vocabulary =
                counts.distinctOperators.size()
                + counts.distinctOperands.size();

        int length =
                counts.totalOperators
                + counts.totalOperands;

        if (vocabulary == 0 || length == 0) {
            return 0.0;
        }

        return length *
                (Math.log(vocabulary) / Math.log(2));
    }

    public double calculateDifficulty(String filePath)
            throws Exception {

        Counts counts = analyze(filePath);

        int n1 =
                counts.distinctOperators.size();

        int n2 =
                counts.distinctOperands.size();

        int N2 =
                counts.totalOperands;

        if (n1 == 0 || n2 == 0) {
            return 0.0;
        }

        return (n1 / 2.0) * ((double) N2 / n2);
    }

    public double calculateEffort(String filePath)
            throws Exception {

        double volume =
                calculateVolume(filePath);

        double difficulty =
                calculateDifficulty(filePath);

        return volume * difficulty;
    }

    private Counts analyze(String filePath)
            throws Exception {

        CompilationUnit compilationUnit =
                sourceParser.parse(filePath);

        Counts counts = new Counts();

        // Operators from binary expressions
        for (BinaryExpr expression :
                compilationUnit.findAll(BinaryExpr.class)) {

            String operator =
                    expression.getOperator().asString();

            counts.distinctOperators.add(operator);
            counts.totalOperators++;
        }

        // Unary operators
        for (UnaryExpr expression :
                compilationUnit.findAll(UnaryExpr.class)) {

            String operator =
                    expression.getOperator().asString();

            counts.distinctOperators.add(operator);
            counts.totalOperators++;
        }

        // Assignment operators
        for (AssignExpr expression :
                compilationUnit.findAll(AssignExpr.class)) {

            String operator =
                    expression.getOperator().asString();

            counts.distinctOperators.add(operator);
            counts.totalOperators++;
        }

        // Method calls are treated as operators
        for (MethodCallExpr expression :
                compilationUnit.findAll(MethodCallExpr.class)) {

            String methodName =
                    expression.getNameAsString();

            counts.distinctOperators.add(
                    methodName);

            counts.totalOperators++;
        }

        // Names / variables
        for (NameExpr expression :
                compilationUnit.findAll(NameExpr.class)) {

            String name =
                    expression.getNameAsString();

            counts.distinctOperands.add(name);
            counts.totalOperands++;
        }

        // Field accesses
        for (FieldAccessExpr expression :
                compilationUnit.findAll(FieldAccessExpr.class)) {

            String field =
                    expression.getNameAsString();

            counts.distinctOperands.add(field);
            counts.totalOperands++;
        }

        // Integer literals
        for (IntegerLiteralExpr expression :
                compilationUnit.findAll(
                        IntegerLiteralExpr.class)) {

            String value =
                    expression.getValue();

            counts.distinctOperands.add(value);
            counts.totalOperands++;
        }

        // Double literals
        for (DoubleLiteralExpr expression :
                compilationUnit.findAll(
                        DoubleLiteralExpr.class)) {

            String value =
                    expression.getValue();

            counts.distinctOperands.add(value);
            counts.totalOperands++;
        }

        // String literals
        for (StringLiteralExpr expression :
                compilationUnit.findAll(
                        StringLiteralExpr.class)) {

            String value =
                    expression.getValue();

            counts.distinctOperands.add(value);
            counts.totalOperands++;
        }

        // Boolean literals
for (BooleanLiteralExpr expression :
        compilationUnit.findAll(
                BooleanLiteralExpr.class)) {

    String value =
            String.valueOf(expression.getValue());

    counts.distinctOperands.add(value);
    counts.totalOperands++;
}
        // Control-flow keywords as operators
        int ifCount =
                compilationUnit.findAll(
                        IfStmt.class).size();

        for (int i = 0; i < ifCount; i++) {
            counts.distinctOperators.add("if");
            counts.totalOperators++;
        }

        int forCount =
                compilationUnit.findAll(
                        ForStmt.class).size();

        for (int i = 0; i < forCount; i++) {
            counts.distinctOperators.add("for");
            counts.totalOperators++;
        }

        int whileCount =
                compilationUnit.findAll(
                        WhileStmt.class).size();

        for (int i = 0; i < whileCount; i++) {
            counts.distinctOperators.add("while");
            counts.totalOperators++;
        }

        // Return statement
        int returnCount =
                compilationUnit.findAll(
                        ReturnStmt.class).size();

        for (int i = 0; i < returnCount; i++) {
            counts.distinctOperators.add("return");
            counts.totalOperators++;
        }

        return counts;
    }

    private static class Counts {

        Set<String> distinctOperators =
                new HashSet<>();

        Set<String> distinctOperands =
                new HashSet<>();

        int totalOperators = 0;

        int totalOperands = 0;
    }
}