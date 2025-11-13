# src/combinators.py
from typing import TypeVar, Callable, List
import random
from .generators import Generator

# Tipos genéricos
T = TypeVar("T")
U = TypeVar("U")

# ---------------------------------------------------------
# COMBINADORES DE GENERADORES
# ---------------------------------------------------------
# Permiten crear generadores más complejos a partir de otros.
# Ejemplo: elegir entre varios generadores o combinarlos en tuplas.
# ---------------------------------------------------------

def one_of(generators: List[Generator[T]]) -> Generator[T]:
    """
    Devuelve un generador que elige aleatoriamente uno 
    de los generadores dados.
    """
    def generate(rng: random.Random, size: int) -> T:
        # Elige un generador al azar y produce un valor
        gen = rng.choice(generators)
        return gen.generate(rng, size)
    
    def shrink(value: T) -> List[T]:
        # Usa el primer generador que pueda reducir el valor
        for gen in generators:
            shrinks = gen.shrink(value)
            if shrinks:
                return shrinks
        return []
    
    return Generator(generate, shrink)


def frequency(weighted_gens: List[tuple[int, Generator[T]]]) -> Generator[T]:
    """
    Devuelve un generador que elige uno según pesos dados.
    Ejemplo: [(1, gen_a), (3, gen_b)] → gen_b se elige 3 veces más.
    """
    def generate(rng: random.Random, size: int) -> T:
        total = sum(w for w, _ in weighted_gens)
        choice = rng.uniform(0, total)
        upto = 0
        for weight, gen in weighted_gens:
            if upto + weight >= choice:
                return gen.generate(rng, size)
            upto += weight
        # En caso de redondeo, devuelve el último
        return weighted_gens[-1][1].generate(rng, size)
    
    def shrink(value: T) -> List[T]:
        # Intenta reducir usando cada generador
        for _, gen in weighted_gens:
            shrinks = gen.shrink(value)
            if shrinks:
                return shrinks
        return []
    
    return Generator(generate, shrink)


def tuple_of(*gens: Generator) -> Generator[tuple]:
    """
    Combina varios generadores en una tupla.
    Ejemplo: tuple_of(integer(), string()) → genera (42, "abc")
    """
    def generate(rng: random.Random, size: int) -> tuple:
        # Genera un valor por cada generador
        return tuple(gen.generate(rng, size) for gen in gens)
    
    def shrink(values: tuple) -> List[tuple]:
        # Intenta reducir cada elemento de la tupla
        shrunk = []
        for i, gen in enumerate(gens):
            for s in gen.shrink(values[i]):
                new_tuple = values[:i] + (s,) + values[i+1:]
                shrunk.append(new_tuple)
        return shrunk
    
    return Generator(generate, shrink)


def map2(
    gen_a: Generator[T],
    gen_b: Generator[U],
    fn: Callable[[T, U], any]
) -> Generator:
    """
    Aplica una función binaria a los valores generados por dos generadores.
    Ejemplo: map2(integer(), integer(), lambda a,b: a+b)
    """
    def generate(rng: random.Random, size: int):
        # Genera un valor de cada generador y los combina con la función
        a = gen_a.generate(rng, size)
        b = gen_b.generate(rng, size)
        return fn(a, b)
    
    def shrink(value):
        # En este ejemplo simplificado no se hace shrinking real,
        # solo se muestra la estructura.
        return []
    
    return Generator(generate, shrink)
