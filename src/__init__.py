# src/__init__.py

# 1. Importaciones de funcionalidades clave para un acceso directo y limpio
# -----------------------------------------------------------------------

# Desde generators.py
from .generators import Generator, integer, string, list_of, one_of, constant
# Desde properties.py
from .properties import TestResult, forall, property_test, run_tests
# Desde shrinking.py
from .shrinking import shrink_counterexample
# Desde mutation.py
from .mutation import MutationOperator, generate_mutants, mutation_score
# Desde combinators.py
from .combinators import tuple_of, one_of_values, recursive
# Desde strategies.py
from .strategies import quick_check, check_with_mutation, combine_tests

# 2. Función de Ejemplo Principal (para ejecutar el programa)
# -----------------------------------------------------------

def run_example_suite():
    """
    Ejecuta una suite de Property-Based Tests de ejemplo
    para demostrar el uso del framework.
    """
    print("\n=======================================================")
    print("🚀 Property-Based Testing (PBT) - Demostración de QuickCheck")
    print("=======================================================\n")
    
    # --- 1. Definir Generadores ---
    
    # Enteros positivos pequeños (0 a 100)
    gen_pos_int = integer(min_val=0, max_val=100) 
    
    # Listas de hasta 10 enteros positivos
    gen_list_int = list_of(gen_pos_int, min_size=0, max_size=10)

    # --- 2. Definir Propiedades (Tests) ---

    # Propiedad 1: Identidad al revertir dos veces (Debe pasar)
    @property_test
    @forall(gen_list_int)
    def test_reverse_twice_is_identity(lst):
        """Propiedad: list(reverse(reverse(x))) == x"""
        # Explicación: Revertir una lista dos veces debe devolver la lista original.
        return list(reversed(list(reversed(lst)))) == lst
    
    # Propiedad 2: Suma conmutativa (Debe pasar)
    @property_test
    @forall(gen_pos_int, gen_pos_int)
    def test_addition_commutative(a, b):
        """Propiedad: a + b == b + a"""
        # Explicación: El orden de los sumandos no altera la suma.
        return a + b == b + a

    # Propiedad 3: Una propiedad que FALLA para demostrar Shrinking
    def bad_sort(lst):
        """Una función intencionalmente defectuosa para demostrar el fallo."""
        if len(lst) > 1 and lst[0] > lst[1]:
             # Bug: Si el primer elemento es mayor al segundo, devuelve el original
             return lst
        return sorted(lst)

    @property_test
    @forall(gen_list_int)
    def test_bad_sort_is_sorted(lst):
        """Propiedad: El resultado de bad_sort debe estar ordenado."""
        # Esta prueba fallará con el bug de bad_sort, y el shrinking encontrará el contraejemplo mínimo.
        result = bad_sort(lst)
        # La propiedad es: para todo i, result[i] <= result[i+1]
        for i in range(len(result) - 1):
            if result[i] > result[i+1]:
                return False
        return True
    
    # --- 3. Ejecutar los Tests ---
    
    # Usamos la función de estrategia quick_check
    
    print("\n--- Ejecutando Propiedad 1: Reverse Twice (Éxito esperado) ---")
    quick_check(test_reverse_twice_is_identity) 
    
    print("\n--- Ejecutando Propiedad 3: Bad Sort (Fallo y Shrinking esperado) ---")
    quick_check(test_bad_sort_is_sorted)
    
    # Opcional: Ejecutar todos juntos con run_tests
    # run_tests(test_reverse_twice_is_identity, test_addition_commutative, test_bad_sort_is_sorted, num_tests=50)


# 3. Punto de Entrada
# -------------------

if __name__ == '__main__':
    # Esto permite ejecutar el proyecto directamente como: python src/__init__.py
    run_example_suite()
    