from typing import Any, Callable, Tuple

def shrink_counterexample(
    values: Tuple[Any, ...],
    generators: Tuple[Any, ...], 
    test_fn: Callable
) -> Tuple[Any, ...]:
    """
    Intenta reducir un contraejemplo paso a paso.
    """
    current = values
    max_shrink_steps = 100
    steps = 0

    while steps < max_shrink_steps:
        steps += 1
        shrunk_any = False
        
        for i, (value, gen) in enumerate(zip(current, generators)):
            candidates = gen.shrink(value)
            
            for shrunk_value in candidates:
                test_values = current[:i] + (shrunk_value,) + current[i+1:]
                
                try:
                    # Si la prueba sigue fallando (False o Exception), aceptamos el shrink
                    result = test_fn(*test_values)
                    if result is False:
                        current = test_values
                        shrunk_any = True
                        break 
                except Exception:
                    current = test_values
                    shrunk_any = True
                    break
            
            if shrunk_any:
                break
        
        if not shrunk_any:
            break
            
    return current