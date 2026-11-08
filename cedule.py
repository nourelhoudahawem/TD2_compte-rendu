import random
from itertools import product

# 1. Donnees du probleme
CAPACITES = [20, 15, 35, 40, 15, 15, 10]
DEMANDES = [80, 90, 65, 70]

MOTIFS = [
    ["1100", "0110", "0011"],
    ["1100", "0110", "0011"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"]
]

CAPACITE_TOTALE = sum(CAPACITES)

# 2. Parametres
TAILLE_POPULATION = 49
NOMBRE_GENERATIONS = 200
PC = 0.8
PM = 0.2
TYPE_MUTATION = "inversion"    # "inversion" ou "remplacement"


# 3. Population initiale
def generer_chromosome():
    return [random.choice(motifs) for motifs in MOTIFS]


def generer_population():
    return [generer_chromosome() for _ in range(TAILLE_POPULATION)]


# 4. Reserves et fitness
def calculer_reserves(chromosome):
    reserves = []

    for j in range(4):
        puissance_maintenance = 0

        for i in range(7):
            if chromosome[i][j] == "1":
                puissance_maintenance += CAPACITES[i]

        reserves.append(CAPACITE_TOTALE - puissance_maintenance - DEMANDES[j])

    return reserves


def fitness(chromosome):
    reserves = calculer_reserves(chromosome)

    if min(reserves) < 0:
        return 0

    return min(reserves)


# 5. Selection par loterie
def selection_loterie(population, valeurs):
    total = sum(valeurs)

    if total == 0:
        return random.choice(population)

    tirage = random.uniform(0, total)
    cumul = 0

    for individu, valeur in zip(population, valeurs):
        cumul += valeur
        if cumul >= tirage:
            return individu

    return population[-1]


# 6. Croisement
def croisement(parent1, parent2):
    point = random.randint(1, 6)

    enfant1 = parent1[:point] + parent2[point:]
    enfant2 = parent2[:point] + parent1[point:]

    return enfant1, enfant2


# 7. Mutations
def mutation_inversion(chromosome):
    chromosome = chromosome.copy()

    if random.random() < PM:
        position = random.randint(0, 6)
        chromosome[position] = chromosome[position][::-1]

    return chromosome


def mutation_remplacement(chromosome):
    chromosome = chromosome.copy()

    if random.random() < PM:
        position = random.randint(0, 6)

        motifs_possibles = [
            m for m in MOTIFS[position] if m != chromosome[position]
        ]

        chromosome[position] = random.choice(motifs_possibles)

    return chromosome


def mutation(chromosome):
    if TYPE_MUTATION == "inversion":
        return mutation_inversion(chromosome)
    return mutation_remplacement(chromosome)


# 8. Algorithme genetique
def algorithme_genetique():
    population = generer_population()
    meilleur = max(population, key=fitness)

    for generation in range(NOMBRE_GENERATIONS):

        valeurs = [fitness(c) for c in population]
        nouvelle_population = [meilleur.copy()]

        while len(nouvelle_population) < TAILLE_POPULATION:

            parent1 = selection_loterie(population, valeurs)
            parent2 = selection_loterie(population, valeurs)

            if random.random() < PC:
                enfant1, enfant2 = croisement(parent1, parent2)
            else:
                enfant1, enfant2 = parent1.copy(), parent2.copy()

            nouvelle_population.append(mutation(enfant1))

            if len(nouvelle_population) < TAILLE_POPULATION:
                nouvelle_population.append(mutation(enfant2))

        population = nouvelle_population

        candidat = max(population, key=fitness)
        if fitness(candidat) > fitness(meilleur):
            meilleur = candidat.copy()

        if (generation + 1) % 20 == 0:
            print(f"Generation {generation + 1} : Fitness = {fitness(meilleur)} MW")

    return meilleur


# 9. Affichage
def afficher_solution(chromosome):
    print("\n========== MEILLEURE SOLUTION ==========")

    for i, gene in enumerate(chromosome):
        print(f"Unite {i + 1} : {gene}")

    reserves = calculer_reserves(chromosome)

    print("\n========== RESERVES ==========")

    for j in range(4):
        print(f"Intervalle {j + 1} : {reserves[j]} MW")

    print("\nFitness :", fitness(chromosome), "MW")


# 10. Verification par force brute
def optimum_exact():
    meilleur_f = 0
    for combinaison in product(*MOTIFS):
        meilleur_f = max(meilleur_f, fitness(list(combinaison)))
    return meilleur_f


# 11. Programme principal
if __name__ == "__main__":
    print(f"Mutation utilisee : {TYPE_MUTATION}\n")
    meilleure_solution = algorithme_genetique()
    afficher_solution(meilleure_solution)
    print("Optimum exact (force brute) :", optimum_exact(), "MW")