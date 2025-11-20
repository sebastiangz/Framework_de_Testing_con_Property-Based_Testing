"""
test_shrinking.py
-----------------
Pruebas unitarias para la funcionalidad de shrinking.
Incluye IntShrinker y ListShrinker.
Cada prueba verifica que los valores generados por shrink sean válidos y más simples que los originales.
"""

import random
from src.shrinking import IntShrinker, ListShrinker

def test_int_shrinker():
    """
    Prueba que IntShrinker reduzca correctamente los enteros.
    Verifica que los valores shrinked sean menores en magnitud que el original.
    """
    shrinker = IntShrinker()
    test_values = [100, -50, 1, -1]
    for val in test_values:
        shrunk = shrinker.shrink(val)
        for s in shrunk:
            assert abs(s) < abs(val), f"Shrink produjo valor inválido: {s} para {val}"
    print("test_int_shrinker passed")

def test_list_shrinker():
    """
    Prueba que ListShrinker reduzca correctamente listas de enteros.
    Verifica:
    - Las listas shrinked no sean idénticas a la original
    - Todos los elementos sean enteros
    """
    int_shrinker = IntShrinker()              # Shrinker para elementos individuales
    list_shrinker = ListShrinker(int_shrinker)  # Shrinker para listas de enteros

    test_lists = [ [5, 3, 1], [100, -50], [], [1, 2, 3, 4] ]
    for lst in test_lists:
        shrunk_lists = list_shrinker.shrink(lst)
        for sl in shrunk_lists:
            assert sl != lst, f"Shrink no modificó la lista: {sl}"
            assert all(isinstance(x, int) for x in sl), f"Elemento no entero: {sl}"
    print("test_list_shrinker passed")

if __name__ == '__main__':
    # Ejecuta los tests si se corre directamente
    test_int_shrinker()
    test_list_shrinker()
