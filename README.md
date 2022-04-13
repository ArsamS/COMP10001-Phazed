<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">COMP10001 Phazed</h3>
</div>



<!-- TABLE OF CONTENTS -->
<details>
<summary>Table of Contents</summary>
  

  
</details>

## 1. About The Project
This was the second project for COMP10001 (Foundations of Computing) at the University of Melbourne. Descriptions for various functions were provided via Grok Learning and checked against various inputs. The <a href="#project-description">Project Description</a> and <a href="#function-descriptions">Function Descriptions</a> will be below. <b> Final mark: 94% </b>

<p align="right">(<a href="#top">back to top</a>)</p>

## 2. Project Description
### Background
In this project, you will implement a program that plays a game called “Phazed”, which is a variant of Phase 10, which is in turn a variant of rummy. Why a variant? Because Tim can’t help himself ... or more seriously, because Tim wanted to come up with a version that was more compatible with a computational implementation (e.g. not too long, and suitably algorithmically complex).
We will play Phazed with two standard decks of 52 cards each (i.e. 104 cards in total). Each card has a “suit” (Spades, Clubs, Hearts, Diamonds) as well as a “value” (numbers 2 to 10, as well as Jack, Queen, King and Ace).

  <hr></hr>
  
### The Rules of Phazed
#### Overview
Phazed is a 4-player game where the objective is to be the first to complete a series of “phases” by placing particular combinations of cards on the table. The game is broken down into a series of “hands”, in each of which, the 4 players are dealt 10 cards each from a 104 card deck, and take it in turns either drawing a card from the face-down deck, or picking up the top card from the discard pile. When they have the requisite cards to complete a given phase, on their turn, they place those cards on the table, and optionally place any remaining cards on any group that has been placed on the table (their own or groups of other players). For a given hand, play continues until one of the following occurs: (1) a player places all of their cards on the table; (2) the deck is exhausted; or (3) each player has played 50 times. At the point that one of these occurs, players tally up penalty points based on the cards remaining in their hand. The game continues across multiple hands until either: (1) a player has completed all of their phases; or (2) 20 hands have been completed. In the former case, the winner is the player who completed all of their phases (or the player(s) with the lowest point score who have completed all phases, in the case of a tie); in the latter case, the player(s) with the lowest point score win.

The full details of the deal, how cards are drawn and played, and how phases work, are outlined in the following sections.

#### The Deal
The sequence of play is fixed throughout the game (based on clockwise sequence between the players), but the dealing of cards for each phase rotates between players (also clockwise, by one player per deal), and the lead player for each phase also rotates, with the player to the left of the dealer leading. The dealer shuffles the combined deck, deals out 10 cards to each of the 4 players, places the top card of the remaining deck face up in the middle of the table (to form the “discard” pile), and places the remainder of the deck face down next to it.

#### A Single Turn
On their turn, a player performs the following actions:
1. picks up either the top card from the discard pile, or the top card from the deck
2. optionally plays cards from their hand to make up a complete phase. Note that only one phase can be played for a given hand, and that a complete phase must be played at once (i.e. it is not possible to play part of a phase with one play, and the remainder with a later play)
3. assuming that the player has completed their phase for the hand, optionally plays other cards on whatever groups of cards have been played on the table (for any player, including their own groups)
4. assuming the player still has at least one card left in their hand, they place a single card face up in the discard pile

#### Card Combination Types for Phases

The phases that a player must complete are made up of the following card combinations:
*	a “set” of N cards of the same value: N cards of the same value, of any suit (e.g.	`['2S',	'2S',	'2H']` is a set of 3 cards)			
*	a “set” of N cards of the same suit: N cards of the same suit, of any values (e.g.	`['2C',	'7C',	'7C', '8C', 'JC', 'QC', 'KC']` is a set of 7 Clubs)
*	a “run” of N cards: a consecutive sequence of N cards (of any combination of suits/colours), based on value (e.g. `['2S', '3D', '4C', '5D', '6C', '7D', '8H']` is a run of 7 cards); note that, for the purpose of runs, Jacks, Queens and Kings take on the values 11, 12 and 13, resp., and runs can wrap around from 13 to 2 (e.g. `['KH', '2S', '3D', '4C', '5D']` is a valid run of 5 cards)
*	a “run” of N cards of the same colour: a run of N cards where all cards are of the same colour, as defined by the suit (Spades and Clubs are black, and Hearts and Diamonds are red; e.g. `['2S', '3C', '4C', '5S']` is a run of 4 black cards); once again, runs of the same colour can loop around from 13 to 2 (e.g. `['KC', '2S', '3C', '4C', '5S']` is a valid run of the same colour, of length 5 cards)
* an “N-accumulation” of cards: cards of any suit/colour which add up to N in terms of their combined value (e.g. `['KS', '0D', '8C', '3S']` is a 34-accumulation); for the purpose of accumulations, Jacks, Queens and Kings take on the values 11, 12 and 13, resp., and Aces take on the value 1
* an “N-accumulation” of cards of the same colour: cards of a given colour (all red or all black) which add up to N in terms of their combined value (e.g. `['KS', '0C', '8C', '3S']` is a 34-accumulation of black cards)

