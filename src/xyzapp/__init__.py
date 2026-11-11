def sumar(a, b):
    """Suma dos numeros; rechaza booleanos y valores no numericos."""
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) for x in (a, b)):
        raise ValueError("Se requieren numeros")
    return a + b
