import pytest
import random
from src.combinators import one_of, tuple_of, map2
from src.generators import integer, string, boolean

# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------

@pytest.fixture
def rng():
    """Generador de números aleatorios con semilla fija para reproducibilidad."""
    return random.Random(42)

# -----------------------------------------------------------------------------
# Test para one_of
# -----------------------------------------------------------------------------

class TestOneOf:
    def test_one_of_selection(self, rng):
        """
        Verifica que one_of sea capaz de elegir valores de cualquiera 
        de los generadores proporcionados.
        """
        gen_int = integer()
        gen_str = string()
        combined = one_of([gen_int, gen_str])
        
        types_seen = set()
        
        # Generamos suficientes veces para asegurar que salen ambos tipos
        for _ in range(50):
            val = combined.generate(rng, size=10)
            types_seen.add(type(val))
        
        # Deberíamos haber visto tanto enteros como strings
        assert int in types_seen
        assert str in types_seen
        assert len(types_seen) == 2

    def test_one_of_shrink_delegation(self):
        """
        Verifica que el shrinking se delegue al generador correcto.
        Tu implementación itera sobre los generadores hasta que uno funciona.
        """
        gen_int = integer()
        gen_str = string()
        combined = one_of([gen_int, gen_str])
        
        # Caso A: Shrinkear un entero (debería ser manejado por gen_int)
        # El 10 se reduce típicamente a 0, 5, 9
        shrunk_int = combined.shrink(10)
        assert 0 in shrunk_int
        assert 5 in shrunk_int

        # Caso B: Shrinkear un string (gen_int fallará, debería capturar excepción y usar gen_str)
        # "abc" se reduce a "", "ab", "bc"
        shrunk_str = combined.shrink("abc")
        assert "" in shrunk_str
        assert "bc" in shrunk_str

# -----------------------------------------------------------------------------
# Test para tuple_of
# -----------------------------------------------------------------------------

class TestTupleOf:
    def test_tuple_structure(self, rng):
        """
        Verifica que se genere una tupla con la longitud y tipos correctos.
        """
        gen = tuple_of(integer(), string(), boolean())
        val = gen.generate(rng, size=10)
        
        assert isinstance(val, tuple)
        assert len(val) == 3
        assert isinstance(val[0], int)
        assert isinstance(val[1], str)
        assert isinstance(val[2], bool)

    def test_tuple_shrink_head_only(self):
        """
        Prueba crítica: Tu implementación actual de tuple_of SOLO reduce el primer elemento.
        Este test verifica ese comportamiento específico.
        """
        gen = tuple_of(integer(), string())
        
        original_val = (10, "hello")
        shrunk_vals = gen.shrink(original_val)
        
        # Verificamos que el primer elemento (10) se redujo (ej. a 0)
        # Esperamos ver (0, "hello")
        expected_variant = (0, "hello")
        assert expected_variant in shrunk_vals
        
        # Verificamos que el segundo elemento ("hello") NO cambió en ninguna variante
        # ya que tu lógica es: shrunk.append((s,) + rest)
        for item in shrunk_vals:
            assert item[1] == "hello"

    def test_tuple_empty(self, rng):
        """Manejo de generadores de tuplas vacías."""
        gen = tuple_of()
        val = gen.generate(rng, size=10)
        assert val == ()
        assert gen.shrink(()) == []

# -----------------------------------------------------------------------------
# Test para map2
# -----------------------------------------------------------------------------

class TestMap2:
    def test_map2_logic(self, rng):
        """
        Verifica que la función se aplique a los resultados de dos generadores.
        """
        # Usamos generadores deterministas (rango min=max) para probar la matemática
        gen_a = integer(min_val=5, max_val=5)
        gen_b = integer(min_val=10, max_val=10)
        
        def add(x, y):
            return x + y
            
        gen_sum = map2(gen_a, gen_b, add)
        val = gen_sum.generate(rng, size=10)
        
        assert val == 15  # 5 + 10

    def test_map2_different_types(self, rng):
        """Verifica map2 combinando tipos distintos (int y str)."""
        gen_str = string(min_length=1, max_length=1) # Un caracter
        gen_int = integer(min_val=3, max_val=3)      # Numero 3
        
        def repeat(s, n):
            return s * n
            
        gen_comb = map2(gen_str, gen_int, repeat)
        val = gen_comb.generate(rng, size=10)
        
        # Debería ser un string de longitud 3
        assert isinstance(val, str)
        assert len(val) == 3

    def test_map2_no_shrink(self):
        """
        Verifica que map2 devuelve lista vacía en shrink,
        tal como está definido en la implementación.
        """
        gen = map2(integer(), integer(), lambda x, y: x + y)
        assert gen.shrink(100) == []