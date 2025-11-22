from typing import List
from .generators import Generator, integer, float_val, boolean, string, list_of
from .combinators import one_of, tuple_of

# =====================================================
# Estrategias Numéricas y Booleanas
# =====================================================

def small_ints() -> Generator[int]:
    """Enteros pequeños (-10 a 10)."""
    return integer(-10, 10)

def positive_ints(max_value: int = 100) -> Generator[int]:
    """Enteros positivos."""
    return integer(0, max_value)

def small_floats() -> Generator[float]:
    """Flotantes pequeños."""
    return float_val(-10.0, 10.0)

def booleans() -> Generator[bool]:
    return boolean()

# =====================================================
# Estrategias de Texto y Estructuras
# =====================================================

def small_strings(max_length: int = 10) -> Generator[str]:
    return string(0, max_length)

def emails() -> Generator[str]:
    """Generador simple de emails simulados."""
    def make_email(user, domain):
        return f"{user}@{domain}.com"
    
    user_gen = string(min_length=3, max_length=8)
    domain_gen = string(min_length=3, max_length=5)
    
    # Usamos map2 (definido conceptualmente) o lo hacemos manual con map
    # Aquí lo haremos manual combinando dos strings:
    gen_tuple = tuple_of(user_gen, domain_gen)
    return gen_tuple.map(lambda t: make_email(t[0], t[1]))

# =====================================================
# Estrategias Compuestas
# =====================================================

def one_of_str_int() -> Generator:
    """Elige entre entero pequeño o cadena corta."""
    return one_of([small_ints(), small_strings()])