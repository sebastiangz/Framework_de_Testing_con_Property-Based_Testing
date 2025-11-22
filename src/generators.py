from typing import Callable, TypeVar, Generic, Any, List
from dataclasses import dataclass
import random
import string as string_module # Renombrado para evitar conflictos

T = TypeVar('T')

@dataclass(frozen=True)
class Generator(Generic[T]):
    generate: Callable[[random.Random, int], T]
    shrink: Callable[[T], List[T]]
    
    def map(self, fn: Callable[[T], Any]) -> 'Generator':
        def new_generate(rng: random.Random, size: int):
            return fn(self.generate(rng, size))
        def new_shrink(value):
            return [] 
        return Generator(new_generate, new_shrink)

# --- Generadores Primitivos ---

def integer(min_val: int = -100, max_val: int = 100) -> Generator[int]:
    def generate(rng: random.Random, size: int) -> int:
        return rng.randint(min_val, max_val)
    
    def shrink(value: int) -> List[int]:
        if value == 0: return []
        shrunk = [0, value // 2]
        if value > 0: shrunk.append(value - 1)
        if value < 0: shrunk.append(value + 1)
        return list(set(shrunk) - {value})
    return Generator(generate, shrink)

def float_val(min_val: float = -100.0, max_val: float = 100.0) -> Generator[float]:
    def generate(rng: random.Random, size: int) -> float:
        return rng.uniform(min_val, max_val)
    
    def shrink(value: float) -> List[float]:
        if abs(value) < 1e-5: return []
        return [0.0, value / 2.0]
    return Generator(generate, shrink)

def boolean() -> Generator[bool]:
    def generate(rng: random.Random, size: int) -> bool:
        return rng.choice([True, False])
    
    def shrink(value: bool) -> List[bool]:
        if value is True: return [False] # Shrink hacia "más simple" (Falso)
        return []
    return Generator(generate, shrink)

def string(min_length: int = 0, max_length: int = 20) -> Generator[str]:
    def generate(rng: random.Random, size: int) -> str:
        length = rng.randint(min_length, min(max_length, size))
        chars = string_module.ascii_letters + string_module.digits + ' '
        return ''.join(rng.choice(chars) for _ in range(length))
    
    def shrink(value: str) -> List[str]:
        if not value: return []
        return ['', value[:-1], value[1:]]
    return Generator(generate, shrink)

def list_of(element_gen: Generator[T], min_size: int = 0, max_size: int = 10) -> Generator[List[T]]:
    def generate(rng: random.Random, size: int) -> List[T]:
        length = rng.randint(min_size, min(max_size, size))
        return [element_gen.generate(rng, size) for _ in range(length)]
    
    def shrink(lst: List[T]) -> List[List[T]]:
        if not lst: return []
        shrunk = [[], lst[:len(lst)//2], lst[len(lst)//2:]]
        if len(lst) > 0:
            head = lst[0]
            for s_head in element_gen.shrink(head):
                shrunk.append([s_head] + lst[1:])
        return [s for s in shrunk if len(s) < len(lst) or (len(s)==len(lst) and s != lst)]
    return Generator(generate, shrink)