import math, random

INF = 10_000   # pénalité pour une arête inexistante
N = 8
d = [[INF] * (N + 1) for _ in range(N + 1)]
aretes = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17, (3, 7): 9, (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9,
    (7, 8): 13,
}
for (a, b), w in aretes.items():
    d[a][b] = d[b][a] = w


def longueur(t):
    return sum(d[t[k]][t[(k + 1) % N]] for k in range(N))


def affiche(t):
    return "-".join(map(str, t + [t[0]]))


def voisin_2opt(t, i, j):
    return t[:i] + t[i:j + 1][::-1] + t[j + 1:]


# ---------------- Recherche taboue ----------------
def tabou(init, max_iter=20, taille_tabou=5):
    cur, best = init[:], init[:]
    best_c = longueur(best)
    liste = []
    print(f"Init {affiche(cur)}  L = {longueur(cur)}")
    for it in range(1, max_iter + 1):
        cand = []
        for i in range(1, N - 1):
            for j in range(i + 1, N):
                v = voisin_2opt(cur, i, j)
                c = longueur(v)
                if (i, j) in liste and c >= best_c:
                    continue
                cand.append((c, v, (i, j)))
        if not cand:
            break
        c, v, m = min(cand, key=lambda t: t[0])
        cur = v
        liste.append(m)
        if len(liste) > taille_tabou:
            liste.pop(0)
        if c < best_c:
            best, best_c = v[:], c
        print(f"Iter {it:2d} : inversion {m} -> {affiche(cur)}  L = {c} | meilleur = {best_c}")
    return best, best_c


# ---------------- Recuit simulé ----------------
def recuit(init, T0=30.0, alpha=0.6, iterations=5, essais_par_palier=15, seed=3):
    random.seed(seed)
    cur, cur_c = init[:], longueur(init)
    best, best_c = cur[:], cur_c
    T = T0
    print(f"Init {affiche(cur)}  L = {cur_c}  T0 = {T0}")
    for it in range(1, iterations + 1):
        for _ in range(essais_par_palier):
            i, j = sorted(random.sample(range(1, N), 2))
            v = voisin_2opt(cur, i, j)
            c = longueur(v)
            delta = c - cur_c
            if delta <= 0 or random.random() < math.exp(-delta / T):
                cur, cur_c = v, c
                if c < best_c:
                    best, best_c = v[:], c
        print(f"Iter {it} : T = {T:7.3f}  courant = {affiche(cur)} (L={cur_c})  meilleur = {best_c}")
        T *= alpha
    return best, best_c


if __name__ == "__main__":
    init = [1, 2, 3, 4, 5, 6, 7, 8]
    print("=== TABOU ===")
    s, c = tabou(init)
    print("Meilleure tournée :", affiche(s), " L =", c)
    print("\n=== RECUIT SIMULE ===")
    s2, c2 = recuit(init)
    print("Meilleure tournée :", affiche(s2), " L =", c2)