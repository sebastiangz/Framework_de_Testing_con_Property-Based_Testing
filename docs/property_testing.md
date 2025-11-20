# Property-Based Testing (PBT)

## 1. Introducción

El **Property-Based Testing (PBT)** es un enfoque de testing donde se definen **propiedades** que el código debe cumplir para *todos los valores posibles* generados automáticamente, en lugar de escribir tests para casos específicos.

Por ejemplo, en lugar de escribir:

```python
assert add(2, 3) == 5
```

podemos definir una propiedad general:

```python
a + b == b + a  # La suma es conmutativa
```

El framework generará automáticamente muchos valores y comprobará que la propiedad siempre se cumpla.

---

## 2. Conceptos Clave

* **Generadores (`Generator`)**: producen datos aleatorios de distintos tipos para probar las propiedades.
* **Propiedades (`Property`)**: funciones que deben devolver `True` para todos los valores válidos.
* **Shrinking**: cuando se encuentra un valor que falla, se reduce automáticamente a un caso más simple que siga fallando, ayudando a localizar el error.
* **Test Runner**: ejecuta repetidamente las propiedades, muestra resultados y aplica shrinking si hay fallos.

---

## 3. Ejemplo de Uso

```python
from src.generators import integer, list_of
from src.properties import property_test, forall

# Generador de listas de enteros
gen_list = list_of(integer(min_value=0, max_value=100), min_size=0, max_size=10)

# Definición de propiedad
@property_test
@forall(gen_list)
def test_reverse_twice_is_identity(lst):
    """Propiedad: revertir dos veces devuelve la lista original"""
    return list(reversed(list(reversed(lst)))) == lst

# Ejecutar property test
test_reverse_twice_is_identity()
```

**Explicación**:

* `gen_list` genera listas aleatorias de enteros.
* `@forall(gen_list)` indica que la función será probada con muchos valores generados.
* Si alguna lista falla, el framework aplica *shrinking* para encontrar la versión más simple que aún falle.

---

## 4. Ventajas

* Detecta errores que los tests manuales podrían no cubrir.
* Reduce el tiempo de escribir tests repetitivos.
* Shrinking permite diagnósticos más claros y reproducibles.

---

## 5. Buenas Prácticas

* Definir propiedades simples y puras, sin efectos secundarios.
* Componer generadores para cubrir distintos escenarios.
* Evitar depender de valores concretos, enfocarse en invariantes.
* Utilizar shrinking para comprender mejor los fallos.

---

## 6. Integración con el Framework

* Los generadores se encuentran en `src/generators.py`.
* Las propiedades se definen en `src/properties.py`.
* Shrinking se aplica desde `src/shrinking.py`.
* Tests completos pueden ejecutarse desde `run_framework.py` o los archivos en `tests/`.

---

Este documento sirve como guía para entender y aplicar property-based testing dentro del framework funcional que hemos implementado.
