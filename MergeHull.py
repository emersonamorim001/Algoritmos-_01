import math


def turn(p, q, r):
    """
    Produto vetorial (cross product) de (q-p) e (r-p).

    Retorna:
      > 0 -> anti-horário (esquerda)
      < 0 -> horário (direita)
      == 0 -> pontos colineares
    """
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def distance(a, b):
    """Distância euclidiana entre dois pontos (usada para desempate em colinearidade)."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def leftmost(pts):
    """Retorna a lista de pontos com o menor x (pode haver empate = aresta vertical)."""
    min_x = min(p[0] for p in pts)
    return [p for p in pts if p[0] == min_x]


def rightmost(pts):
    """Retorna a lista de pontos com o maior x (pode haver empate = aresta vertical)."""
    max_x = max(p[0] for p in pts)
    return [p for p in pts if p[0] == max_x]


def topmost(pts):
    """Dentre os pontos empatados em x, retorna os de maior y."""
    max_y = max(p[1] for p in pts)
    return [p for p in pts if p[1] == max_y]


def bottommost(pts):
    """Dentre os pontos empatados em x, retorna os de menor y."""
    min_y = min(p[1] for p in pts)
    return [p for p in pts if p[1] == min_y]


def _merge(l, r):
    """
    Funde dois cascos convexos em um só.

    Convenção mantida em toda a recursão:
      - o primeiro ponto da lista é o mais à esquerda (menor x);
      - os pontos seguintes estão em ordem anti-horária (CCW).

    A fusão é feita encontrando a tangente superior e a tangente inferior
    entre os dois cascos.
    """
    ret = []

    # Caso base: funde 2 pontos, o de menor y primeiro
    if len(l) == 1 and len(r) == 1:
        if l[0][1] < r[0][1]:
            ret.extend(l)
            ret.extend(r)
        else:
            ret.extend(r)
            ret.extend(l)
        return ret

    # Garante que o casco comece pelo ponto mais à esquerda
    while len(l) > 1 and l[0][0] > l[1][0]:
        rotate = l.pop(0)
        l.append(rotate)

    # Pontos candidatos: mais à direita de l e mais à esquerda de r
    p = rightmost(l)
    q = leftmost(r)
    p_upp = topmost(p)[0]     # desempate em caso de aresta vertical
    p_low = bottommost(p)[0]
    q_upp = topmost(q)[0]
    q_low = bottommost(q)[0]
    p_upp_i = l.index(p_upp)
    p_low_i = l.index(p_low)
    q_upp_i = r.index(q_upp)
    q_low_i = r.index(q_low)

    # --- Tangente superior ---
    while True:
        p_prev = p_upp
        q_prev = q_upp
        # anda q_upp em sentido horário enquanto formar virada à esquerda
        while True:
            cw_i = (q_upp_i - 1) % len(r)
            t = turn(p_upp, q_upp, r[cw_i])
            if (t > 0) or (t == 0 and distance(p_upp, r[cw_i]) > distance(p_upp, q_upp)):
                q_upp_i = cw_i
                q_upp = r[cw_i]
            else:
                break
        # anda p_upp em sentido anti-horário enquanto formar virada à direita
        while True:
            ccw_i = (p_upp_i + 1) % len(l)
            t = turn(q_upp, p_upp, l[ccw_i])
            if (t < 0) or (t == 0 and distance(q_upp, l[ccw_i]) > distance(q_upp, p_upp)):
                p_upp_i = ccw_i
                p_upp = l[ccw_i]
            else:
                break
        if p_upp == p_prev and q_upp == q_prev:
            break

    # --- Tangente inferior ---
    while True:
        p_prev = p_low
        q_prev = q_low
        # anda q_low em sentido anti-horário enquanto formar virada à direita
        while True:
            ccw_i = (q_low_i + 1) % len(r)
            t = turn(p_low, q_low, r[ccw_i])
            if (t < 0) or (t == 0 and distance(p_low, r[ccw_i]) > distance(p_low, q_low)):
                q_low_i = ccw_i
                q_low = r[ccw_i]
            else:
                break
        # anda p_low em sentido horário enquanto formar virada à esquerda
        while True:
            cw_i = (p_low_i - 1) % len(l)
            t = turn(q_low, p_low, l[cw_i])
            if (t > 0) or (t == 0 and distance(q_low, l[cw_i]) > distance(q_low, p_low)):
                p_low_i = cw_i
                p_low = l[cw_i]
            else:
                break
        if p_low == p_prev and q_low == q_prev:
            break

    # Monta o casco final usando as tangentes encontradas
    ret.extend(l[0:p_low_i + 1])
    if q_upp_i < q_low_i:
        ret.extend(r[q_low_i:len(r)])
        ret.extend(r[0:q_upp_i + 1])
    else:
        ret.extend(r[q_low_i:q_upp_i + 1])
    if p_upp_i != p_low_i:
        if p_upp_i > p_low_i:
            ret.extend(l[p_upp_i:len(l)])

    return ret


def merge_hull_recursive(points):
    """Divisão e conquista pura. Recurso até restar 1 ponto por grupo (caso base trivial)."""
    if len(points) == 1:
        return points
    mid = len(points) // 2
    left_hull = merge_hull_recursive(points[:mid])
    right_hull = merge_hull_recursive(points[mid:])
    return _merge(left_hull, right_hull)


def merge_hull(points_list):
    """Função principal que aceita listas [x, y]."""
    if len(points_list) < 3:
        return points_list

    sorted_points = sorted(points_list, key=lambda p: (p[0], p[1]))
    return merge_hull_recursive(sorted_points)


import matplotlib.pyplot as plt


def plot_convex_hull(all_points, hull_points):
    """Gera um gráfico com todos os pontos e desenha o envoltório convexo (polígono)."""
    all_x = [p[0] for p in all_points]
    all_y = [p[1] for p in all_points]

    hull_closed = hull_points + [hull_points[0]]
    hull_x = [p[0] for p in hull_closed]
    hull_y = [p[1] for p in hull_closed]

    plt.figure(figsize=(8, 6))
    plt.scatter(all_x, all_y, color='blue', label='Pontos Internos', zorder=5)
    plt.scatter([p[0] for p in hull_points], [p[1] for p in hull_points], color='red', s=80, zorder=6)
    plt.plot(hull_x, hull_y, color='red', linestyle='-', linewidth=2, label='Casco Convexo')

    plt.title('Visualização do Merge Hull', fontsize=14)
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    from random import randint as rdt
    N = 1000
    A,B = -N, N
    pontos = []
    for i in range(N):
        x = rdt(A,B)
        y = rdt(A,B)
        pontos.append((x,y))

    resultado = merge_hull(pontos)
    print("Casco Convexo final:", resultado)

    plot_convex_hull(pontos, resultado)
