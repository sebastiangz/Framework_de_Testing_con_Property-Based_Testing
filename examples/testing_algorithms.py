from hypothesis import given, strategies as st
import pytest

# Ejemplo de algoritmo: una función de ordenamiento (bubble sort, quick sort, lo que sea)
def my_sort(xs):
    # por simplicidad, usar el sort de python
    return sorted(xs)

@given(st.lists(st.integers()))
def test_sort_preserves_multiset(xs):
    sorted_xs = my_sort(xs)
    # la propiedad es que los elementos en la lista ordenada son los mismos que en la original (multiconjunto)
    assert sorted(xs) == sorted_xs
    # también debe estar ordenado
    assert all(sorted_xs[i] <= sorted_xs[i + 1] for i in range(len(sorted_xs) - 1))

# Algoritmo de búsqueda: búsqueda binaria sobre una lista ordenada
def binary_search(xs, target):
    lo, hi = 0, len(xs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if xs[mid] == target:
            return mid
        elif xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

@given(st.lists(st.integers()), st.integers())
def test_binary_search(xs, target):
    xs_sorted = sorted(xs)
    idx = binary_search(xs_sorted, target)
    if idx == -1:
        # si no lo encuentra, asegurarse de que en realidad no está
        assert target not in xs_sorted
    else:
        assert xs_sorted[idx] == target

# Algoritmo más complejo: por ejemplo, cálculo de máximo común divisor
def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

@given(st.integers(min_value=-1000, max_value=1000), st.integers(min_value=-1000, max_value=1000))
def test_gcd_properties(a, b):
    if a == 0 and b == 0:
        # gcd(0, 0) podría no estar definido, saltar
        return
    g = gcd(a, b)
    # Propiedad: g divide a y b
    assert a % g == 0
    assert b % g == 0
    # Propiedad: si divides a y b por g, ya no tienen otro divisor común > 1 (es el máximo)
    # No es trivial de testear con PBT, pero podrías comprobar que no hay un divisor más grande:
    for d in range(1, abs(min(a, b)) + 2):
        if a % d == 0 and b % d == 0:
            assert d <= abs(g)

