import random
from typing import List, Callable, TypeVar, Iterator

T = TypeVar('T')

# =========================================================
# 1. EL COMPONENTE SHRINKER
# =========================================================

class IntShrinker:
    """Implementa la lógica de reducción (shrinking) para el tipo 'int'."""
    
    @staticmethod
    def shrink(value: int) -> List[int]:
        """
        Genera una lista de enteros que son 'más simples' que el valor de entrada,
        priorizando valores cercanos a cero.
        """
        if value == 0:
            return []
        
        candidates = set()
        
        # Estrategia 1: Acercarse a cero (dividir por potencias de 2)
        i = 2
        while abs(value) // i >= 0 and i <= abs(value) * 2:
            candidate = value // i
            if candidate != value:
                 candidates.add(candidate)
            i *= 2
            
        # Estrategia 2: Probar valores frontera y cercanos
        candidates.add(0)
        candidates.add(1)
        candidates.add(-1)
        
        # Estrategia 3: Valor justo anterior/posterior (si es más simple)
        if abs(value - 1) < abs(value):
            candidates.add(value - 1)
        if abs(value + 1) < abs(value):
            candidates.add(value + 1)

        # Filtra y ordena por valor absoluto para probar lo más simple primero.
        return sorted(
            [c for c in candidates if abs(c) < abs(value) and c != value], 
            key=abs
        )

# =========================================================
# 2. EL BUCLE DE REDUCCIÓN EN EL PropTestRunner
# =========================================================

def run_property(
    prop: Callable[[int], bool],
    generator: Iterator[int], # Un generador que produce valores aleatorios
    shrinker: IntShrinker,
    runs: int = 100
):
    """
    Simulación del PropTestRunner: Ejecuta la propiedad y gestiona la reducción.
    """

    for run_count in range(runs):
        counter_example = next(generator)
        
        # 1. Probar el valor generado
        if not prop(counter_example):
            
            print(f" Fallo inicial en la corrida #{run_count+1} con: {counter_example}")
            minimal_counter_example = counter_example
            
            # 2. BUCLE PRINCIPAL DE SHRINKING (Semana Uno: Shrinking Simple)
            
            while True:
                # Obtener la lista de candidatos más simples
                shrunk_candidates = IntShrinker.shrink(minimal_counter_example)
                found_simpler_failing_case = False
                
                print(f"   Intentando reducir a partir de: {minimal_counter_example}")

                for candidate in shrunk_candidates:
                    # Probar cada candidato reducido
                    if not prop(candidate):
                        # Se encontró un caso más simple que aún falla.
                        minimal_counter_example = candidate
                        found_simpler_failing_case = True
                        print(f"   -> Shrink exitoso a: {minimal_counter_example}")
                        break # Romper el 'for' y reiniciar el 'while' con el nuevo caso
                        
                if not found_simpler_failing_case:
                    # Se ha llegado al contraejemplo más simple.
                    print("--- Proceso de Shrinking Terminado ---")
                    print(f" **Contraejemplo más simple y reproducible:** {minimal_counter_example}")
                    return 
                        
    print("Propiedad superada después de 100 corridas.")

# =========================================================
# 3. EJEMPLO DE USO
# =========================================================

# Generador de prueba
def gen_int_simple() -> Iterator[int]:
    while True:
        yield random.randint(-1000, 1000)

# Propiedad de prueba con un bug
def property_par_negativo(i: int) -> bool:
    # Falla si el número es -2.
    if i < 0 and i % 2 == 0:
        return i != -2 
    return True

# Ejecución
run_property(
    prop=property_par_negativo,
    generator=gen_int_simple(),
    shrinker=IntShrinker
)