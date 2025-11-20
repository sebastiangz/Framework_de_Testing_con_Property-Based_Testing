"""
test_properties.py
-------------------
Pruebas unitarias para properties.py y TestRunner.
Incluye casos de prueba simples y verificación de shrinking.
"""

import random
from src.generators import int_gen, list_of, str_gen
from src.properties import for_all, TestRunner

def test_property_int():
    rng = random.Random(42)
    gen = int_gen(0, 10)

    # Propiedad: valor generado siempre >= 0
    def prop_func(x):
        assert x >= 0
        return True

    prop = for_all(gen, prop_func)
    runner = TestRunner(iterations=10)
    runner.run(prop)


def test_property_list_length():
    rng = random.Random(42)
    gen = list_of(int_gen(0, 5), min_size=1, max_size=5)

    # Propiedad: longitud <= 5
    def prop_func(lst):
        assert len(lst) <= 5
        return True

    prop = for_all(gen, prop_func)
    runner = TestRunner(iterations=10)
    runner.run(prop)


def test_property_str_shrink():
    rng = random.Random(42)
    gen = str_gen(5)

    # Propiedad falsa: la longitud debe ser >= 10 (intencional para probar shrinking)
    def prop_func(s):
        assert len(s) >= 10
        return True

    prop = for_all(gen, prop_func)
    runner = TestRunner(iterations=10)
    runner.run(prop)

# Ejecutar tests si se corre directamente
if __name__ == '__main__':
    print("--- test_property_int ---")
    test_property_int()
    print("\n--- test_property_list_length ---")
    test_property_list_length()
    print("\n--- test_property_str_shrink ---")
    test_property_str_shrink()