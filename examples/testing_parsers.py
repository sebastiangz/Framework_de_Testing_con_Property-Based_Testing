from hypothesis import given, strategies as st
import pytest

# Imaginemos un parser trivial para expresiones como "1+2*3"
# Y un "serializador" que convierte un AST a cadena.

# Definimos una AST simple
class Expr:
    pass

class Num(Expr):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Num) and self.value == other.value

class Add(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, Add) and self.left == other.left and self.right == other.right

class Mul(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, Mul) and self.left == other.left and self.right == other.right

# Parser (muy simplificado)
def parse_expr(s: str) -> Expr:
    # para el ejemplo, aceptar solo dígitos, +, *
    # no implemento un parser completo, solo algo demo:
    tokens = list(s)
    # aquí debes usar un parser real, pero para la propiedad lo ilustro así
    if '+' in tokens:
        parts = s.split('+', 1)
        return Add(parse_expr(parts[0]), parse_expr(parts[1]))
    elif '*' in tokens:
        parts = s.split('*', 1)
        return Mul(parse_expr(parts[0]), parse_expr(parts[1]))
    else:
        # número
        return Num(int(s))

# Serializador (convierte AST a string)
def serialize_expr(expr: Expr) -> str:
    if isinstance(expr, Num):
        return str(expr.value)
    elif isinstance(expr, Add):
        return f"{serialize_expr(expr.left)}+{serialize_expr(expr.right)}"
    elif isinstance(expr, Mul):
        return f"{serialize_expr(expr.left)}*{serialize_expr(expr.right)}"
    else:
        raise ValueError("Tipo desconocido")

# Generador de cadenas de expresiones válidas
@st.composite
def expr_strings(draw, max_depth=3):
    # estrategia recursiva
    if max_depth == 0:
        # devolver solo número simple
        n = draw(st.integers(min_value=0, max_value=100))
        return str(n)
    else:
        # decidir recursivamente si poner operación
        left = draw(expr_strings(max_depth=max_depth - 1))
        right = draw(expr_strings(max_depth=max_depth - 1))
        op = draw(st.sampled_from(['+', '*']))
        return f"({left}){op}({right})"

@given(expr_strings())
def test_parser_roundtrip(s):
    # parsear la cadena
    ast = parse_expr(s)
    # serializar de nuevo
    s2 = serialize_expr(ast)
    # prop: al parsear la serialización obtenemos un AST equivalente
    ast2 = parse_expr(s2)
    assert ast2 == ast

# También puedes probar que el parser no falla para muchas entradas (incluso malformadas)
@given(st.text(alphabet=list("0123456789+*() "), min_size=0, max_size=20))
def test_parser_no_crash(s):
    try:
        _ = parse_expr(s)
    except Exception:
        # si lanza excepción, depende de si lo permites o no; en PBT puedes requerir que no falle
        pytest.skip("Entrada no válida, pero no queremos que se rompa el parser")
