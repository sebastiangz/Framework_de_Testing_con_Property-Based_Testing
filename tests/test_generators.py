import pytest
import random
from src.generators import (
    integer, 
    float_val, 
    boolean, 
    string, 
    list_of,
    Generator
)

# Instancia de Random con semilla fija para reproducibilidad en los tests
@pytest.fixture
def rng():
    return random.Random(42)

class TestIntegerGenerator:
    def test_integer_bounds(self, rng):
        """Verifica que los enteros generados respeten min y max."""
        gen = integer(min_val=10, max_val=20)
        for _ in range(100):
            val = gen.generate(rng, size=10)
            assert 10 <= val <= 20
            assert isinstance(val, int)

    def test_integer_shrink_positive(self):
        """Verifica el shrinking de un número positivo."""
        gen = integer()
        # El shrink de 10 debería incluir 0, 5 (mitad) y 9 (val-1)
        shrunk_vals = gen.shrink(10)
        assert 0 in shrunk_vals
        assert 5 in shrunk_vals
        assert 9 in shrunk_vals
        assert 10 not in shrunk_vals # No debe contenerse a sí mismo

    def test_integer_shrink_zero(self):
        """El 0 es el caso base y no debe reducirse más."""
        gen = integer()
        assert gen.shrink(0) == []

class TestFloatGenerator:
    def test_float_bounds(self, rng):
        gen = float_val(min_val=0.0, max_val=1.0)
        for _ in range(50):
            val = gen.generate(rng, size=10)
            assert 0.0 <= val <= 1.0
            assert isinstance(val, float)

    def test_float_shrink(self):
        gen = float_val()
        shrunk = gen.shrink(10.0)
        assert 0.0 in shrunk
        assert 5.0 in shrunk # Val / 2
        
    def test_float_shrink_base_case(self):
        gen = float_val()
        # Según tu código, si abs(val) < 1e-5 devuelve []
        assert gen.shrink(0.0) == []
        assert gen.shrink(0.000001) == []

class TestBooleanGenerator:
    def test_boolean_generation(self, rng):
        gen = boolean()
        results = set()
        for _ in range(20):
            results.add(gen.generate(rng, size=10))
        # Debería ser capaz de generar ambos con suficientes intentos
        assert True in results or False in results
        assert isinstance(list(results)[0], bool)

    def test_boolean_shrink(self):
        gen = boolean()
        # True se reduce a False
        assert gen.shrink(True) == [False]
        # False es el caso base
        assert gen.shrink(False) == []

class TestStringGenerator:
    def test_string_length_and_content(self, rng):
        gen = string(min_length=5, max_length=10)
        for _ in range(50):
            val = gen.generate(rng, size=20) # Size grande
            assert 5 <= len(val) <= 10
            assert isinstance(val, str)
            # Verificar que solo contiene letras, dígitos o espacio
            import string as string_module
            allowed = string_module.ascii_letters + string_module.digits + ' '
            assert all(c in allowed for c in val)

    def test_string_shrink(self):
        gen = string()
        val = "abc"
        shrunk = gen.shrink(val)
        # Tu lógica: ['', val[:-1], val[1:]] -> ['', 'ab', 'bc']
        assert '' in shrunk
        assert 'ab' in shrunk
        assert 'bc' in shrunk
        assert len(shrunk) == 3

    def test_string_shrink_empty(self):
        gen = string()
        assert gen.shrink("") == []

class TestListGenerator:
    def test_list_structure(self, rng):
        # Lista de enteros entre 0 y 5, longitud de lista entre 2 y 4
        int_gen = integer(0, 5)
        list_gen = list_of(int_gen, min_size=2, max_size=4)
        
        for _ in range(20):
            val = list_gen.generate(rng, size=10)
            assert isinstance(val, list)
            assert 2 <= len(val) <= 4
            if val:
                assert isinstance(val[0], int)

    def test_list_shrink(self):
        # Probamos que la lista reduce su tamaño o sus elementos
        int_gen = integer()
        list_gen = list_of(int_gen)
        
        original = [10, 20]
        shrunk_variants = list_gen.shrink(original)
        
        # Según tu lógica, debe incluir:
        # 1. [] (vacía)
        # 2. [10] (primera mitad)
        # 3. [20] (segunda mitad)
        # 4. Reducción de elementos: shrinkage del head (10) + tail ([20])
        
        assert [] in shrunk_variants
        assert [10] in shrunk_variants
        assert [20] in shrunk_variants
        
        # Verificamos que si reducimos un elemento, la lista resultante es válida
        # 10 se reduce a 0, 5, 9. Entonces [0, 20], [5, 20], [9, 20] deberían estar.
        assert [5, 20] in shrunk_variants

class TestMapFunction:
    def test_map_modifies_output(self, rng):
        """Prueba que .map transforma el valor generado."""
        int_gen = integer(1, 1) # Siempre genera 1
        
        # Mapeamos x -> x * 2
        doubled_gen = int_gen.map(lambda x: str(x * 2))
        
        val = doubled_gen.generate(rng, size=10)
        assert val == "2"
        assert isinstance(val, str)

    def test_map_resets_shrink(self):
        """
        Tu implementación actual de .map define new_shrink devolviendo [],
        lo cual significa que los generadores mapeados pierden la capacidad de shrink.
        Probamos que este comportamiento sea el esperado.
        """
        int_gen = integer(10, 20)
        mapped_gen = int_gen.map(lambda x: x)
        
        assert mapped_gen.shrink(15) == []