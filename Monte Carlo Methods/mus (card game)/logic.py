from random import shuffle
from typing import List, Tuple, Generator, Union
from itertools import combinations_with_replacement

BARAJA = ["R", "R", "R", "R", "R", "R", "R", "R",
          "1", "1", "1", "1", "1", "1", "1", "1",
          "4", "4", "4", "4",
          "5", "5", "5", "5",
          "6", "6", "6", "6",
          "7", "7", "7", "7",
          "S", "S", "S", "S",
          "C", "C", "C", "C"]


def repartidor(cartas: Union[List[str], Tuple[str, str, str, str]] = None) -> Generator:
    cartas = [] if cartas is None else cartas
    while True:
        # Creamos la baraja
        baraja = BARAJA.copy()
        for c in cartas:
            baraja.remove(c)

        shuffle(baraja)

        for c in baraja:
            yield c


def repartir(n_jugadores, baraja=None) -> Tuple[list] or list:
    baraja = baraja if baraja is not None else BARAJA.copy()
    # El nº es 1 cuando la IA juega contra sí misma en el cálculo de la probabilidad
    if n_jugadores == 1:
        mano1 = [next(baraja) for _ in range(4)]
        return mano1

    else:
        # Barajeamos:
        shuffle(baraja)

        # Repartimos las cartas
        mano1 = baraja[:4]
        mano2 = baraja[4:8]

        return mano1, mano2


# Se declaran fuera porque son los mismos para grande que para chica
ORDEN_CARTA = {"R": 8, "C": 7, "S": 6, "7": 5, "6": 4, "5": 3, "4": 2, "1": 1}


def insertion_sort(lista):
    for j in range(1, len(lista)):
        key = lista[j]
        i = j - 1
        while i >= 0 and lista[i] < key:
            lista[i + 1] = lista[i]
            i -= 1
        lista[i + 1] = key
    return lista


def ordenar(mano) -> List[int]:
    # Cambiamos la lista de cartas por su valor (orden de victoria)
    valores = list(map(lambda x: ORDEN_CARTA[x], mano))
    return insertion_sort(valores)


def gana_grande(cartas1, cartas2, mano) -> int:
    valores1 = ordenar(cartas1)
    valores2 = ordenar(cartas2)

    # Determinamos ganador

    if valores1[0] != valores2[0]:
        if valores1[0] > valores2[0]:
            return 1
        else:
            return 2
    elif valores1[1] != valores2[1]:
        if valores1[1] > valores2[1]:
            return 1
        else:
            return 2
    elif valores1[2] != valores2[2]:
        if valores1[2] > valores2[2]:
            return 1
        else:
            return 2
    elif valores1[3] != valores2[3]:
        if valores1[3] > valores2[3]:
            return 1
        else:
            return 2
    else:
        return mano  # A empate gana quien sea cartas


def gana_chica(cartas1, cartas2, mano) -> int:
    valores1 = ordenar(cartas1)
    valores2 = ordenar(cartas2)

    # Determinamos ganador (proceso inverso)

    if valores1[3] != valores2[3]:
        if valores1[3] < valores2[3]:
            return 1
        else:
            return 2
    elif valores1[2] != valores2[2]:
        if valores1[2] < valores2[2]:
            return 1
        else:
            return 2
    elif valores1[1] != valores2[1]:
        if valores1[1] < valores2[1]:
            return 1
        else:
            return 2
    elif valores1[0] != valores2[0]:

        if valores1[0] < valores2[0]:
            return 1
        else:
            return 2
    else:
        return mano  # A empate gana quien sea cartas


def prob_ganar_grande(cartas, mano) -> float:
    rep = 10_000
    casos_favorables = 0
    baraja = repartidor(cartas)

    for i in range(rep):
        cartas_random = repartir(1, baraja)
        ganador = gana_grande(cartas, cartas_random, mano)
        if ganador == 1:
            casos_favorables += 1

    return casos_favorables / rep


def prob_ganar_chica(cartas, mano):
    rep = 10_000
    casos_favorables = 0
    baraja = repartidor(cartas)

    for i in range(rep):
        cartas_random = repartir(1, baraja)
        ganador = gana_chica(cartas, cartas_random, mano)
        if ganador == 1:
            casos_favorables += 1

    return casos_favorables / rep


if __name__ == "__main__":
    cards = ["R", "C", "S", "7", "6", "5", "4", "1"]
    print(list(combinations_with_replacement(cards, 4)))
