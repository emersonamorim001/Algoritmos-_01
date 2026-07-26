"""
    Multiplicação rápida usando o algoritmo de Karatsuba
    Complexidade: O(n^log₂3) ≈ O(n^1.585)
 """

def karatsuba(x, y):
    
    # Caso base: números pequenos
    if x < 10 or y < 10:
        return x * y
    
    # Determina o número de dígitos
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    
    # Divide os números
    divisor = 10 ** m
    a, b = divmod(x, divisor)
    c, d = divmod(y, divisor)
    
    # 3 multiplicações recursivas
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    ad_bc = karatsuba(a + b, c + d) - ac - bd
    
    # Combina os resultados
    return ac * (10 ** (2 * m)) + ad_bc * (10 ** m) + bd

# Teste básico
A = 1234
B = 5678
resultado = karatsuba(A,B)
print(f"karatsuba({A}, {B}) = {resultado}")
print(f"Comfirmação: {A*B}")