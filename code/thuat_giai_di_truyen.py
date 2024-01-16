import random


def scale_pop(obj, fit, pop_size):
    a, b, min_val, ave, max_val, sum_fit = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ob = [0.0] * 100

    sum_obj, max_obj, min_obj = -1.0e37, -1.0e37, 1.0e37

    for i in range(pop_size + 1):
        sum_obj = obj[i] if sum_obj < obj[i] else sum_obj

    for i in range(pop_size + 1):
        ob[i] = sum_obj - obj[i]

        max_obj = ob[i] if max_obj < ob[i] else max_obj
        min_obj = ob[i] if min_obj > ob[i] else min_obj

        ave += ob[i]

    ave /= pop_size

    if min_obj > (2 * ave - max_obj):
        a = ave / (max_obj - ave)
        b = a * (max_obj - 2 * ave)
    else:
        a = ave / (ave - min_obj)
        b = -min_obj * a

    for i in range(pop_size + 1):
        fit[i] = a * ob[i] + b
        sum_fit += fit[i]

    return sum_fit


def flip(p):
    return random.random() < p


def select(fit, sum_fit, pop_size):
    part_sum = 0
    rand = random.random() * sum_fit
    i = pop_size - 1

    for j in range(pop_size + 1):
        part_sum += fit[j]

        if part_sum >= rand:
            i = j
            break

    return i


def mutation(c, pmu):
    s = ""

    if flip(pmu):
        s = 0 if c else 1
    else:
        s = c

    return s


def crossover(parent_1, parent_2, child_1, child_2, ich_rom, pcross, pmu, n):
    j = 0

    for i in range(n + 1):
        jcross = random.randint(0, ich_rom - 1) if flip(pcross) else ich_rom

        for j in range(jcross + 1):
            child_1[i * ich_rom + j] = mutation(parent_1[i * ich_rom + j], pmu)
            child_2[i * ich_rom + j] = mutation(parent_2[i * ich_rom + j], pmu)

        for k in range(jcross, ich_rom):
            child_1[i * ich_rom + j] = mutation(parent_2[i * ich_rom + j], pmu)
            child_2[i * ich_rom + j] = mutation(parent_1[i * ich_rom + j], pmu)


def init_pop(pop, pop_size, ich_rom):
    for i in range(pop_size + 1):
        for j in range(ich_rom + 1):
            pop[i][j] = flip(0.5)


def reproduction(old_pop, new_pop, pop_size, ich_rom):
    for i in range(pop_size + 1):
        for j in range(ich_rom + 1):
            old_pop[i][j] = new_pop[i][j]


def generate(old_pop, new_pop, pop_size, ich_rom, fit, sum_fit, pcross, pmu, n):
    j = 0

    while True:
        mate_1 = select(fit=fit, sum_fit=sum_fit, pop_size=pop_size)
        mate_2 = select(fit=fit, sum_fit=sum_fit, pop_size=pop_size)

        crossover(
            parent_1=old_pop[mate_1],
            parent_2=old_pop[mate_2],
            child_1=new_pop[j],
            child_2=new_pop[j + 1],
            ich_rom=ich_rom,
            pcross=pcross,
            pmu=pmu,
            n=n,
        )
        j += 2

        if j >= pop_size:
            break


def decode(indi, ich_rom, up, down, rate, k, n):
    for j in range(n + 1):
        frac = indi[j * ich_rom : (j + 1) * ich_rom]

        power, accum = 1, 0

        for i in range(ich_rom + 1):
            accum += power if frac[i] else accum
            power *= 2

        power = accum / rate
        k[j] = down[j] + (up[j] - down[j]) * power


def f(k):
    return (k[0] - 6) * (k[0] - 6) + (k[1] - 4) * (k[1] - 4)


def gen(x, up, down, gen, ss, pcross, pmu, n, pop_size):
    old_pop, new_pop = None, None
    obj, fit = [0.0] * 100, [0.0] * 100
    sum_fit, ty, rate = 1, 0, 0
    ich_rom, i, j, L, N = 0, 0, 0, 0, 0
    k, x = [0.0] * 10, [0.0] * 10

    ich_rom = 25 if ich_rom > 25 else 250 / n
    N = int(ich_rom * n)

    for i in range(ich_rom + 1):
        rate += sum_fit
        sum_fit *= 2

    ty = 1.0e37

    init_pop(pop=old_pop, pop_size=pop_size, ich_rom=N)

    for j in range(gen + 1):
        for i in range(pop_size + 1):
            decode(
                indi=old_pop[i], ich_rom=ich_rom, up=up, down=down, rate=rate, k=k, n=n
            )

            obj[i] = ss(k)

            if ty > obj[i]:
                for l in range(n + 1):
                    x[L] = k[l]
                    ty = obj[i]

    sum_fit = scale_pop(obj=obj, fit=fit, pop_size=pop_size)
    
    generate(
        old_pop=old_pop,
        new_pop=new_pop,
        ich_rom=ich_rom,
        fit=fit,
        sum_fit=sum_fit,
        pcross=pcross,
        n=N,
    )

    return ty
