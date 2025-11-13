import random
from typing import List, Callable, TypeVar, Iterator, Generic, Optional

T = TypeVar('T')
U = TypeVar('U')

# =========================================================
# 1. INTERFACES Y SHRINKER SIMPLE (SEMANA 1)
# =========================================================

class Shrinker(Generic[T]):
    """Define la interfaz para cualquier reductor."""
    def shrink(self, value: T) -> List[T]:
        raise NotImplementedError

class IntShrinker(Shrinker[int]):
    """Implementación del Shrinking Simple para enteros."""
    def shrink(self, value: int) -> List[int]:
        if value == 0:
            return []
        
        candidates = set()
        
        # Estrategias: Acercarse a cero
        i = 2
        while abs(value) // i >= 0 and i <= abs(value) * 2:
            candidates.add(value // i)
            i *= 2
            
        candidates.add(0)
        candidates.add(1)
        candidates.add(-1)
        if abs(value - 1) < abs(value): candidates.add(value - 1)

        return sorted(
            [c for c in candidates if abs(c) < abs(value) and c != value], 
            key=abs
        )

# =========================================================
# 2. SHRINKER AVANZADO (SEMANA 2)
# =========================================================

class ListShrinker(Shrinker[List[T]]):
    """
    Implementación del Shrinking Avanzado para listas.
    Combina reducción estructural y reducción de valores internos.
    """
    def __init__(self, element_shrinker: Shrinker[T]):
        self.element_shrinker = element_shrinker

    def shrink(self, value: List[T]) -> List[List[T]]:
        candidates = []
        
        # Estrategia A: Reducción Estructural (Eliminar elementos)
        for i in range(len(value) - 1, -1, -1):
             candidates.append(value[:i] + value[i+1:])
             
        if len(value) > 1:
            candidates.append(value[:len(value)//2])
        
        # Estrategia B: Reducción de Valores Internos
        for i, element in enumerate(value):
            shrunk_elements = self.element_shrinker.shrink(element)
            
            for shrunk_e in shrunk_elements:
                new_list = list(value)
                new_list[i] = shrunk_e
                candidates.append(new_list)

        # Eliminar duplicados y el valor original
        unique_candidates = []
        seen = set()
        for c in candidates:
            c_tuple = tuple(c)
            if c_tuple not in seen:
                seen.add(c_tuple)
                if c != value:
                    unique_candidates.append(c)

        return sorted(unique_candidates, key=lambda lst: (len(lst), lst))

# =========================================================
# 3. RUNNER Y EJEMPLO DE USO (INTEGRADO)
# =========================================================

def gen_list_of_ints(min_len=0, max_len=10) -> Iterator[List[int]]:
    """Generador simple para listas de enteros."""
    while True:
        length = random.randint(min_len, max_len)
        yield [random.randint(-100, 100) for _ in range(length)]

def property_test_no_ones(lst: List[int]) -> bool:
    """Propiedad de ejemplo que falla si la lista contiene el número '1'."""
    if 1 in lst:
        return False
    return True

def run_property(
    prop: Callable[[T], bool],
    generator: Iterator[T],
    shrinker: Shrinker[T],
    runs: int = 100
):
    """Ejecuta la propiedad y gestiona la reducción usando el Shrinker genérico."""
    
    for run_count in range(runs):
        counter_example = next(generator)
        if not prop(counter_example):
            print(f"Fallo inicial en la corrida #{run_count+1} con: {counter_example}")
            minimal_counter_example = counter_example
            
            # Bucle de shrinking
            while True:
                shrunk_candidates = shrinker.shrink(minimal_counter_example)
                found_simpler_failing_case = False
                
                for candidate in shrunk_candidates:
                    if not prop(candidate):
                        minimal_counter_example = candidate
                        found_simpler_failing_case = True
                        print(f"   -> Shrink exitoso a: {minimal_counter_example}")
                        break
                        
                if not found_simpler_failing_case:
                    print(f" Contraejemplo más simple y reproducible: {minimal_counter_example}")
                    return 
    
    print(" Propiedad superada después de 100 corridas.")

# =========================================================
# 4. EJECUCIÓN
# =========================================================

if __name__ == "__main__":
    # 1. Crear el shrinker base (Semana 1)
    int_shrinker = IntShrinker()
    
    # 2. Componer el shrinker avanzado (Semana 2)
    list_int_shrinker = ListShrinker(element_shrinker=int_shrinker)

    print("Iniciando prueba de Shrinking Avanzado (Semana 2)...")
    
    # 3. Ejecutar la propiedad
    run_property(
        prop=property_test_no_ones,
        generator=gen_list_of_ints(),
        shrinker=list_int_shrinker
    )