# Importa las herramientas del framework
from src.generators import integer, list_of # Usaremos generadores para crear el contraejemplo inicial
from src.properties import property_test, forall # Decoradores (aunque no se usan directamente para shrink)
from src.shrinking import shrink_to_minimum # La función clave a probar

# Importa una herramienta para simular la ejecución de la prueba
import pytest 

# --- Código bajo prueba (Función con un fallo específico) ---
def procesar_listas(lst: list[int]) -> bool:
    """
    Función que falla intencionalmente SÓLO si la lista es [0].
    Cualquier otra lista ([1, 2], [0, 0], [1]) pasa.
    El contraejemplo mínimo es [0].
    """
    if lst == [0]:
        return False  # Este es el fallo
    return True

# --- Propiedad que falla (con un contraejemplo grande) ---
@forall(list_of(integer(min_value=0, max_value=10), min_size=1, max_size=10))
def prop_procesar_no_falla(lst):
    """Propiedad: 'procesar_listas' siempre retorna True."""
    return procesar_listas(lst)

# --- Test del Shrinker ---

def test_shrinking_finds_minimum_counterexample():
    """
    Verifica que el algoritmo de shrinking reduzca un contraejemplo
    complejo a su forma mínima ([0]).
    """
    
    # 1. Simulación del fallo
    # El framework genera un contraejemplo grande y lo pasa al shrinker.
    # Por ejemplo, el generador aleatorio podría haber encontrado el fallo con [5, 1, 0, 8, 3].
    # El último valor aleatorio que causó el fallo es el 'counterexample'.
    
    counterexample_grande = [5, 1, 0, 8, 3] 

    # 2. Definición del Test de Fallo (función de predicado)
    # El shrinker necesita una función que reciba una entrada y retorne True si FALLA.
    def is_failing(data):
        # La propiedad es que la función retorna True.
        # Por lo tanto, FALLA si retorna False.
        return not procesar_listas(data)

    # 3. Ejecución del Shrinker
    # Llama a la función principal de shrinking con la función de fallo y el contraejemplo.
    counterexample_minimo = shrink_to_minimum(
        is_failing, 
        counterexample_grande
    )
    
    # 4. Verificación
    # El resultado del shrinking debe ser el caso mínimo conocido: [0].
    expected_minimum = [0]
    
    assert counterexample_minimo == expected_minimum, \
        f" El Shrinker no encontró el mínimo. Se esperaba {expected_minimum}, pero se obtuvo {counterexample_minimo}"
        
    print(f" Shrinking exitoso: El contraejemplo {counterexample_grande} se redujo a {counterexample_minimo}")
    
def test_shrinking_on_integer_failure():
    """
    Verifica que el shrinking funcione en tipos de datos simples (enteros).
    Fallo: La función es incorrecta para n < 5. El mínimo esperado es 0 (o 5, dependiendo del rango).
    """
    
    def logica_con_bug(n):
        return n >= 5 # Falla si n es 0, 1, 2, 3 o 4
        
    def is_failing(n):
        return not logica_con_bug(n)

    # Simulación: el generador encontró el fallo con un número grande (ej: 3)
    counterexample_start = 3
    
    # El shrinker debe reducir 3 -> 2 -> 1 -> 0 (si el rango permite 0)
    counterexample_minimo = shrink_to_minimum(is_failing, counterexample_start)
    
    # El mínimo en este caso es 0 (el valor más pequeño del rango que falla)
    expected_minimum = 0
    
    assert counterexample_minimo == expected_minimum, \
        f" Shrinking de entero incorrecto. Esperado {expected_minimum}, obtenido {counterexample_minimo}"
