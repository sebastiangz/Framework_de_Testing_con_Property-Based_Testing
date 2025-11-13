"""
Estrategias de testing predefinidas.
Contiene generadores listos para usar: enteros pequeños, listas no vacías, cadenas, booleanos, etc.
"""

from typing import List
import random
from .generators import Generator, int_gen, float_gen, bool_gen, str_gen
from .combinators import one_of, tuple_of

# =====================================================
# Generadores de enteros y flotantes
# =====================================================

def small_ints() -> Generator[int]:
    """
    Generador de enteros pequeños, típicamente usados para pruebas rápidas.
    Rango: -10 a 10
    """
    return int_gen(-10, 10)

def positive_ints(max_value: int = 100) -> Generator[int]:
    """
    Generador de enteros positivos.
    """
    return int_gen(0, max_value)

def small_floats() -> Generator[float]:
    """
    Generador de números flotantes pequeños, entre -10.0 y 10.0
    """
    return float_gen(-10.0, 10.0)

# =====================================================
# Generadores de booleanos
# =====================================================

def booleans() -> Generator[bool]:
    """
    Generador de valores booleanos True/False.
    """
    return bool_gen()

# =====================================================
# Generadores de cadenas
# =====================================================

def small_strings(max_length: int = 10) -> Generator[str]:
    """
    Generador de cadenas cortas de letras.
    """
    return str_gen(max_length)

# =====================================================
# Generadores de listas
# =====================================================

def list_of(gen: Generator, min_size: int = 0, max_size: int = 10) -> Generator[List]:
    """
    Generador de listas usando cualquier generador de elementos.
    """
    def generate(rng: random.Random, size: int) -> List:
        length = rng.randint(min_size, min(max_size, size))
        return [gen.generate(rng, size) for _ in range(length)]

    def shrink(lst: List) -> List[List]:
        if not lst:
            return []
        shrunk = []
        # Lista vacía
        shrunk.append([])
        # Quitar un elemento a la vez
        for i in range(len(lst)):
            shrunk.append(lst[:i] + lst[i+1:])
        # Shrink de elementos individuales
        for i in range(len(lst)):
            for s in gen.shrink(lst[i]):
                shrunk.append(lst[:i] + [s] + lst[i+1:])
        return shrunk

    return Generator(generate, shrink)

# =====================================================
# Generadores compuestos (tuplas y elección)
# =====================================================

def tuple2(gen1: Generator, gen2: Generator) -> Generator[tuple]:
    """
    Generador de tuplas de dos elementos.
    """
    return tuple_of(gen1, gen2)

def one_of_str_int() -> Generator:
    """
    Generador que elige aleatoriamente entre un entero pequeño y una cadena corta.
    """
    return one_of([small_ints(), small_strings()])
