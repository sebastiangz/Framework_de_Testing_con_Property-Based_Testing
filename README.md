# 🧪 Proyecto 10: Framework de Testing Funcional con Property-Based Testing

## NOMBRE COMPLETO DE INTEGRANTES 
- Maria Fernanda Alcaraz Morales (malcaraz41@ucol.mx)
- Jordan Adrián Miramontes Gutiérrez (Jmiramontes4@ucol.mx)
- Karol Said Preciado Castillo (Kpreciado6@ucol.mx) 

## 📋 Descripción del Proyecto

Framework completo de testing funcional que incluye generadores de datos aleatorios composables, property-based testing, shrinking de contraejemplos y mutation testing, todo implementado con programación funcional pura.

**Universidad de Colima - Ingeniería en Computación Inteligente**  
**Materia**: Programación Funcional  
**Profesor**: Gonzalez Zepeda Sebastian  
**Semestre**: Agosto 2025 - Enero 2026

---

## 🎯 Objetivos

- Implementar **generadores composables** de datos aleatorios
- Desarrollar **property-based testing** desde cero
- Aplicar **shrinking funcional** para minimizar contraejemplos
- Crear **mutation testing** funcional
- Utilizar **QuickCheck-style testing**
- Practicar **higher-order functions** para test composition

---

## Caracteristicas Principales 
- Generación Aleatoria de Casos:	El framework automáticamente genera casos de prueba aleatorios (incluyendo estructuras de datos complejas) basados en las especificaciones de entrada definidas para la propiedad. Esto automatiza la creación de tests.
- Simplificación (Shrinking): Cuando se encuentra un caso fallido, el framework intenta simplificar automáticamente el caso de prueba fallido a la versión más pequeña y legible posible, facilitando la depuración.

## Ejemplos de Uso 
1. Generación de Casos de Prueba Aleatorios y Memoria
Cuando un framework de PBT necesita probar una propiedad, como una función que ordena una lista, debe generar un gran volumen de listas de prueba.
Generación de Listas Infinitas de Datos de Prueba:	En lugar de crear una lista con 1 millón de tuplas de entrada y guardarla en memoria (ej: todas_las_listas = [generar_lista() for _ in range(1000000)]), el PBT usa un generador.
Ejemplo de Código (Conceptual):	casos_de_prueba = (generar_lista_aleatoria(tamanio_max) for _ in itertools.count())
El generador (casos_de_prueba) solo produce la lista siguiente justo antes de que se necesite para la prueba. Si el framework se detiene después de 10,000 pruebas exitosas, solo se crearon 10,000 listas, no 1 millón, ahorrando recursos masivamente.

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.11+
- **Paradigma**: Programación Funcional
- **Librerías**:
  - `hypothesis` - Property-based testing (referencia)
  - `ast` - Abstract Syntax Trees para mutation
  - `toolz` - Utilidades funcionales
  - `pytest` - Framework de testing
  - `typing` - Type hints avanzados

---

## REFERENCIAS IEEE/ACM 
- Claessen, K., & Hughes, J. (2000). QuickCheck: A lightweight tool for random testing 
of Haskell programs. In Proceedings of the ACM SIGPLAN International 
Conference on Functional Programming (pp. 268-279). ACM. 
https://doi.org/10.1145/351240.351266
- Pacheco, C., & Ernst, M. D. (2007). Randoop: Feedback-directed random testing in 
Java. In Companion to the 22nd ACM SIGPLAN Conference on Object-oriented 
Programming Systems and Applications (pp. 815-816).
- Jia, Y., & Harman, M. (2011). An analysis and survey of the development of mutation 
testing. IEEE Transactions on Software Engineering, 37(5), 649-678.

## EMPRENDIMIENTO 
- En nuestro proyecto queremos aumentaer la confiabilidad del software al validar automáticamente propiedades funcionales y tratar de disminuir costos en mantenimiento y depuración de código, Al igual que queremos tener impacto en la capacitación y certificaciones en testing automatizado y property-based testing y en marketplace de propiedades y generadores (venta de módulos específicos según dominio: finanzas, IoT, juegos). En nuestro proyecto tenemos destinado que nuestro objetivo en el cliente sea equipos de investigación o universidades que trabajan en validación de software y empresas nuevas que necesitan pruebas rápidas y automatizadas sin grandes recursos. 

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/functional-testing-framework.git
cd functional-testing-framework

# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### requirements.txt
```
hypothesis>=6.92.0
pytest>=7.4.0
toolz>=0.12.0
pytest-cov>=4.1.0
pytest-xdist>=3.5.0
typing-extensions>=4.8.0
```

---

## 🚀 Uso del Framework

```python
from src.generators import integer, string, list_of
from src.properties import property_test, forall
from src.shrinking import shrink

# Definir generadores
gen_positive_int = integer(min=1, max=100)
gen_string = string(min_length=0, max_length=20)
gen_list = list_of(gen_positive_int, min_size=0, max_size=10)

# Definir propiedades
@property_test
@forall(gen_list)
def test_reverse_twice_is_identity(lst):
    """Propiedad: reverse(reverse(x)) == x"""
    return list(reversed(list(reversed(lst)))) == lst

@property_test
@forall(gen_positive_int, gen_positive_int)
def test_addition_commutative(a, b):
    """Propiedad: a + b == b + a"""
    return a + b == b + a

# Ejecutar tests
test_reverse_twice_is_identity()  # Ejecuta 100 casos por defecto
test_addition_commutative()

# Si falla, automáticamente shrink el contraejemplo
```

---

## 📂 Estructura del Proyecto

```
functional-testing-framework/
├── FTest_Engine.py
├── src/
│   ├── __init__.py
│   ├── generators.py       # Generadores de datos
│   ├── properties.py       # Property-based testing
│   ├── shrinking.py        # Shrinking de contraejemplos
│   ├── mutation.py         # Mutation testing
│   ├── combinators.py      # Combinadores de generadores
│   └── strategies.py       # Estrategias de testing
├── tests/
│   ├── test_generators.py
│   ├── test_properties.py
│   ├── test_shrinking.py
│   └── test_mutation.py
│   ├── test_combinators.py    
│   └── test_strategies.py     
├── examples/
│   ├── testing_data_structures.py
│   ├── testing_algorithms.py
│   └── testing_parsers.py
├── docs/
│   ├── generator_guide.md
│   ├── property_testing.md
│   └── api_reference.md
├── requirements.txt
├── README.md
└── .gitignore
```

```
                          ┌────────────────────────────────────┐
                          │  Functional Testing Framework      │
                          └────────────────────────────────────┘
                                        │
      ┌──────────────────────────────────┼──────────────────────────────────────┐
      │                                  │                                      │
      ▼                                  ▼                                      ▼
┌─────────────┐                 ┌────────────────┐                    ┌─────────────────┐
│   src/      │                 │    tests/      │                    │    examples/    │
└─────────────┘                 └────────────────┘                    └─────────────────┘
      │                                  │                                      │
      │                                  │                                      │
      ▼                                  ▼                                      ▼
┌─────────────┐   ┌────────────────┐   ┌──────────────────┐       ┌─────────────────────────┐
│ generators  │   │ combinators    │   │ strategies       │       │ testing_data_structures │
└─────────────┘   └────────────────┘   └──────────────────┘       └─────────────────────────┘
      │                  │                    │
      │ (Generadores     │ (Composición       │ (Estrategias listas
      │  básicos)        │  funcional)        │  para usar)
      │                  │                    │
      │                  │                    │
      ▼                  ▼                    ▼
 ┌────────────────────────────────────────────────────────────────────────────┐
 │                           properties.py                                    │
 └────────────────────────────────────────────────────────────────────────────┘
      │
      │ (Define: forall, property_test, ejecución de tests,
      │          orquestación completa del framework)
      ▼
 ┌──────────────────────────────┐
 │        shrinking.py          │
 └──────────────────────────────┘
      │
      │ (Reduce contraejemplos: shrink)
      ▼
 ┌──────────────────────────────┐
 │         mutation.py          │
 └──────────────────────────────┘
      │
      │ (Mutation Testing: mutantes AST, mutation score)
      ▼
   Resultados finales
```



1. generators.py

Crea valores aleatorios y sabe cómo reducirlos.

Es la base de todo.

2. combinators.py

Combina generadores para crear generadores más complejos.

3. strategies.py

Usa generadores y combinadores para crear estrategias listas para usar.

4. properties.py

Toma estrategias/generadores y ejecuta tests repetidos.

Detecta fallos.

Llama al shrinker.

5. shrinking.py

