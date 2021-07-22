from player import Player
from apuesta import Apuesta
import logic

from random import random, choice
from typing import Union


class Agent(Player):

    estrategia_condicional: bool
    imprimir: True
    marcador: Union[list[int, int], None]
    goal: Union[int, None]

    def __init__(self, name="AI", estrategia_condicional: bool = True, imprimir: bool = True):
        super().__init__(name)
        self.goal = None  # it must be filled outside
        self.estrategia_condicional = estrategia_condicional
        self.imprimir = imprimir
        self.marcador = None   # it must be filled outside

    def pedir_apuesta(self, apuesta: Apuesta, who: int, lance: int) -> Apuesta:
        if self.estrategia_condicional:
            return self._politica_predefinida(apuesta, who, lance)

    def print_tirar_ordago(self):
        if self.imprimir:
            print(f"{self} ha tirado un órdago!")

    def print_se_ve(self):
        if self.imprimir:
            print(f"{self} ha visto la apuesta")

    def print_apostar(self, n: int):
        if self.imprimir:
            print(f"{self} ha apostado {n}")

    def print_subir_apuesta(self, n: int):
        if self.imprimir:
            print(f"{self} apuesta {n} más")

    def print_pasar(self):
        if self.imprimir:
            print(f"{self} ha pasado")

    def get_marcador_pts_restantes(self) -> list[int, int]:
        return [self.goal - self.marcador[0], self.goal - self.marcador[1]]

    def _politica_predefinida(self, apuesta: Apuesta, who: int, lance: int) -> Apuesta:

        if who == 1:
            mano = 1 if self.mano else 2
        else:
            mano = 2 if self.mano else 1

        if lance == 1:
            prob_ganar = logic.prob_ganar_grande(self.cartas, mano)
        elif lance == 2:
            prob_ganar = logic.prob_ganar_chica(self.cartas, mano)

        pts_restantes = self.get_marcador_pts_restantes()
        rival = 1 if who == 2 else 2

        if pts_restantes[rival-1] == 1 or (pts_restantes[rival - 1] < 5 < pts_restantes[who - 1]):
            return self._modo_desesperacion(apuesta, who)
        elif pts_restantes[who-1] - pts_restantes[rival-1] > 5 and pts_restantes[rival-1] <= 10:
            return self._modo_pasivo_agresivo(apuesta, prob_ganar, who)
        elif random() > 0.25:
            return self._modo_agresivo(apuesta, prob_ganar, who)
        else:
            return self._modo_normal(apuesta, prob_ganar, who)

    def _modo_desesperacion(self, apuesta: Apuesta, who: int) -> Apuesta:
        if apuesta.ordago:
            apuesta.se_ve()
            self.print_se_ve()
        else:
            self.print_tirar_ordago()
            apuesta.tirar_ordago(who)

        return apuesta

    def _modo_normal(self, apuesta: Apuesta, prob_ganar: float, who: int) -> Apuesta:
        x = random()
        envidar_fuerte = choice([3, 4, 5])
        envidar_flojo = choice([2, 3])

        if prob_ganar > 0.9:
            if apuesta.ordago:
                apuesta.se_ve()
                self.print_se_ve()
            elif apuesta.apuesta_total == 1:
                if x < 0.1:
                    self.print_apostar(envidar_flojo)
                    apuesta.subir_apuesta(envidar_flojo - 1, who)
                elif x < 0.9:
                    self.print_apostar(envidar_fuerte)
                    apuesta.subir_apuesta(envidar_fuerte - 1, who)
                else:
                    self.print_tirar_ordago()
                    apuesta.tirar_ordago(who)
            elif apuesta.apuesta_total <= 10:
                if x < 0.1:
                    self.print_subir_apuesta(envidar_flojo)
                    apuesta.subir_apuesta(envidar_flojo, who)
                elif x < 0.9:
                    self.print_subir_apuesta(envidar_fuerte)
                    apuesta.subir_apuesta(envidar_fuerte, who)
                else:
                    self.print_tirar_ordago()
                    apuesta.tirar_ordago(who)
            else:
                self.print_tirar_ordago()
                apuesta.tirar_ordago(who)
        elif prob_ganar > 0.8:
            if apuesta.ordago:
                if x < 0.5:
                    apuesta.se_ve()
                    self.print_se_ve()
                else:
                    self.print_pasar()
                    apuesta.pasar()
            elif apuesta.apuesta_total == 1:
                if x < 0.2:
                    self.print_apostar(envidar_fuerte)
                    apuesta.subir_apuesta(envidar_fuerte - 1, who)
                else:
                    self.print_apostar(envidar_flojo)
                    apuesta.subir_apuesta(envidar_flojo - 1, who)
            elif apuesta.apuesta_total <= 4:
                if x < 0.2:
                    self.print_subir_apuesta(envidar_fuerte)
                    apuesta.subir_apuesta(envidar_fuerte, who)
                else:
                    self.print_subir_apuesta(envidar_flojo)
                    apuesta.subir_apuesta(envidar_flojo, who)
            else:
                if x < 0.3:
                    self.print_tirar_ordago()
                    apuesta.tirar_ordago(who)
                else:
                    apuesta.se_ve()
                    self.print_se_ve()
        elif prob_ganar > 0.5:
            if apuesta.ordago:
                self.print_pasar()
                apuesta.pasar()
            elif apuesta.apuesta_total == 1:
                if x < 0.2:
                    self.print_apostar(envidar_fuerte)
                    apuesta.subir_apuesta(envidar_fuerte - 1, who)
                elif x < 0.8:
                    self.print_apostar(envidar_flojo)
                    apuesta.subir_apuesta(envidar_flojo - 1, who)
                else:
                    self.print_pasar()
                    apuesta.pasar()
        else:
            self.print_pasar()
            apuesta.pasar()

        return apuesta

    def _modo_agresivo(self, apuesta: Apuesta, prob_ganar: float, who: int) -> Apuesta:
        x = random()
        envidar_fuerte = choice([4, 5, 6, 7])
        envidar_flojo = choice([2, 3, 4])

        if prob_ganar > 0.85:
            if apuesta.ordago:
                apuesta.se_ve()
                self.print_se_ve()
            elif apuesta.apuesta_total == 1:  # Envidar fuerte 80%, flojo 10%, ordago 10%
                if x < 0.1:
                    self.print_apostar(envidar_flojo)
                    apuesta.subir_apuesta(envidar_flojo - 1, who)
                elif x < 0.9:
                    self.print_apostar(envidar_fuerte)
                    apuesta.subir_apuesta(envidar_fuerte - 1, who)
                else:
                    self.print_tirar_ordago()
                    apuesta.tirar_ordago(who)
            elif apuesta.apuesta_total <= 10:
                if x < 0.1:
                    self.print_subir_apuesta(envidar_flojo)
                    apuesta.subir_apuesta(envidar_flojo, who)
                elif x < 0.9:
                    self.print_subir_apuesta(envidar_fuerte)
                    apuesta.subir_apuesta(envidar_fuerte, who)
                else:
                    self.print_tirar_ordago()
                    apuesta.tirar_ordago(who)
            else:
                self.print_tirar_ordago()
                apuesta.tirar_ordago(who)
        elif prob_ganar > 0.7:
            if apuesta.ordago:
                if x < 0.5:
                    apuesta.se_ve()
                    self.print_se_ve()
                else:
                    self.print_pasar()
                    apuesta.pasar()
            elif apuesta.apuesta_total == 1:
                if x < 0.2:
                    self.print_apostar(envidar_fuerte)
                    apuesta.subir_apuesta(envidar_fuerte - 1, who)
                else:
                    self.print_apostar(envidar_flojo)
                    apuesta.subir_apuesta(envidar_flojo - 1, who)
            elif apuesta.apuesta_total <= 4:
                if x < 0.2:
                    self.print_subir_apuesta(envidar_fuerte)
                    apuesta.subir_apuesta(envidar_fuerte, who)
                else:
                    self.print_subir_apuesta(envidar_flojo)
                    apuesta.subir_apuesta(envidar_flojo, who)
            else:
                if x < 0.3:
                    self.print_tirar_ordago()
                    apuesta.tirar_ordago(who)
                else:
                    apuesta.se_ve()
                    self.print_se_ve()
        elif prob_ganar > 0.4:
            if apuesta.ordago:
                self.print_pasar()
                apuesta.pasar()
            elif apuesta.apuesta_total == 1:
                if x < 0.7:
                    self.print_apostar(envidar_fuerte)
                    apuesta.subir_apuesta(envidar_fuerte - 1, who)
                else:
                    self.print_apostar(envidar_flojo)
                    apuesta.subir_apuesta(envidar_flojo - 1, who)
            elif apuesta.apuesta_total <= 4:
                apuesta.se_ve()
                self.print_se_ve()
            else:
                if x < 0.75:
                    self.print_tirar_ordago()
                    apuesta.tirar_ordago(who)
                else:
                    self.print_pasar()
                    apuesta.pasar()
        else:
            self.print_pasar()
            apuesta.pasar()

        return apuesta

    def _modo_pasivo_agresivo(self, apuesta: Apuesta, prob_ganar: float, who: int) -> Apuesta:
        x = random()

        if prob_ganar > 0.75:
            if apuesta.ordago:
                apuesta.se_ve()
                self.print_se_ve()
            else:
                self.print_tirar_ordago()
                apuesta.tirar_ordago(who)
        elif prob_ganar > 0.5:
            if apuesta.ordago:
                if x > 0.7:
                    apuesta.se_ve()
                    self.print_se_ve()
                else:
                    self.print_pasar()
                    apuesta.pasar()
            else:
                self.print_tirar_ordago()
                apuesta.tirar_ordago(who)
        else:
            self.print_pasar()
            apuesta.pasar()

        return apuesta
