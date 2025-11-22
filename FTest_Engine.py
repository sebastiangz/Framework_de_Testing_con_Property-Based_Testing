# main.py
from src import run_demo, integer, property_test, forall

# Ejecutar la demo interna
run_demo()

# O crear tu propio test aquí mismo
print("\n--- Mi Propio Test ---")
@property_test
@forall(integer())
def test_par(x):
    # Esto va a fallar a propósito para ver el shrinking
    return x % 2 == 0 

res = test_par()
if not res.success:
    print(f"Test falló. Contraejemplo encontrado: {res.counterexample}")