Reduce valores que causan fallos.

6. mutation.py

Genera mutaciones del código a probar.

Reejecuta tests para medir fortaleza del test suite.

7. tests/

Contiene tests del propio framework.

8. examples/

Ejemplos de cómo usar el framework en la vida real.


---

## 🔑 Características Principales

### 1. Generadores Composables
```python
from typing import Callable, TypeVar, Generic, Any
from dataclasses import dataclass
import random

T = TypeVar('T')

@dataclass(frozen=True)
class Generator(Generic[T]):
    """Generador funcional de valores aleatorios"""
    generate: Callable[[random.Random, int], T]
    shrink: Callable[[T], list[T]]
    
    def map(self, fn: Callable[[T], Any]) -> 'Generator':
        """Functor map para generadores"""
        def new_generate(rng: random.Random, size: int):
            value = self.generate(rng, size)
            return fn(value)
        
        def new_shrink(value):
            # Shrink en el espacio original, luego mapear
            original = self.inverse_map(value)  # Simplificado
            return [fn(s) for s in self.shrink(original)]
        
        return Generator(new_generate, new_shrink)
    
    def filter(self, predicate: Callable[[T], bool]) -> 'Generator':
        """Filtrar valores generados"""
        def new_generate(rng: random.Random, size: int):
            max_attempts = 100
            for _ in range(max_attempts):
                value = self.generate(rng, size)
                if predicate(value):
                    return value
            raise ValueError("Could not generate valid value")
        
        return Generator(new_generate, self.shrink)
    
    def flat_map(self, fn: Callable[[T], 'Generator']) -> 'Generator':
        """Monad bind para generadores"""
        def new_generate(rng: random.Random, size: int):
            value = self.generate(rng, size)
            next_gen = fn(value)
            return next_gen.generate(rng, size)
        
        def new_shrink(value):
            # Shrinking para flat_map es complejo
            return []  # Simplificado
        
        return Generator(new_generate, new_shrink)

# Generadores básicos
def integer(min: int = -100, max: int = 100) -> Generator[int]:
    """Generador de enteros"""
    def generate(rng: random.Random, size: int) -> int:
        return rng.randint(min, max)
    
    def shrink(value: int) -> list[int]:
        """Shrink hacia 0"""
        if value == 0:
            return []
        
        shrunk = []
        # Shrink binario hacia 0
        half = value // 2
        if half != value:
            shrunk.append(half)
        if value > 0:
            shrunk.append(value - 1)
        elif value < 0:
            shrunk.append(value + 1)
        shrunk.append(0)
        
        return shrunk
    
    return Generator(generate, shrink)

def string(min_length: int = 0, max_length: int = 100) -> Generator[str]:
    """Generador de strings"""
    def generate(rng: random.Random, size: int) -> str:
        length = rng.randint(min_length, min(max_length, size))
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
        return ''.join(rng.choice(chars) for _ in range(length))
    
    def shrink(value: str) -> list[str]:
        """Shrink hacia string vacío"""
        if not value:
            return []
        
        shrunk = ['']  # String vacío
        
        # Remover caracteres
        if len(value) > 1:
            shrunk.append(value[:-1])  # Remover último
            shrunk.append(value[:len(value)//2])  # Mitad
        
        return shrunk
    
    return Generator(generate, shrink)

def list_of(element_gen: Generator[T], 
            min_size: int = 0,
            max_size: int = 100) -> Generator[list[T]]:
    """Generador de listas"""
    def generate(rng: random.Random, size: int) -> list[T]:
        length = rng.randint(min_size, min(max_size, size))
        return [element_gen.generate(rng, size) for _ in range(length)]
    
    def shrink(lst: list[T]) -> list[list[T]]:
        """Shrink lista"""
        if not lst:
            return []
        
        shrunk = []
        
        # Lista vacía
        shrunk.append([])
        
        # Remover un elemento a la vez
        for i in range(len(lst)):
            shrunk.append(lst[:i] + lst[i+1:])
        
        # Dividir por la mitad
        mid = len(lst) // 2
        if mid > 0:
            shrunk.append(lst[:mid])
            shrunk.append(lst[mid:])
        
        # Shrink elementos individuales
        for i in range(len(lst)):
            for shrunk_elem in element_gen.shrink(lst[i]):
                shrunk.append(lst[:i] + [shrunk_elem] + lst[i+1:])
        
        return shrunk
    
    return Generator(generate, shrink)
```