To win the game, a player must complete the following phases, in the sequence indicated:

1.	Phase 1: two sets of three cards of the same value (e.g. `[['2S', '2S', '2H'], ['7H', '7S','7D']]`)
2.	Phase 2: one set of seven cards of the same suit (e.g. `[['2C', '7C', '7C', '8C', 'JC', 'QC', 'KC']]`)
3.	Phase 3: two accumulations of cards, each of value 34 (e.g. `[['KS', '0D', '8C', '3S'], ['9D', '9S', '9S', '6C', 'AH']]`)
4.	Phase 4: two sets of four cards of the same value (e.g. `[['2S', '2S', '2H', '2D'], ['7H', '7S', '7D',	'7D']]`)
5.	Phase 5: one run of eight cards (e.g. `[['2S', '3D', '4C', '5D', '6C', '7D', '8H', '9S']]`)
6.	Phase 6: two accumulations of cards of the same colour, each of value 34 (e.g. `[['KS', '0C', '8C','3S'],	['9C',	'9S',	'9S',	'6C',	'AS']]`)
7.	Phase 7: one run of four cards of one colour + one set of four cards of the same value (e.g. `[['KC', '2S', '3C',	'4C'],	['7C',	'7S',	'7D',	'7D']]`)

#### Playing Cards on Groups
Once a player has played the necessary phase for the hand, they may play any number of cards from their hand onto any group that is on the table, consistent with the composition of that group. That is:
•	for a set of cards of the same value, an additional card of the same value (e.g. '2C' on `['2S', '2S', '2H']`)
•	for a run, a card which continues the sequence (e.g. '9D' on `['2S', '3D', '4C', '5D', '6C', '7D', '8H']`)
•	for a set of cards of a given suit, a card of the same suit (e.g. '4C' on `['2C', '7C', '7C', '8C', 'JC', 'QC', 'KC']`)
•	for a run of cards of a given colour, a card which continues the sequence of that same colour (e.g. '6S' on `['2S', '3C', '4C', '5S'`]
•	for an accumulation of cards, an accumulation via series of plays in a single turn such that the total value of the cards is equal to 21, 13, 8, 5, 3, 2, 1, or 1 for the first, second, etc. (series of) plays, that is the value determined by the decreasing Fibonacci sequence from 34 down, noting that from the second accumulation series of plays to an accumulation (i.e. 13 and onwards), the accumulation can consist of a single card, and that in a single turn, a player can complete multiple items in the sequence, e.g. first play card(s) totalling 13, then play card(s) totalling 8. For example, it would be possible to play the cards '9S' and then 'QH' to the accumulation `['KS', '0D', '8C', '3S']`. This series of card values (21, 13, ...) is shared across all players, such that if Player A plays cards totalling 21 to an accumulation, the next play to that group from any player (Player A or otherwise) must total 13, for example. In the case that the accumulation is of the same colour, any additional cards played to that accumulation must also be of that colour.

Note that this can only take place once a given player has completed their phase for the hand. A player may play as many cards as they want in a given turn, including in the case that they played their phase in that turn.

In the case of a run, players can continue to build on the group only until it cycles around (i.e. is made up of 12 cards, with strictly one card representing each value), whereas there is no such constraint for the other group types (e.g. a set of cards of the same value can include up to 16 elements — the eight cards of that value, and eight Wild cards; see the comments on Wild cards in the next section).

#### Special Cards


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/arsamsamadi/
