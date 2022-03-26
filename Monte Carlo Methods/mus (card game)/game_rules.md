# Mus Rules
The following rules are a simplification of the original card game _mus_ in order to be able to implemenent an AI based on 
Monte Carlo Methods.

### Deck of cards
A 40 card Spanish deck. Threes are considered kings ("R", of _rey_) and twos are aces.

```
DECK = ["R", "R", "R", "R", "R", "R", "R", "R",
        "1", "1", "1", "1", "1", "1", "1", "1",
        "4", "4", "4", "4",
        "5", "5", "5", "5",
        "6", "6", "6", "6",
        "7", "7", "7", "7",
        "S", "S", "S", "S",
        "C", "C", "C", "C"]
```

Threes ("3") are considered kings ("R", of _rey_) and deuces aces.

### Number of players
Two players.

### Order and value of the cards
The order of the cards, from highest to lowest, is: king or three ("R"), knight ("C" of _caballo_), jack 
("S" of _sota_), seven, six, five, four and deuce or ace. There are no trumps or differences between the suits.

The value of the cards, in any of the four suits, is as follows: each king, three, knight or jack is worth 10 points; 
the other cards, their natural value represented by the pips, except the deuces, which, like the aces, are worth one 
point. The kings have the same value as the threes, and the deuces are equal to the aces, which is equivalent to playing 
with 8 kings and 8 aces.

`VALUES = {"R": 10, "C": 10, "S": 10, "7": 7, "6": 6, "5": 5, "4": 4, "1": 1}`
### Dealing the cards
Four cards are dealt to each player.

### Betting
Each player, with their 4 cards, can make the following bets:

* **High (Grande)**: Consisting in having the highest cards possible, according to their rank.
* **Low (Chica)**: The opposite to the one above, consisting in having the lowest cards possible.
* **Pairs (Pares)**: Having two or more equal cards.
    * Pair (Par): when only 2 cards are equal.
    * Trio (Medias): when 3 cards are equal.
    * Double pair (Duples): Having 2 pairs.
    
* **WindyGridworldGame (Juego)**: A player has WindyGridworldGame when the sum of the value of the four cards in their hand is 31 or more, the best 
  WindyGridworldGame being 31, followed by 32 and from here it jumps to 40, descending to 37, 36, 35, 34 and 33, which is the worst. 
  The player with the best WindyGridworldGame wins. If no player has WindyGridworldGame, i.e., if the sum of the value of the cards in each players 
  hand is less than 31, then the bet is to see who has the best Point (punto). The best Point is 30, dropping down to 4, 
  which is the worst.
  
### Announcing bets
The “hand” is the first to announce whether they wish to pass, bet (two stones) or make a bigger bet, and the 
other player in turn must state if they pass, accept the bet or increase it.

The “hand” must announce the bets in the order already established: High, Low, Pairs, WindyGridworldGame or No WindyGridworldGame. In the Pairs bet, 
when a player’s turn arrives they say whether or not they have pairs, initiating the bets that, at least, one of the 
players in each team has Pairs. WindyGridworldGame (Juego) is initiated in the same way, with each player in turning saying WindyGridworldGame 
“Yes” or “No”. If no one has WindyGridworldGame, bets are made between the players that wish to bet on the best No WindyGridworldGame (No Juego).

### Scoring
Collection of the bets is governed by the following rules:
* **High and Low** If, at the end of the partial game, all the players pass without anyone betting, the player with the 
  best High (Grande) takes one stone, and the player with the best Low (Chica) takes another stone. However, if a 
  player bets and nobody accepts their bet, this player takes one stone by way of “Deje” (not accepting the bet), which 
  immediately counts towards the score of the game.
  
* **Pairs and Mus**. If, at the end of the partial game, all the players pass without anybody betting, the player with 
  the best hand takes its corresponding value, adding these stones to any that may correspond to their partner. If a 
  player bets and no one accepts their bet, a “Deje” stone is immediately taken, and at the end of the partial game the 
  value of their hand is also taken, plus the value of their partner’s, even if their cards were worse than those of any 
  other opponent.
  
* **No Mus**. If everyone passes and there is no bet, the one with the best Point (Punto) takes a stone. If a player 
  bets Point (Punto) and nobody accepts, a “Deje” stone is immediately taken and another can be taken for the Point at 
  the end of the game, even if this was inferior to another player’s Point.
  
* Any player who renounces a bet by not accepting it, loses all right to collect the bet, even when at the end of 
  the partial game and after showing the cards it can seen that their cards were better. In any of the bets, the 
  partner who has best cards wins, even if the one who made the bet or announced Órdago has worse cards than the 
  opponent who accepted.
  
Value of the bets:

Bet  | Value (stones)
------------- | -------------
Deje (bet not accepted) | 1
High or low during pass | 1
Pair/strong | 1
Trios (medias) | 2
Double pairs (duples) | 3
Game (Juego) | 2
Game of 31 (la una) | 3
No game or Point (punto) | 1


_Original game rules: https://www.nhfournier.es/en/como-jugar/mus/_ 
