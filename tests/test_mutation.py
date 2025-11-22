# Se asume la importación de las herramientas base del framework
from src.generators import integer, list_of
from src.properties import property_test, forall
# Se asume que el módulo mutation expone una función para evaluar la puntuación
from src.mutation import run_mutation_test 

# --- Código bajo prueba (target) ---
# Se define una función simple que será el objetivo de las mutaciones.
# (En un proyecto real, esta función estaría en 'src/algos.py' o similar)
def es_par(n: int) -> bool:
    """Verifica si un número es par."""
    return n % 2 == 0

# --- Propiedad Robusta para 'es_par' ---
# Esta propiedad debe ser lo suficientemente buena para "matar" a los mutantes
@property_test
@forall(integer(min_value=-50, max_value=50))
def propiedad_par_impar_inversion(n):
    """
    Propiedad: Si N es par, N+1 debe ser impar (y viceversa).
    
    Esta propiedad es fuerte porque relaciona dos resultados.
    """
    # Si N es par, N+1 NO debe ser par
    if es_par(n):
        assert not es_par(n + 1), f"El mutante sobrevivió: {n} es par y {n+1} también lo es."
    
    # Si N es impar (no es par), N-1 DEBE ser par
    else:
        assert es_par(n - 1), f"El mutante sobrevivió: {n} es impar y {n-1} es impar."


# --- Test de Mutación ---
def test_puntuacion_de_mutacion_de_es_par():
    """
    Ejecuta el proceso de Mutation Testing en la función 'es_par'
    utilizando 'propiedad_par_impar_inversion' para evaluar la calidad del test.
    """
    
    # La función 'run_mutation_test' (hipotética) del framework:
    # 1. Analiza el código de 'es_par'.
    # 2. Genera mutantes (ej: cambia 'n % 2 == 0' por 'n % 2 != 0' o 'n % 3 == 0').
    # 3. Ejecuta 'propiedad_par_impar_inversion' contra cada mutante.
    # 4. Cuenta cuántos mutantes fueron "muertos" (hicieron fallar el test).
    # 5. Retorna la puntuación de mutación (Mutants Killed / Total Mutants).
    
    puntuacion = run_mutation_test(
        target_function=es_par,
        property_test_function=propiedad_par_impar_inversion,
        # Se asumen 1000 iteraciones por mutante para asegurar la detección
        iterations=1000
    )
    
    # Una puntuación de 1.0 (100%) es perfecta. 
    # Se establece un umbral mínimo de 0.90 (90%)
    umbral_minimo = 0.90
    
    assert puntuacion >= umbral_minimo, \
        f" La puntuación de mutación ({puntuacion:.2f}) es baja. Los tests son débiles."
    
    print(f" Mutantes Muertos: {puntuacion * 100:.2f}% - La suite de tests es robusta.")