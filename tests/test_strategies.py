# Importa las funciones clave del framework
from src.generators import integer, list_of, string
from src.properties import property_test, forall

# --- Generadores de Datos (Estrategias) ---
# Definimos los 'Strategies' que generarán datos aleatorios para nuestras pruebas.

# 1. Estrategia para números enteros positivos
gen_pos_int = integer(min_value=1, max_value=100)

# 2. Estrategia para listas de enteros pequeños (incluyendo la lista vacía)
gen_small_list = list_of(integer(min_value=0, max_value=10), min_size=0, max_size=5)

# 3. Estrategia para cadenas de texto (incluyendo la cadena vacía)
gen_text = string(min_length=0, max_length=25)


# --- Pruebas de Propiedad ---

@property_test  # Decorador para indicar que esta es una prueba de propiedad
@forall(gen_pos_int, gen_pos_int)  # Aplica la estrategia a los argumentos de la función
def test_multiplication_associativity(a, b):
    """
    Propiedad: La multiplicación de números enteros es asociativa (a * b) == (b * a).
    
    El framework generará miles de pares (a, b) usando gen_pos_int
    y validará que esta propiedad SIEMPRE se cumpla.
    """
    assert (a * b) == (b * a), f"Fallo con a={a}, b={b}"


@property_test
@forall(gen_small_list)
def test_list_length_is_preserved_by_sorting(lst):
    """
    Propiedad: Ordenar una lista no debe cambiar su longitud.

    El framework generará miles de listas 'lst' usando gen_small_list
    y verificará que la longitud inicial sea igual a la longitud después de ordenarse.
    """
    original_length = len(lst)
    sorted_lst = sorted(lst)
    
    # Esta es una propiedad fundamental que debe ser cierta
    assert len(sorted_lst) == original_length, f"Fallo: Lista original {lst} tenía longitud {original_length}, la ordenada tiene {len(sorted_lst)}"


@property_test
@forall(gen_text)
def test_string_reversal_inversion(s):
    """
    Propiedad: Revertir una cadena dos veces debe dar como resultado la cadena original.
    """
    reversed_once = s[::-1]
    reversed_twice = reversed_once[::-1]
    
    # Verifica el invariant
    assert reversed_twice == s, f"Fallo con cadena '{s}'"

# --- Ejecución (Típicamente con pytest) ---

# Para ejecutar estas pruebas, si estás usando 'pytest', solo necesitarías correr:
# $ pytest tests/test_strategies.py
