import pytest
from unittest.mock import MagicMock, patch
from src.properties import forall, property_test, TestResult
from src.generators import integer, Generator

# --- Helpers ---

@pytest.fixture
def mock_shrinking():
    """
    Mockea la función shrink_counterexample para que no dependamos
    de la implementación real de shrinking.py durante este test.
    """
    with patch('src.properties.shrink_counterexample') as mock:
        # Hacemos que el shrink devuelva siempre un valor fijo para verificarlo
        mock.return_value = ("shrunk_value",) 
        yield mock

# --- Tests ---

class TestForallDecorator:
    
    def test_success_case(self):
        """Prueba una propiedad que siempre es verdadera."""
        
        # Propiedad: x + 0 == x
        @forall(integer())
        def prop_identity(x):
            return x + 0 == x

        # Ejecutamos con 50 iteraciones
        result = prop_identity(num_tests=50)
        
        assert isinstance(result, TestResult)
        assert result.success is True
        assert result.num_tests == 50
        assert result.counterexample is None

    def test_failure_exception(self, mock_shrinking):
        """Prueba una propiedad que falla lanzando una excepción (AssertionError)."""
        
        # Propiedad falsa: x siempre es menor que 5 (fallará para x >= 5)
        # Usamos un generador que seguro genere números grandes
        @forall(integer(min_val=10, max_val=20))
        def prop_fail_always(x):
            assert x < 5 

        result = prop_fail_always(num_tests=10)
        
        assert result.success is False
        assert result.counterexample is not None
        # Verificamos que el valor generado estaba en el rango esperado
        assert 10 <= result.counterexample[0] <= 20
        # Verificamos que se llamó al shrinking y se guardó su resultado
        assert result.shrunk_counterexample == ("shrunk_value",)
        mock_shrinking.assert_called_once()

    def test_failure_return_false(self, mock_shrinking):
        """Prueba una propiedad que falla retornando False."""
        
        @forall(integer(min_val=10, max_val=20))
        def prop_return_false(x):
            # Si x > 5 devolvemos False
            return x < 5

        result = prop_return_false(num_tests=10)
        
        assert result.success is False
        assert result.counterexample is not None
        mock_shrinking.assert_called_once()

    def test_multiple_generators(self):
        """Prueba que se pasen correctamente múltiples argumentos."""
        
        # Propiedad: la suma de dos positivos es mayor que sus partes
        @forall(integer(1, 10), integer(1, 10))
        def prop_sum(x, y):
            return (x + y) > x and (x + y) > y

        result = prop_sum(num_tests=20)
        assert result.success is True

    def test_reproducibility_with_seed(self, mock_shrinking):
        """
        Verifica que usando una semilla (seed), el contraejemplo sea idéntico.
        """
        # Definimos una propiedad que falla aleatoriamente (o determinísticamente con seed)
        # x > 50 falla si generamos enteros hasta 100.
        
        @forall(integer(0, 100))
        def prop_random_fail(x):
            assert x <= 50

        # Ejecución 1
        result1 = prop_random_fail(num_tests=50, seed=12345)
        
        # Ejecución 2
        result2 = prop_random_fail(num_tests=50, seed=12345)
        
        assert result1.success == result2.success
        if not result1.success:
            # Los contraejemplos deben ser idénticos
            assert result1.counterexample == result2.counterexample

class TestPropertyTestDecorator:
    def test_metadata_marker(self):
        """Verifica que @property_test añade el atributo _is_property_test."""
        
        @property_test
        def my_test():
            pass
            
        assert hasattr(my_test, '_is_property_test')
        assert my_test._is_property_test is True

class TestIntegrationFlow:
    """
    Test más realista sin mockear el shrinking (suponiendo que shrinking.py existe
    o está vacío pero importable). Valida que el flujo exception -> catch funcione.
    """
    def test_real_exception_handling(self):
        # Creamos un generador dummy manual para controlar exactamente qué sale
        def gen_fn(rng, size): return 10
        def shrink_fn(val): return [5, 0] # Simula shrinking
        dummy_gen = Generator(gen_fn, shrink_fn)

        @forall(dummy_gen)
        def prop_fail(x):
            if x == 10:
                raise ValueError("Boom")
            return True

        # Forzamos el fallo
        # Nota: aquí NO usamos el mock de shrinking, por lo que usará 
        # el shrinking real importado en properties.py. 
        # Si shrinking.py falla, este test fallará.
        try:
            result = prop_fail(num_tests=1)
            assert result.success is False
            assert result.counterexample == (10,)
        except ImportError:
            pytest.skip("Skipping integration test: shrinking module not found")