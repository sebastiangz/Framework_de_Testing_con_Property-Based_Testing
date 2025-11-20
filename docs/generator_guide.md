# Guía de Generadores - Framework de Testing

## Introducción

Los generadores son el componente fundamental para crear datos de prueba en property-based testing. Esta guía explica cómo usar y crear generadores efectivos.

## Generadores Básicos

### Tipos Primitivos

```python
from src.generators import integers, floats, booleans, strings, characters

# Enteros en un rango
int_gen = integers(min_value=0, max_value=100)

# Floats con precisión
float_gen = floats(min_value=0.0, max_value=1.0)

# Booleanos
bool_gen = booleans()

# Strings y caracteres
string_gen = strings(min_length=1, max_length=10)
char_gen = characters()


`Colecciones`
from src.generators import lists, tuples, dictionaries

# Listas de enteros
list_gen = lists(integers(), min_length=0, max_length=5)

# Tuplas heterogéneas
tuple_gen = tuples(integers(), strings(), booleans())

# Diccionarios
dict_gen = dictionaries(
    keys=strings(min_length=1, max_length=5),
    values=integers()
)

"Combinadores Avanzados"
from src.combinators import one_of, frequency, map, filter, bind

# Elegir entre múltiples generadores
choice_gen = one_of([integers(), strings(), booleans()])

# Con diferentes probabilidades
weighted_gen = frequency([
    (5, integers()),      # 50% probabilidad
    (3, strings()),       # 30% probabilidad  
    (2, booleans())       # 20% probabilidad
])

# Transformar valores
squared_gen = map(lambda x: x * x, integers())

# Filtrar valores
positive_gen = filter(lambda x: x > 0, integers())

# Generadores dependientes
complex_gen = bind(integers(), lambda n: 
                  lists(integers(), min_length=n, max_length=n))


"Generadores personalizados"
from src.generators import Generator
import random

def emails():
    """Generador de emails válidos"""
    return map(
        lambda pair: f"{pair[0]}@{pair[1]}.com",
        tuples(
            strings(min_length=1, max_length=8),
            one_of([constant("gmail"), constant("hotmail"), constant("yahoo")])
        )
    )

def dates():
    """Generador de fechas válidas"""
    return map(
        lambda triple: f"{triple[0]:02d}/{triple[1]:02d}/{triple[2]}",
        tuples(
            integers(min_value=1, max_value=31),  # día
            integers(min_value=1, max_value=12),  # mes
            integers(min_value=2000, max_value=2023)  # año
        )
    )

"Mejor practica-Generadores reutilizables"
# En un módulo shared_generators.py
positive_ints = filter(lambda x: x > 0, integers())
non_empty_strings = filter(lambda s: len(s) > 0, strings())
valid_emails = emails()  # Definido anteriormente