"""
properties.py
"""

from typing import Callable, Any

class Property:
    """
    Representa una propiedad a verificar.
    Una propiedad es una función que recibe un valor y:
    - Devuelve True si la propiedad se cumple
    - Devuelve False o lanza excepción si falla
    """

    def __init__(self, strategy, test_func: Callable[[Any], bool]):
        self.strategy = strategy   # Estrategia para generar datos
        self.test_func = test_func

    def run_once(self):
        """
        Genera un valor, lo prueba y devuelve el valor.
        Si falla, se lanza AssertionError.
        """
        value = self.strategy.generate()
        try:
            result = self.test_func(value)
            if result is False:
                raise AssertionError("La propiedad devolvió False.")
            return value
        except Exception as e:
            raise AssertionError(f"La propiedad falló con el valor {value}: {e}")

    def shrink(self, value):
        """
        Mecanismo simple de shrinking.
        La idea: si el valor es reducible (int, list, str), intentamos
        generar versiones "más pequeñas" hasta encontrar la mínima que falle.

        NOTA: versión simplificada, útil para demostración.
        """
        # int: intentamos acercarnos a 0
        if isinstance(value, int):
            candidates = [value // 2, 0]
        # list: intentamos achicar por tamaño
        elif isinstance(value, list) and value:
            candidates = [value[: len(value)//2], []]
        # string: reducir longitud
        elif isinstance(value, str) and value:
            candidates = [value[: len(value)//2], ""]
        else:
            return value  # No shrinkable

        smallest = value
        for c in candidates:
            try:
                self.test_func(c)  # Si falla, seguimos achicando
                # Si NO falla, no sirve
            except Exception:
                smallest = c
        return smallest


def for_all(strategy, property_func):
    """
    Crea un objeto Property que combina estrategia + función propiedad.
    """
    return Property(strategy, property_func)


class TestRunner:
    """
    Motor para ejecutar propiedades.
    Ahora imprime valores generados y aplica shrinking cuando hay fallas.
    """

    def __init__(self, iterations: int = 100):
        self.iterations = iterations

    def run(self, prop: Property):
        """
        Ejecuta la propiedad `iterations` veces.
        Si encuentra una falla:
        - Muestra el valor que la provocó
        - Intenta reducirlo usando shrinking
        - Reporta el valor mínimo que sigue fallando
        """
        for i in range(self.iterations):
            try:
                value = prop.run_once()
                print(f" Iteración {i+1}: valor generado = {value}")
            except AssertionError as e:
                failing_value = str(e).split("valor ")[-1]
                print("\n Falla encontrada:")
                print(str(e))
                # Intento de shrinking
                print("Intentando shrinking...")
                minimal = prop.shrink(eval(failing_value.split(":")[0]))
                print(f"Valor mínimo que también falla: {minimal}")
                return

        print("\nPropiedad verificada: no se encontraron fallas.")