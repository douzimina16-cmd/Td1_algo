import random, math

INF = 10**6
n = 8
d = [[INF] * (n + 1) for _ in range(n + 1)]
data = {
    1: [14, 15, None, None, None, None, 17],
    2: [13, 14, 20, None, None, 21],
    3: [11, 21, 17, 9, 9],
    4: [11, 10, 8, 20],
    5: [15, 18, None],
    6: [9, None],
    7: [13],
}
for i, row in data.items():
    for k, v in enumerate(row):
        j = i + 1 + k
        if v is not None:
            d[i][j] = d[j][i] = v


def cout(t):
    """t = [1, ..., 1] (tournee fermee)"""
    return sum(d[t[k]][t[k + 1]] for k in range(len(t) - 1))


def fmt(t):
    return "-".join(map(str, t))


def voisins(t):
    """echange de deux villes (la ville 1 reste fixe)"""
    for a in range(1, n):
        for b in range(a + 1, n):
            v = t[:]
            v[a], v[b] = v[b], v[a]
            yield (t[a], t[b]), v



def tabou(init, iters=6, tenure=3):
    cur = init[:]
    best, fbest = cur[:], cout(cur)
    tabu = {}
    print("TABOU  solution initiale", fmt(cur), "cout", cout(cur))
    for it in range(1, iters + 1):
        cand = None
        for mv, v in voisins(cur):
            f = cout(v)
            est_tabou = tabu.get(frozenset(mv), 0) >= it
            if est_tabou and f >= fbest:      # aspiration
                continue
            if cand is None or f < cand[0]:
                cand = (f, mv, v)
        f, mv, cur = cand
        tabu[frozenset(mv)] = it + tenure
        if f < fbest:
            best, fbest = cur[:], f
        print(f"  it {it}: echange {mv} -> {fmt(cur)} cout {f} | meilleur {fbest}")
    return best, fbest

def recuit(init, iters=5, T=10.0, alpha=0.8, seed=1):
    random.seed(seed)
    cur, fcur = init[:], cout(init)
    best, fbest = cur[:], fcur
    print("RECUIT solution initiale", fmt(cur), "cout", fcur)
    for it in range(1, iters + 1):
        a, b = sorted(random.sample(range(1, n), 2))
        v = cur[:]
        v[a], v[b] = v[b], v[a]
        fv = cout(v)
        delta = fv - fcur
        if delta <= 0:
            ok, p = True, 1.0
        else:
            p = math.exp(-delta / T)
            r = random.random()
            ok = r < p
        print(f"  it {it}: T={T:.2f} voisin {fmt(v)} cout {fv} delta={delta} p={p:.3f} -> {'accepte' if ok else 'rejete'}")
        if ok:
            cur, fcur = v, fv
            if fcur < fbest:
                best, fbest = cur[:], fcur
        T *= alpha
    return best, fbest

def cout_ind(ind):
    return cout([1] + ind + [1])


def fmt_ind(ind):
    return fmt([1] + ind + [1])


def croisement_ox(p1, p2):
    m = len(p1)
    a, b = sorted(random.sample(range(m), 2))
    enfant = [None] * m
    enfant[a:b + 1] = p1[a:b + 1]
    reste = [c for c in p2 if c not in enfant]
    for k in range(m):
        if enfant[k] is None:
            enfant[k] = reste.pop(0)
    return enfant


def genetique(taille=30, gens=40, pm=0.3, seed=1):
    random.seed(seed)
    base = list(range(2, n + 1))
    pop = []
    while len(pop) < taille:
        p = base[:]
        random.shuffle(p)
        pop.append(p)
    best = min(pop, key=cout_ind)
    for g in range(1, gens + 1):
        pop.sort(key=cout_ind)
        parents = pop[:taille // 2]
        enfants = []
        while len(enfants) < taille - len(parents):
            p1, p2 = random.sample(parents, 2)
            e = croisement_ox(p1, p2)
            if random.random() < pm:
                i, j = random.sample(range(len(e)), 2)
                e[i], e[j] = e[j], e[i]
            enfants.append(e)
        pop = parents + enfants
        b = min(pop, key=cout_ind)
        if cout_ind(b) < cout_ind(best):
            best = b
        if g <= 5 or g % 10 == 0:
            print(f"  gen {g}: meilleur {fmt_ind(b)} cout {cout_ind(b)}")
    return [1] + best + [1], cout_ind(best)


if __name__ == "__main__":
    init = [1, 2, 3, 4, 5, 6, 7, 8, 1]
    print(tabou(init), "\n")
    print(recuit(init), "\n")
    print("GENETIQUE")
    print(genetique())