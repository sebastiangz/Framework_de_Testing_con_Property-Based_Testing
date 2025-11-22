from typing import Callable, TypeVar, Generic, Any
from dataclasses import dataclass
import random
import itertools

# Define un TypeVar para la estructura del dato generado
T = TypeVar('T')

@dataclass(frozen=True)
class Generator(Generic[T]):
    """
    Estructura de datos inmutable que representa un Generador.
    Contiene la lógica para generar valores aleatorios y para reducir/simplificar un valor.
    """
    # 1. Función de generación: Toma un estado aleatorio (rng) y un tamaño (size)
    generate: Callable[[random.Random, int], T]
    # 2. Función de shrinking: Toma un valor (T) y retorna una lista de valores más simples
    shrink: Callable[[T], list[T]]
    
    def map(self, fn: Callable[[T], Any]) -> 'Generator':
        """Functor map: Transforma el valor generado, manteniendo la lógica de shrinking."""
        def new_generate(rng: random.Random, size: int):
            return fn(self.generate(rng, size))
        
        def new_shrink(value):
            # Shrink en el espacio original, luego mapear la función de transformación
            # Esta implementación funcional es compleja y se omite por simplicidad
            # La mayoría de los frameworks PBT solo aplican map a la generación
            # y esperan que el shrinker maneje el tipo transformado o un tipo base.
            return self.shrink(value) # Simplificado para este ejemplo
        
        return Generator(new_generate, new_shrink)

# --- Generadores Base ---

def integer(min_value: int, max_value: int) -> Generator[int]:
    """Generador de números enteros dentro de un rango."""
    
    def generate_int(rng: random.Random, size: int) -> int:
        # Usamos el tamaño como pista para favorecer valores cercanos a los límites
        return rng.randint(min_value, max_value)
    
    def shrink_int(n: int) -> list[int]:
        if n == 0:
            return []
        
        # Estrategias de shrinking para enteros: acercarse a 0 y 1
        return list(itertools.chain(
            # 1. La mitad del valor (acercarse a 0)
            [n // 2] if abs(n) > 1 and n // 2 != 0 else [],
            # 2. Moverse hacia 0
            [0] if n != 0 else [],
            # 3. Moverse hacia 1 o -1
            [1] if n > 1 else ([-1] if n < -1 else [])
        ))
    
    return Generator(generate_int, shrink_int)

def boolean() -> Generator[bool]:
    """Generador de valores booleanos (True o False)."""
    
    def generate_bool(rng: random.Random, size: int) -> bool:
        return rng.choice([True, False])
    
    def shrink_bool(b: bool) -> list[bool]:
        # El booleano tiene un espacio de shrinking trivial
        return [False] if b is True else [] # False es el valor "más simple"
        
    return Generator(generate_bool, shrink_bool)

# --- Generadores Compuestos (Combinadores) ---

def list_of(element_gen: Generator[T], min_size: int = 0, max_size: int = 10) -> Generator[list[T]]:
    """Generador de listas que usa otro generador para sus elementos."""
    
    def generate_list(rng: random.Random, size: int) -> list[T]:
        # Ajusta el tamaño real de la lista
        list_size = rng.randint(min_size, min(max_size, size))
        
        # Genera los elementos
        return [element_gen.generate(rng, size) for _ in range(list_size)]
    
    def shrink_list(lst: list[T]) -> list[list[T]]:
        # Estrategias de shrinking para listas:
        shrunken_lists = []
        
        # 1. Eliminar un elemento (recursión para simplificar la longitud)
        for i in range(len(lst)):
            shrunken_lists.append(lst[:i] + lst[i+1:])
            
        # 2. Shrink de los elementos internos (recursión para simplificar el contenido)
        for i, element in enumerate(lst):
            for shrunken_element in element_gen.shrink(element):
                new_list = list(lst)
                new_list[i] = shrunken_element
                shrunken_lists.append(new_list)
        
        # 3. Listas base (la lista vacía es la más simple)
        if lst:
            shrunken_lists.append([])
            
        # Retorna solo las listas únicas y que respeten el min_size
        return list(set(tuple(l) for l in shrunken_lists if len(l) >= min_size))
        
    return Generator(generate_list, shrink_list)

def sampled_from(options: list[T]) -> Generator[T]:
    """Generador que elige un elemento de una lista de opciones finitas."""
    
    def generate_sampled(rng: random.Random, size: int) -> T:
        return rng.choice(options)
    
    def shrink_sampled(value: T) -> list[T]:
        # Shrinking simple: si el valor es complejo, intenta reducirlo a los primeros elementos
        try:
            # Si el valor está en las opciones, el más simple es el primero
            if value in options and options[0] != value:
                return [options[0]]
        except:
            # Manejo de casos donde 'in' falla (ej: tipos no hasheables)
            pass
        return []
        
    return Generator(generate_sampled, shrink_sampled)


# --- Ejemplo de Uso (para la consola) ---

if __name__ == '__main__':
    # Creamos un generador de listas de booleanos
    gen_list_bool = list_of(boolean(), min_size=1, max_size=5)
    rng_state = random.Random()
    
    # Generar algunos ejemplos
    print("--- Ejemplos de Generación ---")
    for _ in range(3):
        print(f"Generado: {gen_list_bool.generate(rng_state, 10)}")

    # Probar el Shrinking
    print("\n--- Ejemplo de Shrinking ---")
    
    # 1. Shrinking de entero
    fallo_int = 10
    print(f"Shrink de {fallo_int}: {integer(0, 100).shrink(fallo_int)}") # [5, 0, 1]
    
    # 2. Shrinking de lista (el framework intentará reducir la lista y sus elementos)
    fallo_list = [True, True, False]
    shrunken = list_of(boolean()).shrink(fallo_list)
    print(f"Shrink de {fallo_list}:")
    for item in shrunken:
        print(f"  - {item}") 
    # El resultado debe incluir: [], [True, True], [True, False], [False, False], etc.
    