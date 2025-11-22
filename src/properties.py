from typing import Callable, Any, Tuple
from functools import wraps
import random
from dataclasses import dataclass
from .generators import Generator
# Asegúrate de que shrinking.py también exista, ya que lo importamos aquí:
from .shrinking import shrink_counterexample 

@dataclass(frozen=True)
class TestResult:
    success: bool
    num_tests: int
    counterexample: Any = None
    shrunk_counterexample: Any = None

def forall(*generators: Generator):
    """Decorador que ejecuta la función de prueba múltiples veces con datos aleatorios."""
    def decorator(test_fn: Callable) -> Callable:
        @wraps(test_fn)
        def wrapper(num_tests: int = 100, seed: int = None) -> TestResult:
            rng = random.Random(seed)
            
            for i in range(num_tests):
                # Tamaño dinámico: empezamos con casos pequeños, crecemos poco a poco
                size = i + 1
                
                # Generamos los valores
                try:
                    values = tuple(gen.generate(rng, size) for gen in generators)
                except ValueError:
                    continue # Si un filter falla mucho, saltamos iteración
                
                # Ejecutamos el test
                try:
                    result = test_fn(*values)
                    # Si devuelve False o lanza excepción, falló
                    if result is False:
                        raise AssertionError("Test returned False")
                except Exception:
                    # ¡Fallo encontrado! Iniciamos Shrinking
                    shrunk = shrink_counterexample(values, generators, test_fn)
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
    """Marca una función como test de propiedad (metadata)."""
    fn._is_property_test = True
    return fn