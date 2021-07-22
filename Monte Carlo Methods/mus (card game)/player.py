from typing import Union
from apuesta import Apuesta
import abc


class Player(abc.ABC):
    cartas: Union[list[str], None]
    mano: Union[bool, None]
    nombre: str

    def __init__(self, name="player"):
        self.nombre = name
        self.cartas = None
        self.mano = None

    def __str__(self):
        return self.nombre

    @abc.abstractmethod
    def pedir_apuesta(self, apuesta, who, lance) -> Apuesta:
        pass


class Human(Player):

    def __init__(self, name="Player 1"):
        super().__init__(name)

    def preguntar_nombre(self):
        self.nombre = input("Introduce tu nombre: ")

    def pedir_apuesta(self, apuesta: Apuesta, who: int = 1, lance: int = 0) -> Apuesta:
        """
        Esta función pide una apuesta al jugador. Tiene en cuenta lo apostado previamente para hacer las preguntas
        correctas. Devuelve lo que el jugador ha apostado.
        """
        # ¿ordago?
        if apuesta.ordago:
            ver = -1
            while ver < 0:
                try:
                    ver = int(input("¿Desea ver el órdago?(0=No, 1=Sí) "))
                except ValueError:
                    print("Debes introducir '1' o '0'")
            if ver:
                apuesta.se_ve()
                return apuesta
            else:  # Quiere pasar
                apuesta.pasar()
                return apuesta

        elif apuesta.apuesta_total == 1:  # No ha habido apuesta anterior -> no se puede ver
            # ¿pasa?
            pasar = -1
            while pasar < 0:
                try:
                    pasar = int(input("¿Desea pasar?(0=No, 1=Sí) "))
                except ValueError:
                    print("Debes introducir '1' o '0'")
            if pasar:  # No desea apostar

                # Esto es necesario hacerlo porque si se es el primer jugador en pasar,
                # el segundo jugador aun tiene la opción de apostar
                if apuesta.n_acciones > 0:
                    apuesta.pasar()
                apuesta.n_acciones += 1
                return apuesta
            else:  # Desea apostar
                ordago = -1
                while ordago < 0:  # ¿ordago?
                    try:
                        ordago = int(input("¿Desea tirar un órdago?(0=No, 1=Sí) "))
                    except ValueError:
                        print("Debes introducir '1' o '0'")
                if ordago:
                    apuesta.tirar_ordago(who)
                    return apuesta
                else:  # No quiere ordago, solo apostar
                    apuesta_inicial = 0
                    while apuesta_inicial < 2:
                        try:
                            apuesta_inicial = int(input(f"¿Cuánto desea apostar? "))
                            if apuesta_inicial == 1:
                                print("¡Al menos debes apostar 2!")
                        except ValueError:
                            print("Debes introducir un número natural (apuesta mínima 2)")

                    apuesta.subir_apuesta(apuesta_inicial - 1, who)
                    return apuesta

        else:  # Ha habido apuesta anterior
            # ¿pasa?
            subir = -1
            while subir < 0:
                try:
                    subir = int(input("¿Desea subir la apuesta?(0=No, 1=Sí) "))
                except ValueError:
                    print("Debes introducir '1' o '0'")
            if not subir:  # No desea apostar más
                if apuesta.ganador is None:  # Si el anterior ha pasado
                    return apuesta
                ver = -1
                while ver < 0:
                    try:
                        ver = int(input(f"(Apuesta actual: {apuesta.apuesta_total})"
                                        "¿Desea ver la apuesta?(0=No, 1=Sí) "))
                    except ValueError:
                        print("Debes introducir '1' o '0'")
                if ver:  # Quiere ver la puesta
                    apuesta.se_ve()
                    return apuesta
                else:  # Quiere pasar
                    apuesta.pasar()
                    return apuesta
            else:  # Desea apostar
                ordago = -1
                while ordago < 0:  # ¿ordago?
                    try:
                        ordago = int(input("Desea tirar un órdago (0=No, 1=Sí) "))
                    except ValueError:
                        print("Debes introducir '1' o '0'")
                if ordago:  # quiere ordago
                    apuesta.tirar_ordago(who)
                    return apuesta
                else:  # No quiere ordago, solo apostar
                    delta = 0
                    while delta <= 0:
                        try:
                            delta = int(input(f"(Apuesta actual {apuesta.apuesta_total})"
                                              "¿Cuánto desa subir la apuesta? "))
                        except ValueError:
                            print("Debes introducir un número natural mayor que 0")
                    apuesta.subir_apuesta(delta, who)
                    return apuesta
