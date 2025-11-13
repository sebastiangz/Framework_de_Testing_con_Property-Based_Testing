from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, List
import random
import string

# Tipo genérico para permitir que Generator funcione con cualquier tipo de dato
T = TypeVar('T')

@dataclass(frozen=True)
class Generator(Generic[T]):
    """
    Representa un generador de valores aleatorios junto con su función de reducción (shrink).
    El generador sigue el estilo funcional puro: recibe un RNG (random.Random) y un tamaño.
    """
    # Función que genera un valor a partir de un generador de números aleatorios (rng) y un tamaño (size)
    generate: Callable[[random.Random, int], T]

    # Función que produce una lista de versiones más simples (reducidas) del valor generado
    shrink: Callable[[T], List[T]]

    # Permite transformar los valores generados usando una función pura (como map en programación funcional)
    def map(self, fn: Callable[[T], T]) -> "Generator[T]":
        def new_generate(rng: random.Random, size: int) -> T:
            return fn(self.generate(rng, size))
        def new_shrink(value: T) -> List[T]:
            return [fn(v) for v in self.shrink(value)]
        return Generator(new_generate, new_shrink)

    # Permite encadenar generadores dependientes del valor anterior (flatMap)
    def flat_map(self, fn: Callable[[T], "Generator[T]"]) -> "Generator[T]":
        def new_generate(rng: random.Random, size: int) -> T:
            value = self.generate(rng, size)
            next_gen = fn(value)
            return next_gen.generate(rng, size)
        def new_shrink(value: T) -> List[T]:
            # No todos los generadores tienen shrink complejo, se deja simple por ahora
            return self.shrink(value)
        return Generator(new_generate, new_shrink)

# =====================================================
#  Generadores básicos
# =====================================================

# Generador de enteros
def int_gen(min_value: int = 0, max_value: int = 100) -> Generator[int]:
    """
    Genera enteros dentro del rango [min_value, max_value].
    """
    def generate(rng: random.Random, size: int) -> int:
        # Usa size para ajustar el rango si es pequeño
        limit = min(max_value, max(min_value + size, min_value))
        return rng.randint(min_value, limit)

    def shrink(value: int) -> List[int]:
        # Intenta reducir el valor hacia 0
        if value == 0:
            return []
        return [value // 2, 0] if value > 0 else [value // 2, 0]

    return Generator(generate, shrink)

# Generador de números flotantes
def float_gen(min_value: float = 0.0, max_value: float = 1.0) -> Generator[float]:
    """
    Genera números flotantes entre min_value y max_value.
    """
    def generate(rng: random.Random, size: int) -> float:
        scale = min(1.0, size / 100)
        return rng.uniform(min_value, max_value * scale)

    def shrink(value: float) -> List[float]:
        # Reduce el valor flotante hacia 0.0
        if abs(value) < 1e-9:
            return []
        return [value / 2.0, 0.0]

    return Generator(generate, shrink)

# Generador de booleanos
def bool_gen() -> Generator[bool]:
    """
    Genera valores booleanos (True o False).
    """
    def generate(rng: random.Random, size: int) -> bool:
        return rng.choice([True, False])

    def shrink(value: bool) -> List[bool]:
        # Reduce True -> False
        return [False] if value else []

    return Generator(generate, shrink)

# Generador de cadenas de texto
def str_gen(length: int = 5) -> Generator[str]:
    """
    Genera cadenas aleatorias de letras.
    """
    def generate(rng: random.Random, size: int) -> str:
        # Ajusta el largo con el parámetro size
        n = max(1, min(length, size))
        return ''.join(rng.choice(string.ascii_letters) for _ in range(n))

    def shrink(value: str) -> List[str]:
        # Reduce quitando la última letra
        if not value:
            return []
        return [value[:-1]]

    return Generator(generate, shrink)