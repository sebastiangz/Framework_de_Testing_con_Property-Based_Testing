# Referencia de API  
Listado de las funciones, clases y estructuras más importantes del framework.

---
1. Módulo `generators`

### Clase Base: `Generator`
Métodos:
- `generate(rnd=None)` – produce un valor.
- `shrink(value)` – devuelve iterables de valores más simples.

### Generadores Primitivos
| Función | Descripción |
|--------|-------------|
| `integers(min_value=None, max_value=None)` | Genera enteros. |
| `floats(min_value=None, max_value=None, allow_nan=False)` | Genera flotantes. |
| `booleans()` | Genera booleanos. |
| `characters(allowed=None)` | Genera caracteres. |
| `strings(alphabet=None, min_length=0, max_length=20)` | Genera cadenas. |

### Generadores de Estructuras
| Función | Descripción |
|--------|-------------|
| `lists(g, min_length=0, max_length=10)` | Genera listas. |
| `sets(g, min_length=0, max_length=10)` | Genera sets. |
| `tuples(*generators)` | Genera tuplas. |

---

## 2. Módulo `combinators`

### `one_of(*generators)`
Elige un generador aleatoriamente.

### `map(generator, f)`
Transformación funcional de resultados.

### `filter(generator, predicate)`
Filtra los valores generados.

### `flatmap(generator, f)`
Permite dependencias entre generadores.

---

## 3. Módulo `properties`

### `@property_test`
Decorador principal para definir propiedades.

### `forall(generator)`
Asocia un generador a una propiedad.

### `check(property, num_tests=100)`
Ejecuta una propiedad repetidamente.

---

## 4. Módulo `shrinking`

### `shrink_integer(value)`
Reglas de reducción para enteros.

### `shrink_list(value)`
Reducción estructural para listas.

### `shrink_custom(generator, value)`
Punto de extensión para shrinking personalizado.

---

## 5. Módulo `mutation`

### `mutate_function(func)`
Genera mutaciones simples del código para mutation testing.

### `run_mutation_tests(func, tests)`
Evalúa si las pruebas detectan mutaciones.

---

## 6. Módulo `strategies`

### `strategy(generator, condition)`
Combina generadores con filtros.

### `bounded(generator, max_attempts)`
Limita reintentos para generadores filtrados.

---

## 7. Ejemplo Rápido

```python
from functional_testing_framework import properties, generators as g

@properties.property_test
@properties.forall(g.integers(0, 100))
def test_reverse_involution(x):
    assert list(reversed(list(reversed([x])))) == [x]
