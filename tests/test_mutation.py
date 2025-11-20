"""
test_mutation.py
----------------
Pruebas básicas para mutation.py
Incluye tests de mutantes y cálculo de mutation score.
"""

from src.mutation import generate_mutants, mutation_score

# ----------------------------
# Código de ejemplo a testear
# ----------------------------
original_code = """
def add(a, b):
    return a + b

"""

def simple_test_suite():
    # Test básico para add(a, b)
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0

# ----------------------------
# Prueba 1: Generación de mutantes
# ----------------------------
mutants = generate_mutants(original_code)
print(f"Mutantes generados ({len(mutants)}):")
for m in mutants:
    print(m)

# ----------------------------
# Prueba 2: Calcular mutation score
# ----------------------------
score = mutation_score(original_code, simple_test_suite)
print(f"Mutation score: {score}")

if __name__ == '__main__':
    print("--- Ejecución de pruebas de mutación ---")
    print(f"Número de mutantes: {len(mutants)}")
    print(f"Mutation score: {score}")
