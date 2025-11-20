"""
test_generators.py
-------------------
Pruebas unitarias para los generadores del framework, incluyendo shrinking.
"""

import random
from src.generators import int_gen, float_gen, bool_gen, str_gen

def test_int_gen():
    rng = random.Random(42)
    gen = int_gen(0, 10)
    for _ in range(10):
        val = gen.generate(rng, 10)
        assert 0 <= val <= 10, f"Valor generado fuera del rango: {val}"
        # Test shrink
        shrunk = gen.shrink(val)
        for s in shrunk:
            assert 0 <= s <= val, f"Shrink produjo valor inválido: {s}"
    print("test_int_gen passed")

def test_float_gen():
    rng = random.Random(42)
    gen = float_gen(0.0, 1.0)
    for _ in range(10):
        val = gen.generate(rng, 100)
        assert 0.0 <= val <= 1.0, f"Valor generado fuera del rango: {val}"
        # Test shrink
        shrunk = gen.shrink(val)
        for s in shrunk:
            assert 0.0 <= s <= val, f"Shrink produjo valor inválido: {s}"
    print("test_float_gen passed")

def test_bool_gen():
    rng = random.Random(42)
    gen = bool_gen()
    for _ in range(10):
        val = gen.generate(rng, 10)
        assert val in [True, False], f"Valor generado no booleano: {val}"
        # Test shrink
        shrunk = gen.shrink(val)
        for s in shrunk:
            assert s in [False], f"Shrink produjo valor inválido: {s}"
    print("test_bool_gen passed")

def test_str_gen():
    rng = random.Random(42)
    gen = str_gen(5)
    for _ in range(10):
        val = gen.generate(rng, 5)
        assert isinstance(val, str), f"Valor generado no es string: {val}"
        assert 1 <= len(val) <= 5, f"Longitud inválida: {len(val)}"
        # Test shrink
        shrunk = gen.shrink(val)
        for s in shrunk:
            assert isinstance(s, str), f"Shrink produjo valor no string: {s}"
            assert len(s) < len(val), f"Shrink no redujo longitud: {s}"
    print("test_str_gen passed")

# Ejecutar tests si se corre directamente
if __name__ == '__main__':
    test_int_gen()
    test_float_gen()
    test_bool_gen()
    test_str_gen()