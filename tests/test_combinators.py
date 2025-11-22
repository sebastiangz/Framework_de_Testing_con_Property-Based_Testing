# test_combinators.py
import pytest
import random
from typing import Callable, List as TypeList, TypeVar, Generic
from dataclasses import dataclass
import string

# --- SIMULACIÓN DEL ENTORNO (Clase Generator y Generadores Básicos) ---
# Necesario para que las pruebas de los combinadores funcionen.

T = TypeVar('T')
U = TypeVar('U')

@dataclass(frozen=True)
class Generator(Generic[T]):
    """Versión mínima de la clase Generator para testing."""
    generate: Callable[[random.Random, int], T]
    shrink: Callable[[T], TypeList[T]]

# Generador Básico de Enteros (int_gen)
def int_gen(min_value: int = 0, max_value: int = 100) -> Generator[int]:
    def generate(rng: random.Random, size: int) -> int:
        limit = min(max_value, max(min_value + size, min_value))
        return rng.randint(min_value, limit)
    
    def shrink(value: int) -> TypeList[int]:
        if value == 0: return []
        # Candidatos simples para shrinking: valor/2 y 0
        return [value // 2, 0] if value > 0 else [value // 2, 0]
    
    return Generator(generate, shrink)

# Generador Básico de Cadenas (str_gen)
def str_gen(length: int = 5) -> Generator[str]:
    def generate(rng: random.Random, size: int) -> str:
        n = max(1, min(length, size))
        return ''.join(rng.choice(string.ascii_letters) for _ in range(n))

    def shrink(value: str) -> TypeList[str]:
        if not value: return []
        return [value[:-1]] # Quita el último carácter
    
    return Generator(generate, shrink)

# Generador Básico de Booleanos (bool_gen)
def bool_gen() -> Generator[bool]:
    def generate(rng: random.Random, size: int) -> bool:
        return rng.choice([True, False])

    def shrink(value: bool) -> TypeList[bool]:
        return [False] if value else []
    
    return Generator(generate, shrink)

# --- CÓDIGO DE combinators.py (Para Evitar Errores de Importación) ---
def one_of(generators: TypeList[Generator[T]]) -> Generator[T]:
    def generate(rng: random.Random, size: int) -> T:
        gen = rng.choice(generators)
        return gen.generate(rng, size)
    def shrink(value: T) -> TypeList[T]:
        for gen in generators:
            shrinks = gen.shrink(value)
            if shrinks:
                return shrinks
        return []
    return Generator(generate, shrink)

def frequency(weighted_gens: TypeList[tuple[int, Generator[T]]]) -> Generator[T]:
    def generate(rng: random.Random, size: int) -> T:
        total = sum(w for w, _ in weighted_gens)
        choice = rng.uniform(0, total)
        upto = 0
        for weight, gen in weighted_gens:
            if upto + weight >= choice:
                return gen.generate(rng, size)
            upto += weight
        return weighted_gens[-1][1].generate(rng, size)
    def shrink(value: T) -> TypeList[T]:
        for _, gen in weighted_gens:
            shrinks = gen.shrink(value)
            if shrinks:
                return shrinks
        return []
    return Generator(generate, shrink)

def tuple_of(*gens: Generator) -> Generator[tuple]:
    def generate(rng: random.Random, size: int) -> tuple:
        return tuple(gen.generate(rng, size) for gen in gens)
    def shrink(values: tuple) -> TypeList[tuple]:
        shrunk = []
        for i, gen in enumerate(gens):
            for s in gen.shrink(values[i]):
                new_tuple = values[:i] + (s,) + values[i+1:]
                shrunk.append(new_tuple)
        return shrunk
    return Generator(generate, shrink)

def map2(gen_a: Generator[T], gen_b: Generator[U], fn: Callable[[T, U], any]) -> Generator:
    def generate(rng: random.Random, size: int):
        a = gen_a.generate(rng, size)
        b = gen_b.generate(rng, size)
        return fn(a, b)
    def shrink(value):
        return []
    return Generator(generate, shrink)
# ----------------------------------------------------------------------


@pytest.fixture
def test_rng():
    """Fixture para un generador de números aleatorios reproducible."""
    return random.Random(42)

---

## 🎲 Pruebas para `one_of`

def test_one_of_generate_mixed_types(test_rng):
    """Verifica que one_of pueda generar valores de diferentes generadores."""
    gen_int = int_gen(1, 1)  # Siempre 1
    gen_str = str_gen(1)     # Genera una cadena corta
    
    mixed_gen = one_of([gen_int, gen_str])
    generated_values = [mixed_gen.generate(test_rng, 10) for _ in range(20)]
    
    # Debe haber generado al menos un entero (1) y al menos una cadena
    assert 1 in generated_values
    assert any(isinstance(v, str) for v in generated_values)

def test_one_of_shrink_success():
    """Verifica que one_of use el primer generador que puede reducir el valor."""
    gen_A = int_gen(100, 200) # Shrink para int (e.g., 100 -> 50)
    gen_B = bool_gen()        # Shrink para bool (True -> False)
    
    # Colocamos gen_B primero; si falla, pasa a gen_A
    mixed_gen = one_of([gen_B, gen_A]) 
    
    # 1. Prueba de valor que solo gen_A puede reducir
    value_int = 100
    shrunk_values = mixed_gen.shrink(value_int)
    # gen_B.shrink(100) debe fallar (retornar [])
    assert shrunk_values == int_gen().shrink(value_int)

def test_one_of_shrink_no_match():
    """Verifica que si ningún generador puede reducir el valor, retorna una lista vacía."""
    gen_A = str_gen(1) # Un entero no se puede reducir con un shrinker de str
    gen_B = bool_gen() # Un entero no se puede reducir con un shrinker de bool
    
    mixed_gen = one_of([gen_A, gen_B])
    
    assert mixed_gen.shrink(100) == []

---

## ⚖️ Pruebas para `frequency`

def test_frequency_generate_ratio(test_rng):
    """Verifica que frequency genere valores de acuerdo a las proporciones de peso."""
    gen_A = int_gen(1, 1)  # Siempre 1
    gen_B = int_gen(2, 2)  # Siempre 2

    # Proporción 1:9 (A:B)
    weighted_gen = frequency([(1, gen_A), (9, gen_B)])
    
    runs = 100
    generated_values = [weighted_gen.generate(test_rng, 10) for _ in range(runs)]
    
    count_A = generated_values.count(1)
    count_B = generated_values.count(2)
    
    # El generador B (peso 9) debe ser elegido significativamente más que A (peso 1)
    # 90% (80-100) vs 10% (0-20). Usamos un margen amplio.
    assert count_B > count_A * 3

def test_frequency_shrink_priority():
    """Verifica que frequency use el primer generador en la lista que pueda reducir el valor."""
    # gen_B está primero, pero no puede reducir un entero
    gen_B = str_gen(10)
    # gen_A está segundo y puede reducir el entero 42
    gen_A = int_gen(10, 100) 
    
    weighted_gen = frequency([(1, gen_B), (9, gen_A)])
    value = 42
    
    # Debe ser reducido por el shrinker de gen_A
    shrunk_values = weighted_gen.shrink(value)
    expected_shrinks = gen_A.shrink(value) 
    
    assert shrunk_values == expected_shrinks

---

## 📦 Pruebas para `tuple_of`

def test_tuple_of_generate_structure(test_rng):
    """Verifica que tuple_of genere una tupla con la longitud y tipos correctos."""
    gen_i = int_gen(5, 5) # 5
    gen_s = str_gen(2)    # 2-char string
    gen_b = bool_gen()    # True/False
    
    tuple_gen = tuple_of(gen_i, gen_s, gen_b)
    result = tuple_gen.generate(test_rng, 10)
    
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert result[0] == 5
    assert isinstance(result[1], str)
    assert isinstance(result[2], bool)

def test_tuple_of_shrink_elements():
    """Verifica que tuple_of intente reducir cada elemento de la tupla."""
    gen_i = int_gen(10, 10) # Shrinks: [5, 0]
    gen_s = str_gen(3)      # Shrinks: ["AB"] (si el generado es "ABC")
    
    tuple_gen = tuple_of(gen_i, gen_s)
    
    # Asumimos este valor para probar el shrinker:
    value_to_shrink = (10, "ABC")
    
    shrunk_values = tuple_gen.shrink(value_to_shrink)
    
    # Shrinks generados:
    # 1. Por gen_i (posición 0): (5, "ABC