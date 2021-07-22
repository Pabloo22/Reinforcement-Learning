from random import choice

from player import Player, Human
from apuesta import Apuesta
import logic


class MusGame:
    goal: int
    player1: Player
    player2: Player
    marcador: list[int, int]
    round: int

    def __init__(self, goal: int, p1: Player, p2: Player):
        self.goal = goal
        self.player1 = p1
        self.player2 = p2
        self.marcador = [0, 0]
        self.round = 0

    def is_finished(self) -> bool:
        return self.marcador[0] >= self.goal or self.marcador[1] >= self.goal

    def play(self):
        if isinstance(self.player1, Human) or isinstance(self.player2, Human):
            self.__run_game(imprimir=True)
        else:
            self.__run_game(imprimir=False)
            self.player1.imprimir = False
            self.player2.imprimir = False
            self.player1.goal = self.goal
            self.player2.goal = self.goal
            self.player1.marcador = self.marcador
            self.player2.marcador = self.marcador

    def __print_cartas(self):
        print(f"cartas de {self.player1}: {self.player1.cartas}")
        print(f"cartas de {self.player2}: {self.player2.cartas}")

    def __run_game(self, imprimir: bool):

        # Consideramos siempre al jugador 1 como humano
        if not isinstance(self.player1, Human):
            self.player1, self.player2 = self.player2, self.player1

        self.player2.goal = self.goal
        self.player2.marcador = self.marcador

        self.player1.preguntar_nombre()

        x = choice([0, 1])

        if imprimir:
            print(f"{self.player1} VS {self.player2}")
            print("Suerte!")
        else:
            self.player1.imprimir = False
            self.player2.imprimir = False

        while not self.is_finished():

            if self.round % 2 == x:
                self.player1.mano = True
                self.player2.mano = False
                mano = 1
                if imprimir:
                    print(f"El mano es {self.player1}")
            else:
                self.player1.mano = False
                self.player2.mano = True
                mano = 2
                if imprimir:
                    print(f"El mano es {self.player2}")

            self.player1.cartas, self.player2.cartas = logic.repartir(2)
            if imprimir:
                print("Tus cartas son: " + str(self.player1.cartas))

            # A grande:
            apuesta_grande = self._apostar(lance=1)
            if apuesta_grande.ganador == 1:
                self.marcador[0] += apuesta_grande.apuesta_previa
                if imprimir:
                    print(f"La puntuación de {self.player1} ha subido a: {self.marcador[0]}")
            elif apuesta_grande.ganador == 2:
                self.marcador[1] += apuesta_grande.apuesta_previa
                if imprimir:
                    print(f"La puntuación de {self.player2} ha subido a: {self.marcador[1]}")
            elif apuesta_grande.ordago:
                ganador = logic.gana_grande(self.player1.cartas, self.player2.cartas, mano)
                self.__print_cartas()
                if ganador == 1:
                    self.marcador[0] = self.goal
                    if imprimir:
                        print(f"La puntuación de {self.player1} ha subido a: {self.goal}")
                else:
                    self.marcador[1] = self.goal
                    if imprimir:
                        print(f"La puntuación de {self.player2} ha subido a: {self.goal}")
                break

            if self.is_finished():
                break

            # A chica:
            apuesta_chica = self._apostar(lance=2)
            if apuesta_chica.ganador == 1:
                self.marcador[0] += apuesta_chica.apuesta_previa
                if imprimir:
                    print(f"La puntuación de {self.player1} ha subido a: {self.marcador[0]}")
            elif apuesta_chica.ganador == 2:
                self.marcador[1] += apuesta_chica.apuesta_previa
                if imprimir:
                    print(f"La puntuación de {self.player2} ha subido a: {self.marcador[1]}")
            elif apuesta_chica.ordago:
                ganador = logic.gana_chica(self.player1.cartas, self.player2.cartas, mano)
                self.__print_cartas()
                if ganador == 1:
                    self.marcador[0] = self.goal
                    if imprimir:
                        print(f"La puntuación de {self.player1} ha subido a: {self.goal}")
                else:
                    self.marcador[1] = self.goal
                    if imprimir:
                        print(f"La puntuación de {self.player2} ha subido a: {self.goal}")
                break

            if self.is_finished():
                break

            # Conteo de tantos pendientes:
            # A grande:
            if apuesta_grande.ganador is None:
                ganador = logic.gana_grande(self.player1.cartas, self.player2.cartas, mano)
                if ganador == 1:
                    self.marcador[0] += apuesta_grande.apuesta_total
                    if imprimir:
                        print(f"La puntuación de {self.player1} ha subido a: {self.marcador[0]}")
                elif ganador == 2:
                    self.marcador[1] += apuesta_grande.apuesta_total
                    if imprimir:
                        print(f"La puntuación de {self.player2} ha subido a: {self.marcador[1]}")

                if self.is_finished():
                    break

            if apuesta_chica.ganador is None:
                ganador = logic.gana_chica(self.player1.cartas, self.player2.cartas, mano)
                if ganador == 1:
                    self.marcador[0] += apuesta_chica.apuesta_total
                    if imprimir:
                        print(f"La puntuación de {self.player1} ha subido a: {self.marcador[0]}")
                elif ganador == 2:
                    self.marcador[1] += apuesta_chica.apuesta_total
                    if imprimir:
                        print(f"La puntuación de {self.player2} ha subido a: {self.marcador[1]}")

                if self.is_finished():
                    if imprimir:
                        self.__print_cartas()
                    break

            if imprimir:
                print(f"cartas de {self.player1}: {self.player1.cartas}")
                print(f"cartas de {self.player2}: {self.player2.cartas}")
                print(f"puntuación de {self.player1}: {self.marcador[0]}")
                print(f"puntuación de {self.player2}: {self.marcador[1]}")
                print("")

            self.round += 1

        if self.marcador[0] >= self.goal:
            print(f"¡Ha ganado {self.player1}!")
        else:
            print(f"¡Ha ganado {self.player2}!")

    def _apostar(self, lance: int, imprimir: bool = True) -> Apuesta:
        """
        :lance: 1=grande, 2=chica, 3=pares, 4=juego (por ahora solo se puede jugar a grande y a chica)

        Es la función principal de las apuestas.
        Existen 3 posibles acciones: pasar, apostar, ordaguear. Se puede considerar el siguiente arbol de decisión:
        Opción 1, Pasar:
            pasar --> se acaba el bucle
            apuesta n --> continua el bucle... (Opción 3)
            órdago --> ordago() (Opción 2)
        Opción 2, Órdago:
            ordago()
        Opción 3, apuesta n:
            ver --> se acaba el bucle. (Queda pendiente)
            pasar --> se acaba el bucle. (El ganador se lleva la apuesta n previa o en su defecto 1)
            órdago --> ordago()
            apuesta n --> Se repite el bucle.
        """
        if imprimir:
            if lance == 1:
                print("A GRANDE: ")
            elif lance == 2:
                print("A CHICA:")
            elif lance == 3:
                print("A PARES:")
            else:
                print("A JUEGO:")

        apuesta = Apuesta()

        while not apuesta.acuerdo:
            if self.player1.mano:
                apuesta = self.player1.pedir_apuesta(apuesta, 1, lance)

                if apuesta.acuerdo and apuesta.n_acciones > 1:
                    break

                apuesta = self.player2.pedir_apuesta(apuesta, 2, lance)
            else:
                apuesta = self.player2.pedir_apuesta(apuesta, 2, lance)

                if apuesta.acuerdo and apuesta.n_acciones > 1:
                    break

                apuesta = self.player1.pedir_apuesta(apuesta, 1, lance)

        return apuesta
