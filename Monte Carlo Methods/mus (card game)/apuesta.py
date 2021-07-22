from typing import Union
from dataclasses import dataclass


@dataclass
class Apuesta:
    """
    La clase irá actualizando su estado. Por tanto, solamente es necesario instanciar una clase de este tipo una vez
    por cada lance.
    """

    # La apuesta acumulada acordada o no. Si es uno significa que no ha habido apuesta anterior
    apuesta_total: int = 1

    apuesta_previa: int = 1

    # Si se ha tirado ordago o no
    ordago: bool = False

    # Si se ha visto o no la apuesta o si alguien ha rechazado la apuesta del rival. Ambos casos se pueden distinguir
    # atendiendo al atributo 'ganador', si está en None siginifica que se ha visto, etc
    acuerdo: bool = False

    # Con ganador nos referimos a la persona que ha hecho una apuesta que ha sido rechazada por el rival.
    # Si se ha visto la apuesta no hay ganador (None)
    ganador: Union[None, int] = None

    # El número de veces que se han utilizado algunos de los métodos de la clase más el número de veces que se ha
    # pasado. Sirve para ser capaces de identificar si un 'paso' se ha realizado antes que ninguna otra opión
    n_acciones: int = 0

    def subir_apuesta(self, n: int, who: int):
        self.apuesta_previa = self.apuesta_total
        self.apuesta_total += n
        self.ganador = who
        self.acuerdo = False
        self.n_acciones += 1

    def se_ve(self):
        self.acuerdo = True
        self.ganador = None
        self.n_acciones += 1

    def tirar_ordago(self, who: int):
        self.apuesta_previa = self.apuesta_total
        self.ordago = True
        self.ganador = who
        self.acuerdo = False
        self.n_acciones += 1

    def pasar(self):
        self.acuerdo = True
        self.n_acciones += 1


if __name__ == "__main__":
    pass
