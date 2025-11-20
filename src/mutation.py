"""
mutation.py
-----------
Implementación básica de mutation testing funcional.
Permite generar mutantes de código (operadores aritméticos y de comparación) y calcular el mutation score.
"""

import ast
from typing import List, Callable

class MutationOperator:
    """Operadores de mutación para código Python."""

    @staticmethod
    def arithmetic_mutations(node: ast.BinOp) -> List[ast.BinOp]:
        """Genera mutaciones cambiando operadores aritméticos."""
        mutations = []
        operators = {
            ast.Add: [ast.Sub, ast.Mult],
            ast.Sub: [ast.Add, ast.Div],
            ast.Mult: [ast.Add, ast.Div],
            ast.Div: [ast.Mult, ast.Sub]
        }
        op_type = type(node.op)
        if op_type in operators:
            for new_op in operators[op_type]:
                mutated = ast.copy_location(
                    ast.BinOp(node.left, new_op(), node.right),
                    node
                )
                mutations.append(mutated)
        return mutations

    @staticmethod
    def comparison_mutations(node: ast.Compare) -> List[ast.Compare]:
        """Genera mutaciones cambiando operadores de comparación."""
        mutations = []
        operators = {
            ast.Eq: [ast.NotEq],
            ast.NotEq: [ast.Eq],
            ast.Lt: [ast.LtE, ast.Gt],
            ast.LtE: [ast.Lt, ast.GtE],
            ast.Gt: [ast.GtE, ast.Lt],
            ast.GtE: [ast.Gt, ast.LtE]
        }
        for i, op in enumerate(node.ops):
            op_type = type(op)
            if op_type in operators:
                for new_op in operators[op_type]:
                    new_ops = node.ops[:i] + [new_op()] + node.ops[i+1:]
                    mutated = ast.copy_location(
                        ast.Compare(node.left, new_ops, node.comparators),
                        node
                    )
                    mutations.append(mutated)
        return mutations


def generate_mutants(source_code: str) -> List[str]:
    """Genera mutantes del código fuente como strings."""
    tree = ast.parse(source_code)
    mutants = []

    class MutationVisitor(ast.NodeVisitor):
        def visit_BinOp(self, node):
            for mutation in MutationOperator.arithmetic_mutations(node):
                mutated_tree = ast.fix_missing_locations(mutation)
                mutants.append(ast.unparse(mutated_tree))
            self.generic_visit(node)

        def visit_Compare(self, node):
            for mutation in MutationOperator.comparison_mutations(node):
                mutated_tree = ast.fix_missing_locations(mutation)
                mutants.append(ast.unparse(mutated_tree))
            self.generic_visit(node)

    visitor = MutationVisitor()
    visitor.visit(tree)
    return mutants


def mutation_score(original_code: str, test_suite: Callable) -> float:
    """Calcula el mutation score del código ejecutando tests contra los mutantes."""
    mutants = generate_mutants(original_code)
    killed = 0
    for mutant_code in mutants:
        try:
            # Ejecuta el código mutante y la suite de tests
            exec(mutant_code)
            test_suite()
            # Si no falla, el mutante sobrevivió
        except:
            # Mutante matado por el test
            killed += 1
    return killed / len(mutants) if mutants else 1.0