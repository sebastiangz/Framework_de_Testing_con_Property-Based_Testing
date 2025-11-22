import pytest
import random
from src.strategies import (
    small_ints, 
    positive_ints, 
    small_floats, 
    booleans,
    small_strings,
    emails,
    one_of_str_int
)

@pytest.fixture
def rng():
    return random.Random(42)

class TestNumericStrategies:
    
    def test_small_ints_range(self, rng):
        """Verifica que small_ints se mantenga en el rango -10 a 10."""
        gen = small_ints()
        for _ in range(50):
            val = gen.generate(rng, size=10)
            assert isinstance(val, int)
            assert -10 <= val <= 10

    def test_positive_ints_default(self, rng):
        """Verifica enteros positivos con config por defecto."""
        gen = positive_ints()
        for _ in range(50):
            val = gen.generate(rng, size=10)
            assert val >= 0
            assert val <= 100 # Default max

    def test_positive_ints_custom_max(self, rng):
        """Verifica que se respete el argumento max_value."""
        gen = positive_ints(max_value=1000)
        vals = [gen.generate(rng, size=10) for _ in range(50)]
        
        assert min(vals) >= 0
        assert max(vals) <= 1000
        # Verificar que al menos uno sea mayor que el default anterior para asegurar que cambió
        assert any(v > 100 for v in vals)

    def test_small_floats_range(self, rng):
        gen = small_floats()
        for _ in range(50):
            val = gen.generate(rng, size=10)
            assert isinstance(val, float)
            assert -10.0 <= val <= 10.0

    def test_booleans_strategy(self, rng):
        gen = booleans()
        val = gen.generate(rng, size=1)
        assert isinstance(val, bool)

class TestTextStrategies:

    def test_small_strings_length(self, rng):
        """Verifica la longitud máxima de las cadenas pequeñas."""
        gen = small_strings(max_length=5)
        for _ in range(20):
            val = gen.generate(rng, size=10)
            assert isinstance(val, str)
            assert len(val) <= 5

    def test_emails_format(self, rng):
        """
        Prueba de integración: verifica que la estrategia de email 
        combine correctamente usuario y dominio usando map.
        """
        gen = emails()
        for _ in range(20):
            val = gen.generate(rng, size=10)
            
            # Validaciones básicas de estructura
            assert isinstance(val, str)
            assert "@" in val
            assert val.endswith(".com")
            
            # Desglose simple
            parts = val.split("@")
            assert len(parts) == 2
            user, domain_part = parts
            domain = domain_part.replace(".com", "")
            
            # Verificamos longitudes mínimas definidas en strategies.py
            # user: min 3, domain: min 3
            assert len(user) >= 3
            assert len(domain) >= 3

    def test_emails_shrink_limitation(self):
        """
        Nota importante: En tu implementación base de Generator.map, 
        definiste que el shrink devuelve siempre [].
        Esta prueba confirma que esa limitación se hereda en la estrategia emails.
        """
        gen = emails()
        val = "abc@def.com"
        # Como usa .map(), el shrink se pierde (según tu código en generators.py)
        assert gen.shrink(val) == []

class TestCompositeStrategies:

    def test_one_of_str_int_types(self, rng):
        """
        Verifica que la estrategia mixta produzca ambos tipos de datos.
        """
        gen = one_of_str_int()
        types_seen = set()
        
        for _ in range(100):
            val = gen.generate(rng, size=10)
            types_seen.add(type(val))
            
            # Validación de rangos específicos de esta estrategia
            if isinstance(val, int):
                assert -10 <= val <= 10
            elif isinstance(val, str):
                assert len(val) <= 10
        
        # Estadísticamente deberíamos ver ambos
        assert int in types_seen
        assert str in types_seen
        # Y nada más
        assert len(types_seen) == 2