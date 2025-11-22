import pytest
from src.shrinking import shrink_counterexample

# --- Mocks y Helpers ---

class MockGenerator:
    """
    Un generador simulado donde controlamos explícitamente el mapa de shrinking.
    Ejemplo: si shrink_map es {10: [5, 0]}, al llamar shrink(10) devuelve [5, 0].
    """
    def __init__(self, shrink_map: dict):
        self.shrink_map = shrink_map

    def shrink(self, value):
        return self.shrink_map.get(value, [])

# --- Tests ---

class TestShrinkCounterexample:

    def test_basic_shrink_greedy(self):
        """
        Verifica que el algoritmo tome el primer candidato que siga fallando (Greedy).
        Escenario: 
        - Valor actual: 10
        - Candidatos: [0, 5, 9]
        - Test: Falla para x > 3.
        
        Lógica esperada:
        1. Prueba 0 -> Test Pasa (0 <= 3). No sirve (queremos que falle).
        2. Prueba 5 -> Test Falla (5 > 3). ¡Sirve! Nuevo valor: 5.
        3. Reinicia ciclo con 5.
        """
        # Definimos cómo se reduce el 10 y el 5
        gen = MockGenerator({
            10: [0, 5, 9],
            5: [0, 4],
            4: [0]
        })
        
        # La función de prueba devuelve False si el test falla (nuestra condición de éxito para shrink)
        # Falla si x > 3
        def failing_test(x):
            return x <= 3 # Devuelve False si x > 3
            
        final_vals = shrink_counterexample(
            values=(10,), 
            generators=(gen,), 
            test_fn=failing_test
        )
        
        # Debería bajar de 10 -> 5 -> 4. 
        # En 4, su candidato es 0. 0 pasa el test (True). 
        # Así que se queda en 4.
        assert final_vals == (4,)

    def test_shrink_via_exception(self):
        """
        Verifica que el shrink funcione cuando el test falla lanzando una Excepción
        en lugar de devolver False.
        """
        gen = MockGenerator({
            "error_long": ["error", "ok"], 
            "error": ["ok"]
        })

        def test_fn(val):
            if "error" in val:
                raise ValueError("Boom!") # El test falla
            return True # El test pasa

        # Empezamos con "error_long".
        # Candidatos: "error", "ok".
        # "error": lanza Exception -> Shrink aceptado. Nuevo valor: "error".
        # Siguiente paso: "error" -> "ok".
        # "ok": retorna True -> Shrink rechazado.
        # Resultado final: "error".
        
        final_vals = shrink_counterexample(
            values=("error_long",),
            generators=(gen,),
            test_fn=test_fn
        )
        
        assert final_vals == ("error",)

    def test_multi_argument_shrink(self):
        """
        Verifica que pueda reducir múltiples argumentos en la misma tupla.
        """
        gen_a = MockGenerator({10: [0, 5]})
        gen_b = MockGenerator({20: [0, 10]})
        
        # El test falla si la suma es > 0.
        # Queremos llegar al "falso" más pequeño posible, que sería (algo > 0).
        # Pero veamos el comportamiento greedy:
        # (10, 20) -> prueba a -> 0. (0, 20). Suma 20 (>0). Falla. Acepta (0, 20).
        # (0, 20) -> prueba a (no más) -> prueba b -> 0. (0, 0). Suma 0. Pasa el test. Rechaza 0.
        # (0, 20) -> prueba b -> 10. (0, 10). Suma 10 (>0). Falla. Acepta (0, 10).
        
        def test_sum_limit(a, b):
            # Test pasa si suma == 0. Falla si suma > 0.
            if (a + b) > 0:
                return False
            return True

        final_vals = shrink_counterexample(
            values=(10, 20),
            generators=(gen_a, gen_b),
            test_fn=test_sum_limit
        )
        
        # Esperamos que ambos se hayan reducido tanto como sea posible 
        # mientras mantengan la suma > 0.
        assert final_vals == (0, 10)

    def test_local_minimum(self):
        """
        Verifica que si ningún candidato causa fallo, se devuelve el valor original.
        """
        gen = MockGenerator({ 5: [0, 1, 2] })
        
        # El test falla SOLO con 5.
        # 0, 1, 2 pasan el test.
        def specific_fail(x):
            return x != 5 # Retorna False (falla) solo si x es 5
            
        final_vals = shrink_counterexample((5,), (gen,), specific_fail)
        
        assert final_vals == (5,)

    def test_max_steps_limit(self):
        """
        Evita bucles infinitos si el grafo de shrink es circular (aunque los generadores
        no deberían serlo, es bueno protegerse).
        """
        # Grafo circular: 1 -> 2 -> 1 ...
        gen = MockGenerator({
            1: [2],
            2: [1]
        })
        
        def always_fail(x):
            return False
            
        # Si no hubiera límite, esto correría por siempre
        final_vals = shrink_counterexample((1,), (gen,), always_fail)
        
        # Solo verificamos que termina y devuelve algo válido
        assert final_vals in [(1,), (2,)]

    def test_integration_list_structure(self):
        """
        Simula un caso más real con una lista que se reduce en tamaño.
        """
        # Mock complejo: reducir una lista [10, 10]
        # shrinks posibles: [] (vacía), [10] (uno solo)
        gen = MockGenerator({
            (10, 10): [(10,), ()], # La lista se representa como tupla aquí para el mock
            (10,): [()],
            (): []
        })
        
        # El test falla si la lista no está vacía
        def fail_if_not_empty(lst):
            return len(lst) == 0
            
        final_vals = shrink_counterexample(((10, 10),), (gen,), fail_if_not_empty)
        
        # Debería reducirse a la lista más pequeña que no sea vacía: (10,)
        # (10, 10) -> prueba (10,) -> Falla (len 1 != 0). Acepta.
        # (10,) -> prueba () -> Pasa (len 0 == 0). Rechaza.
        assert final_vals == ((10,),)