# ============ BLOC 1 : Données et fonctions de base ============
COUT = [[5, 3, 4],
        [6, 7, 2]]
OFFRE = [8, 9]
DEMANDE = [4, 5, 8]


def cout_total(x):
    total = 0
    for i in range(2):
        for j in range(3):
            total += COUT[i][j] * x[i][j]
    return total


def est_realisable(x):
    for i in range(2):
        if sum(x[i]) != OFFRE[i]:
            return False
    for j in range(3):
        if x[0][j] + x[1][j] != DEMANDE[j]:
            return False
    for i in range(2):
        for j in range(3):
            if x[i][j] < 0:
                return False
    return True


# ============ BLOC 2 : Solution initiale (coin nord-ouest) ============
def solution_initiale():
    x = [[0, 0, 0], [0, 0, 0]]
    offre = OFFRE[:]
    demande = DEMANDE[:]
    i = 0
    j = 0
    while i < 2 and j < 3:
        q = min(offre[i], demande[j])
        x[i][j] = q
        offre[i] -= q
        demande[j] -= q
        if offre[i] == 0:
            i += 1
        else:
            j += 1
    return x


# ============ BLOC 3 : Voisinage (mouvement 2x2) ============
def voisins(x):
    liste = []
    for j1 in range(3):
        for j2 in range(j1 + 1, 3):
            for s in (+1, -1):
                y = [ligne[:] for ligne in x]
                y[0][j1] -= s
                y[0][j2] += s
                y[1][j1] += s
                y[1][j2] -= s
                if est_realisable(y):
                    mouvement = (j1, j2, s)
                    liste.append((y, mouvement))
    return liste


# ============ BLOC 4 : Recherche taboue ============
def recherche_taboue(max_iter=15, taille_tabou=4):
    x = solution_initiale()
    meilleur = [ligne[:] for ligne in x]
    meilleur_cout = cout_total(x)
    tabou = []
    print("Init :", x, "coût =", cout_total(x))

    for it in range(1, max_iter + 1):
        candidats = []
        for y, m in voisins(x):
            c = cout_total(y)
            if m in tabou and c >= meilleur_cout:
                continue
            candidats.append((c, y, m))
        if not candidats:
            break
        c, y, m = min(candidats, key=lambda t: t[0])
        x = y
        tabou.append((m[0], m[1], -m[2]))
        if len(tabou) > taille_tabou:
            tabou.pop(0)
        if c < meilleur_cout:
            meilleur = [ligne[:] for ligne in y]
            meilleur_cout = c
        print("Iter", it, ":", x, "coût =", c, "| meilleur =", meilleur_cout, "| tabou =", tabou)
    return meilleur, meilleur_cout


# ============ BLOC 5 : Programme principal ============
if __name__ == "__main__":
    sol, c = recherche_taboue()
    print()
    print("===== Solution finale =====")
    for i in range(2):
        print("D" + str(i + 1), "-> M1:", sol[i][0], " M2:", sol[i][1], " M3:", sol[i][2])
    print("Coût minimal =", c)