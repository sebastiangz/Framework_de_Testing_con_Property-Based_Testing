import pytest
import random
from src.combinators import one_of, frequency, tuple_of, map2
from src.generators import Generator

# Generadores simples para testing
def constant(value):
    """Generador que siempre devuelve el mismo valor"""
    return Generator(
        generate=lambda rng, size: value,
        shrink=lambda v: []
    )

def integers(min_val=0, max_val=100):
    """Generador de enteros simples"""
    def generate(rng, size):
        return rng.randint(min_val, max_val)
    
    def shrink(value):
        shrinks = []
        if value > min_val:
            shrinks.append(value - 1)
        if value < max_val:
            shrunks.append(value + 1)
        return shrinks
    
    return Generator(generate, shrink)

def booleans():
    """Generador de booleanos"""
    return Generator(
        generate=lambda rng, size: rng.choice([True, False]),
        shrink=lambda v: []
    )

class TestOneOf:
    def test_one_of_chooses_from_generators(self):
        """Test que one_of elige entre los generadores proporcionados"""
        # Setup
        gen1 = constant("a")
        gen2 = constant("b")
        gen3 = constant("c")
        one_of_gen = one_of([gen1, gen2, gen3])
        
        rng = random.Random(42)  # Semilla fija para reproducibilidad
        size = 10
        
        # Ejecución
        result = one_of_gen.generate(rng, size)
        
        # Verificación
        assert result in ["a", "b", "c"]
    
    def test_one_of_shrink(self):
        """Test del shrinking de one_of"""
        # Setup - generadores con shrinking
        gen1 = integers(0, 10)
        gen2 = integers(20, 30)
        one_of_gen = one_of([gen1, gen2])
        
        # Test shrinking con valor que pertenece al primer generador
        shrinks = one_of_gen.shrink(5)
        assert 4 in shrinks or 6 in shrinks  # Debería reducir a 4 o 6
        
        # Test shrinking con valor que pertenece al segundo generador
        shrinks = one_of_gen.shrink(25)
        assert 24 in shrinks or 26 in shrinks

class TestFrequency:
    def test_frequency_respects_weights(self):
        """Test que frequency respeta los pesos de los generadores"""
        # Setup - gen_a con peso 1, gen_b con peso 9
        gen_a = constant("a")
        gen_b = constant("b")
        freq_gen = frequency([(1, gen_a), (9, gen_b)])
        
        rng = random.Random(42)
        size = 10
        
        # Ejecutar múltiples veces y contar frecuencias
        results = [freq_gen.generate(rng, size) for _ in range(1000)]
        
        count_a = results.count("a")
        count_b = results.count("b")
        
        # Verificación - b debería aparecer aproximadamente 9 veces más que a
        ratio = count_b / max(count_a, 1)  # Evitar división por cero
        assert 5 <= ratio <= 15  # Margen amplio para variabilidad aleatoria
    
    def test_frequency_shrink(self):
        """Test del shrinking de frequency"""
        # Setup
        gen1 = integers(0, 10)
        gen2 = integers(20, 30)
        freq_gen = frequency([(1, gen1), (1, gen2)])
        
        # Test shrinking
        shrinks = freq_gen.shrink(5)
        assert len(shrinks) > 0

class TestTupleOf:
    def test_tuple_of_combines_generators(self):
        """Test que tuple_of combina múltiples generadores"""
        # Setup
        int_gen = integers(1, 10)
        bool_gen = booleans()
        tuple_gen = tuple_of(int_gen, bool_gen)
        
        rng = random.Random(42)
        size = 10
        
        # Ejecución
        result = tuple_gen.generate(rng, size)
        
        # Verificación
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], int)
        assert isinstance(result[1], bool)
        assert 1 <= result[0] <= 10
    
    def test_tuple_of_shrink(self):
        """Test del shrinking de tuple_of"""
        # Setup
        int_gen = integers(0, 10)
        bool_gen = booleans()
        tuple_gen = tuple_of(int_gen, bool_gen)
        
        # Test shrinking
        original = (5, True)
        shrinks = tuple_gen.shrink(original)
        
        # Debería generar tuplas reducidas
        assert len(shrinks) > 0
        for shrunk in shrinks:
            assert isinstance(shrunk, tuple)
            assert len(shrunk) == 2

class TestMap2:
    def test_map2_applies_function(self):
        """Test que map2 aplica la función a los valores generados"""
        # Setup
        int_gen1 = integers(1, 5)
        int_gen2 = integers(1, 5)
        
        # Función que suma dos números
        map2_gen = map2(int_gen1, int_gen2, lambda a, b: a + b)
        
        rng = random.Random(42)
        size = 10
        
        # Ejecución
        result = map2_gen.generate(rng, size)
        
        # Verificación
        assert isinstance(result, int)
        assert 2 <= result <= 10  # 1+1=2, 5+5=10
    
    def test_map2_with_different_types(self):
        """Test map2 con tipos diferentes"""
        # Setup
        int_gen = integers(1, 3)
        bool_gen = booleans()
        
        # Función que combina int y bool
        map2_gen = map2(int_gen, bool_gen, lambda num, flag: f"{num}-{flag}")
        
        rng = random.Random(42)
        size = 10
        
        # Ejecución
        result = map2_gen.generate(rng, size)
        
        # Verificación
        assert isinstance(result, str)
        parts = result.split("-")
        assert len(parts) == 2
        assert parts[0] in ["1", "2", "3"]
        assert parts[1] in ["True", "False"]

def test_integration_multiple_combinators():
    """Test de integración usando múltiples combinadores"""
    # Crear un generador complejo combinando varios combinadores
    int_gen = integers(1, 10)
    bool_gen = booleans()
    
    # one_of entre int y bool
    mixed_gen = one_of([int_gen, bool_gen])
    
    # frequency con diferentes pesos
    weighted_gen = frequency([(2, int_gen), (1, bool_gen)])
    
    # tuple_of combinando todo
    complex_gen = tuple_of(mixed_gen, weighted_gen)
    
    rng = random.Random(42)
    size = 10
    
    # Generar algunos valores para verificar que funciona
    for _ in range(10):
        result = complex_gen.generate(rng, size)
        assert isinstance(result, tuple)
        assert len(result) == 2

# Tests de propiedades (property-based testing)
def test_one_of_always_returns_valid_value():
    """Property test: one_of siempre devuelve valores de los generadores fuente"""
    gens = [constant("a"), constant("b"), integers(1, 5)]
    one_of_gen = one_of(gens)
    
    rng = random.Random(42)
    
    for _ in range(100):
        result = one_of_gen.generate(rng, 10)
        assert (result == "a" or result == "b" or isinstance(result, int))