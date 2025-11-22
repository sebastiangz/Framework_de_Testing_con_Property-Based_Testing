"""
Functional Testing Framework
---------------------------
"""

# 1. Core Generators
from .generators import (
    Generator,
    integer,
    float_val,
    boolean,
    string,
    list_of
)

# 2. Combinators & Strategies
from .combinators import one_of, tuple_of, map2
from .strategies import (
    small_ints, 
    positive_ints, 
    emails,
    one_of_str_int
)

# 3. Testing Core
from .properties import property_test, forall, TestResult
from .shrinking import shrink_counterexample
from .mutation import mutation_score

# 4. Exports
__all__ = [
    # Generadores
    'Generator', 'integer', 'float_val', 'boolean', 'string', 'list_of',
    # Combinadores y Estrategias
    'one_of', 'tuple_of', 'map2',
    'small_ints', 'positive_ints', 'emails', 'one_of_str_int',
    # Testing
    'property_test', 'forall', 'TestResult',
    'mutation_score'
]

def run_demo():
    """Ejecuta una demostración rápida del sistema."""
    print("🧪 Ejecutando Demo del Framework...")
    
    # Caso 1: Property Test
    print("\n1. Test de Propiedad: reverse(reverse(s)) == s")
    gen_s = string()
    
    @property_test
    @forall(gen_s)
    def double_reverse(s):
        return s[::-1][::-1] == s
    
    res = double_reverse()
    print(f"Resultado: {'✅ Pasó' if res.success else '❌ Falló'}")

    # Caso 2: Estrategia de Email
    print("\n2. Generando Emails de prueba:")
    gen_email = emails()
    import random
    rng = random.Random(42)
    for _ in range(3):
        print(f" - {gen_email.generate(rng, 10)}")

    print("\nFramework listo.")