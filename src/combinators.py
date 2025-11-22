from typing import TypeVar, Callable, List, Any, Tuple
import random
from .generators import Generator

T = TypeVar("T")
U = TypeVar("U")

def one_of(generators: List[Generator[T]]) -> Generator[T]:
    """Elige aleatoriamente uno de los generadores dados."""
    def generate(rng: random.Random, size: int) -> T:
        gen = rng.choice(generators)
        return gen.generate(rng, size)
    
    def shrink(value: T) -> List[T]:
        # Simplificación: intentamos shrinkear con el primer generador que pueda
        # (Idealmente guardaríamos cuál generador produjo el valor)
        for gen in generators:
            try:
                shrinks = gen.shrink(value)
                if shrinks: return shrinks
            except: pass
        return []
    return Generator(generate, shrink)

def tuple_of(*gens: Generator) -> Generator[Tuple]:
    """Combina varios generadores en una tupla."""
    def generate(rng: random.Random, size: int) -> Tuple:
        return tuple(gen.generate(rng, size) for gen in gens)
    
    def shrink(values: Tuple) -> List[Tuple]:
        shrunk = []
        # Shrink simple: reducir el primer elemento
        if values:
            first_val = values[0]
            rest = values[1:]
            for s in gens[0].shrink(first_val):
                shrunk.append((s,) + rest)
        return shrunk
    return Generator(generate, shrink)

def map2(gen_a: Generator[T], gen_b: Generator[U], fn: Callable[[T, U], Any]) -> Generator:
    """Aplica una función a dos generadores."""
    def generate(rng: random.Random, size: int):
        a = gen_a.generate(rng, size)
        b = gen_b.generate(rng, size)
        return fn(a, b)
    
    def shrink(value):
        return []
    return Generator(generate, shrink)