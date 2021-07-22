# Reglas del juego
Estas reglas son una simplificación del juego original _mus_. El objetivo es poder aplicar métodos de
Monte Carlo.

### Baraja
Se juega con la baraja española. Los treses se consideran reyes y los doses ases. A los doses y los ases se les denomina 
pitos

```
BARAJA = ["R", "R", "R", "R", "R", "R", "R", "R",
         "1", "1", "1", "1", "1", "1", "1", "1",
         "4", "4", "4", "4",
         "5", "5", "5", "5",
         "6", "6", "6", "6",
         "7", "7", "7", "7",
         "S", "S", "S", "S",
         "C", "C", "C", "C"]
```

### Número de jugadores
Dos jugadores (el juego original es con cuatro).

### Orden y de las cartas
El orden de las cartas, de menor a mayor, es: reyes (incluidos los treses), caballo, sota, 7, 6, 5, 4, pitos (2 y ases).

### Dealing the cards
Four cards are dealt to each player.

### Betting
Each player, with their 4 cards, can make the following bets:

* **Grande**: Gana quien tenga la carta más alta. En caso de empate se mira la segunda más alta, y así sucesivamente.
* **Chica**: Gana quien tenga la carta más baja. En caso de empate se mira la segunda más baja, etc.
  
### Anunciando las apuestas
El “mano” es el primero en anunciar si desea pasar, envidar (dos puntos) o hacer una apuesta más grande. El otro jugador
debe decidir si pasa, la ve, o sube la apuesta y así sucesivamente.

### Puntuación
Si, al final de una ronda, todos los jugadores han pasado, el jugador que hubiese ganado de haberse visto una apuesta 
gana un punto. Sin embargo, si un jugador sube o realiza una apuesta y el rival no la acepta, se considera de la misma 
manera que si este hubiese ganado la apuesta previa, llevándose una piedra si no había nínguna. Por ejemplo, si el 
jugador A decide apostar 4, el jugador 2 sube la apuesta a 6 y el jugador A la rechaza, el jugador B ganaría 4 puntos 
inmediatamente.


_Original game rules: https://www.nhfournier.es/en/como-jugar/mus/_ 