### 2. Property-Based Testing
```python
from typing import Callable, Any
from functools import wraps
import random

@dataclass(frozen=True)
class TestResult:
    """Resultado de un test de propiedad"""
    success: bool
    num_tests: int
    counterexample: Any = None
    shrunk_counterexample: Any = None
    
def forall(*generators: Generator):
    """Decorator para property-based tests"""
    def decorator(test_fn: Callable) -> Callable:
        @wraps(test_fn)
        def wrapper(num_tests: int = 100, seed: int = None):
            rng = random.Random(seed)
            
            for i in range(num_tests):
                # Generar valores
                size = min(i, 100)  # Aumentar tamaño gradualmente
                values = tuple(
                    gen.generate(rng, size)
                    for gen in generators
                )
                
                # Ejecutar test
                try:
                    result = test_fn(*values)
                    if not result:
                        # Falló - shrink contraejemplo
                        shrunk = shrink_counterexample(
                            values,
                            generators,
                            test_fn
                        )
                        return TestResult(
                            success=False,
                            num_tests=i + 1,
                            counterexample=values,
                            shrunk_counterexample=shrunk
                        )
                except Exception as e:
                    # Excepción - también shrink
                    shrunk = shrink_counterexample(
                        values,
                        generators,
                        test_fn
                    )
                    return TestResult(
                        success=False,
                        num_tests=i + 1,
                        counterexample=values,
                        shrunk_counterexample=shrunk
                    )
            
            return TestResult(success=True, num_tests=num_tests)
        
        return wrapper
    return decorator

def property_test(fn: Callable) -> Callable:
    """Decorator para marcar property tests"""
    fn._is_property_test = True
    return fn
```

### 3. Shrinking Funcional
```python
def shrink_counterexample(
    values: tuple,
    generators: tuple[Generator, ...],
    test_fn: Callable
) -> tuple:
    """Shrink contraejemplo al mínimo"""
    current = values
    
    while True:
        # Intentar shrink de cada valor
        shrunk_any = False
        
        for i, (value, gen) in enumerate(zip(current, generators)):
            for shrunk_value in gen.shrink(value):
                # Probar con valor shrinked
                test_values = current[:i] + (shrunk_value,) + current[i+1:]
                
                # Ver si todavía falla
                try:
                    result = test_fn(*test_values)
                    still_fails = not result
                except:
                    still_fails = True
                
                if still_fails:
                    # Aceptar shrink
                    current = test_values
                    shrunk_any = True
                    break
            
            if shrunk_any:
                break
        
        if not shrunk_any:
            break
    
    return current
```

### 4. Mutation Testing
```python
import ast
from typing import List, Callable

class MutationOperator:
    """Operador de mutación funcional"""
    
    @staticmethod
    def arithmetic_mutations(node: ast.BinOp) -> List[ast.BinOp]:
        """Mutar operadores aritméticos"""
        mutations = []
        
        operators = {
            ast.Add: [ast.Sub, ast.Mult],
            ast.Sub: [ast.Add, ast.Div],
            ast.Mult: [ast.Add, ast.Div],
            ast.Div: [ast.Mult, ast.Sub]
        }
        
        op_type = type(node.op)
        if op_type in operators:
            for new_op in operators[op_type]:
                mutated = ast.copy_location(
                    ast.BinOp(node.left, new_op(), node.right),
                    node
                )
                mutations.append(mutated)
        
        return mutations
    
    @staticmethod
    def comparison_mutations(node: ast.Compare) -> List[ast.Compare]:
        """Mutar operadores de comparación"""
        mutations = []
        
        operators = {
            ast.Eq: [ast.NotEq],
            ast.NotEq: [ast.Eq],
            ast.Lt: [ast.LtE, ast.Gt],
            ast.LtE: [ast.Lt, ast.GtE],
            ast.Gt: [ast.GtE, ast.Lt],
            ast.GtE: [ast.Gt, ast.LtE]
        }
        
        for i, op in enumerate(node.ops):
            op_type = type(op)
            if op_type in operators:
                for new_op in operators[op_type]:
                    new_ops = node.ops[:i] + [new_op()] + node.ops[i+1:]
                    mutated = ast.copy_location(
                        ast.Compare(node.left, new_ops, node.comparators),
                        node
                    )
                    mutations.append(mutated)
        
        return mutations

def generate_mutants(source_code: str) -> List[str]:
    """Generar mutantes del código"""
    tree = ast.parse(source_code)
    mutants = []
    
    class MutationVisitor(ast.NodeVisitor):
        def visit_BinOp(self, node):
            for mutation in MutationOperator.arithmetic_mutations(node):
                mutated_tree = tree  # Clonar y mutar
                mutants.append(ast.unparse(mutated_tree))
            self.generic_visit(node)
        
        def visit_Compare(self, node):
            for mutation in MutationOperator.comparison_mutations(node):
                mutated_tree = tree  # Clonar y mutar
                mutants.append(ast.unparse(mutated_tree))
            self.generic_visit(node)
    
    visitor = MutationVisitor()
    visitor.visit(tree)
    
    return mutants

def mutation_score(
    original_code: str,
    test_suite: Callable
) -> float:
    """Calcular mutation score"""
    mutants = generate_mutants(original_code)
    killed = 0
    
    for mutant_code in mutants:
        # Ejecutar tests contra mutante
        try:
            exec(mutant_code)
            test_suite()
            # Mutante sobrevivió
        except:
            # Mutante fue matado
            killed += 1
    
    return killed / len(mutants) if mutants else 1.0
```

