
offre = [5, 6, 6]                 
demande = [4, 5, 8]               
C = [[4, 6, 8],                   
     [5, 3, 7],
     [6, 4, 2]]
m, p = len(offre), len(demande)


def cout(x):
    return sum(C[i][j] * x[i][j] for i in range(m) for j in range(p))


def solution_initiale():
    x = [[0] * p for _ in range(m)]
    o, dm = offre[:], demande[:]
    for _, i, j in sorted((C[i][j], i, j) for i in range(m) for j in range(p)):
        q = min(o[i], dm[j])
        x[i][j] += q
        o[i] -= q
        dm[j] -= q
    return x


def voisins(x):
    for i in range(m):
        for k in range(m):
            if i == k:
                continue
            for j1 in range(p):
                for j2 in range(p):
                    if j1 != j2 and x[i][j1] >= 1 and x[k][j2] >= 1:
                        y = [r[:] for r in x]
                        y[i][j1] -= 1; y[i][j2] += 1
                        y[k][j2] -= 1; y[k][j1] += 1
                        yield (i, k, j1, j2), y


def tabou(iters=30, tenure=5):
    x = solution_initiale()
    best, fbest = [r[:] for r in x], cout(x)
    tabu = {}
    print("initiale", x, "cout", fbest)
    for it in range(1, iters + 1):
        cand = None
        for mv, y in voisins(x):
            f = cout(y)
            if tabu.get(mv, 0) >= it and f >= fbest:   
                continue
            if cand is None or f < cand[0]:
                cand = (f, mv, y)
        if cand is None:
            break
        f, mv, x = cand
        i, k, j1, j2 = mv
        tabu[(i, k, j2, j1)] = it + tenure     
        if f < fbest:
            best, fbest = [r[:] for r in x], f
        print(f"it {it}: mouvement {mv} cout {f} (meilleur {fbest})")
    return best, fbest


if __name__ == "__main__":
    sol, f = tabou()
    print("Solution :", sol, "Cout total :", f)