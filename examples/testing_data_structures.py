from hypothesis import given, strategies as st
import pytest

# Ejemplo simple: probar que una lista cuando la reviertes dos veces, obtienes la misma lista
@given(st.lists(st.integers()))
def test_reverse_reverse_identity(lst):
    assert list(reversed(list(reversed(lst)))) == lst

# Supongamos que tienes una implementación de Stack (pila)
class Stack:
    def __init__(self):
        self._data = []

    def push(self, x):
        self._data.append(x)

    def pop(self):
        return self._data.pop()

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

# Propiedad: si haces push y luego pop, obtienes lo que pusheaste
@given(st.integers())
def test_stack_push_pop(x):
    s = Stack()
    s.push(x)
    popped = s.pop()
    assert popped == x
    assert s.is_empty()

# Propiedad: el tamaño de la pila aumenta con push y disminuye con pop
@given(st.lists(st.integers()))
def test_stack_size(lst):
    s = Stack()
    initial_size = s.size()
    for x in lst:
        s.push(x)
    assert s.size() == initial_size + len(lst)
    for _ in lst:
        s.pop()
    assert s.size() == initial_size

# Si tienes un árbol (por ejemplo, un árbol binario de búsqueda), puedes probar invariantes:
class BSTNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def insert(self, x):
        if x <= self.value:
            if self.left:
                self.left.insert(x)
            else:
                self.left = BSTNode(x)
        else:
            if self.right:
                self.right.insert(x)
            else:
                self.right = BSTNode(x)

    def to_list(self):
        """Recorrido in-order que debe dar una lista ordenada."""
        result = []
        if self.left:
            result.extend(self.left.to_list())
        result.append(self.value)
        if self.right:
            result.extend(self.right.to_list())
        return result

@given(st.lists(st.integers()))
def test_bst_inorder_sorted(lst):
    if not lst:
        return
    root = BSTNode(lst[0])
    for x in lst[1:]:
        root.insert(x)
    inorder = root.to_list()
    assert inorder == sorted(lst)