---

## 📊 Funcionalidades Implementadas

### Generadores
- ✅ Primitivos (int, float, bool, string)
- ✅ Colecciones (list, dict, set, tuple)
- ✅ Custom types
- ✅ Recursive generators
- ✅ Combinadores (map, filter, flat_map)

### Property Testing
- ✅ forall decorator
- ✅ Automatic test case generation
- ✅ Shrinking de contraejemplos
- ✅ Statistical testing
- ✅ Regression testing

### Mutation Testing
- ✅ Arithmetic operators
- ✅ Comparison operators
- ✅ Boolean operators
- ✅ Statement mutations
- ✅ Mutation score calculation

### Integración
- ✅ Pytest integration
- ✅ CI/CD support
- ✅ Coverage reports
- ✅ Performance benchmarks

---

## 🧪 Testing

```bash
# Ejecutar framework tests
pytest tests/ -v

# Tests con property-based testing
pytest tests/test_properties.py

# Mutation testing del framework mismo
python -m src.mutation tests/

# Benchmarks
pytest tests/test_performance.py --benchmark
```

---

## 📈 Pipeline de Desarrollo

### Semana 1: Generadores (30 Oct - 5 Nov)
- Generadores básicos
- Combinadores
- Shrinking simple

### Semana 2: Property Testing (6 Nov - 12 Nov)
- forall decorator
- Test runner
- Shrinking avanzado

### Semana 3: Mutation Testing (13 Nov - 19 Nov)
- AST mutations
- Mutation score
- Reportes completos

---

## 💼 Componente de Emprendimiento

**Aplicación Real**: Framework de testing para empresas de software

**Propuesta de Valor**:
- Detección automática de bugs edge-case
- Reducción de 60% en bugs de producción
- Mutation testing para medir calidad de tests
- Integración simple con CI/CD

**Modelo de Negocio**: Open-core + Enterprise features

---

## 📚 Referencias

- Claessen, K., & Hughes, J. (2000). *QuickCheck: A Lightweight Tool for Random Testing*
- **Hypothesis**: https://hypothesis.readthedocs.io/
- **pytest**: https://docs.pytest.org/
- Mutation Testing papers

---

## 🏆 Criterios de Evaluación

- **Generadores (25%)**: Composición funcional, diversidad de datos
- **Property-Based Testing (30%)**: Propiedades bien definidas, estrategias efectivas
- **Shrinking y Mutation (25%)**: Minimización efectiva, cobertura mutacional
- **Framework y Documentación (20%)**: API usable, ejemplos claros, integración

---

## 👥 Autor

**Nombre**: [Maria Fernanda Alcaraz Morales]  
**Email**: [malcaraz41@ucol.mx]  
**GitHub**: [FerAlcaraz](https://github.com/)

**Nombre**: [Karol Said Preciado Castillo]  
**Email**: [kpreciado6@ucol.mx]  
**GitHub**: [k4rolPr3ciado](https://github.com/k4rolPr3ciado)
---

## 📄 Licencia

Proyecto académico - Universidad de Colima © 2025


