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
  
- [1. About The Project](#1-about-the-project)
- [2. Project Description](#2-project-description)
  * [Background](#background)
  * [The Rules of Phazed](#the-rules-of-phazed)
    + [Overview](#overview)
    + [The Deal](#the-deal)
    + [A Single Turn](#a-single-turn)
    + [Card Combination Types for Phases](#card-combination-types-for-phases)
    + [Playing Cards on Groups](#playing-cards-on-groups)
    + [Special Cards](#special-cards)
    + [The End of a Hand](#the-end-of-a-hand)
- [3. Function Descriptions](#3-function-descriptions)
  * [Question 1. Finding Group Types](#question-1-finding-group-types)
  * [Question 2. Finding Phase Types](#question-2-finding-phase-types)
  * [Question 3. Determining if a play is valid](#question-3-determining-if-a-play-is-valid)
  * [Question 4. Returning score](#question-4-returning-score)
  * [Question 5. Determining best play](#question-5-determining-best-play)
  
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
Phazed includes “Wild” cards (×8), in the form of any Ace (e.g. 'AS'), which can take on any value or suit (except for accumulations, where they take the value 1).3 The particular value and suit of the wild is determined by the phase they are played as part of, and may be underspecified, e.g. in the case of the run of seven cards `['2S', '3D', '4C', 'AD', '6C', '7D', '8H']`, where 'AD' is playing the role of a five, but the suit is underspecified. Once played, however, the value/suit of the wild card at the time of play cannot be changed through subsequent plays (e.g. it would not be possible to play '5D' on `['2S', '3D', '4C', 'AD', '6C', '7D', '8H'`] and reclassify 'AD' as a nine). Note that, for runs, an Ace can only be played as a stand-in for values 2–13 (i.e. it can’t be used as value 1 or value 14). Additionally, in any given group, there must be at least two “natural” (= non-Wild) cards, e.g. `['2C', '2S', 'AC']` is a valid set of three cards of the same value (3× Twos), but `['2C', 'AS', 'AC']` is not, as it is made up of only one natural card.

#### The End of a Hand
A hand ends when: (a) a player has played all of their cards (meaning they must also have completed a phase), either by discarding their last card, or by playing their last card to a set; (b) the deck has been exhausted; or (c) each player has played 50 times. In the latter two cases, the hand ends at the point that the player who drew the last card discards.

At the end of a hand, the score for each player is determined based on the cards remaining in their hand, as follows:
*	for cards Two up to Ten, the score is the face value of the card (i.e. 2–10, resp.)
*	for the Jack, Queen and King, the score is 11, 12 and 13, resp.
*	for Aces, the score is 25
For example, if a player holds `['3D', 'JC', 'AS']` at the end of the hand, their score would be 3+11+25 = 39. The player score accumulates over the hands that make up a game.

## 3. Function Descriptions
### Question 1. Finding Group Types

Write a function called `phazed_group_type` that takes the following single argument:

`group`
* A group of cards in the form of a list, each element of which is a 2-character string with the value (drawn from '234567890JQKA') followed by the suit (drawn from 'SHDC'), e.g. ['2C', '2S', '2H'] represents a group of three cards, made up of the Two of Clubs, the Two of Spades, and the Two of Hearts. 

The function should return a sorted list of integers indicating card combination types as specified below, in the case that group is a valid instance of one or more of the following combinations of cards (and the empty list in the instance that it doesn't correspond to any valid card combination). Note that the combination of cards in its entirety must satisfy the requirements of the combination definition, such that ['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC'] is not a valid set of three cards of the same value, e.g., as it is made up of seven cards (despite the fact that it contains ['2C', '2C', 'AH'] which is a valid set of three cards of the same value).

1. A set of three cards of the same value, e.g. ['2C', '2S', '2H'] represents a set of three Twos. Note that the set may include Wilds, but must include at least two "natural" cards (i.e. non-Wild cards), which define the value. Note also that the sequence of the cards is not significant for this group type. 
2. A set of seven cards of the same suit, e.g. ['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC'] represents a set of seven Clubs. Note that the set may include Wilds (as we see in our example, with the Ace of Hearts), but must include at least two "natural" cards (i.e. non-Wild card), which define the suit. Note also that the sequence of the cards is not significant for this group type. 
3. A set of four cards of the same value, e.g. ['4H', '4S', 'AC', '4C'] represents a set of four Fours. Note that the set may include Wilds (as we see in our example, with the Ace of Clubs), but must include at least two "natural" cards (i.e. non-Wild cards), which define the value. Note also that the sequence of the cards is not significant for this group type. 
4. A run of eight cards, e.g. ['4H', '5S', 'AC', '7C', '8H', 'AH', '0S', 'JC'] represents a run of eight cards. Note that the card combination may include Wilds (as we see in our example, with the Ace of Clubs standing in for a Six and the Ace of Hearts standing in for a Nine), but must include at least two "natural" cards (i.e. non-Wild cards). Note also that the sequence of the cards is significant for this group type, and that ['4H', '5S', 'AC', '8H', '7C', 'AH', '0S', 'JC'], e.g., is not a valid run of eight, as it is not in sequence. 
5. A run of four cards of the same colour, e.g. ['4H', '5D', 'AC', '7H'] represents a run of four Red cards. Note that the card combination may include Wilds (as we see in our example, with the Ace of Clubs standing in for a Red Six), but must include at least two "natural" cards (i.e. non-Wild cards), which define the colour. Note also that the sequence of the cards is significant for this group type, and that ['4H', '5D', '7H', 'AC'] is not a valid run of four cards of the same colour, as it is not in sequence. 
6. A 34-accumulation of cards, that is an accumulation of cards totalling 34 in value, e.g. ['KS', '0D', '8C', '3S']. Note that for accumulations, Aces do not function as Wilds, and simply take the value 1. 
7. A 34-accumulation of cards of the same colour, that is an accumulation of cards of the same colour totalling 34 in value, e.g. ['KS', '0C', '8C', '3S']. Note that for accumulations, Aces do not function as Wilds, and simply take the value 1. 

Example calls to the function are:
```
>>> phazed_group_type(['2C', '2S', '2H'])
[1]
>>> phazed_group_type(['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC'])
[2]
>>> phazed_group_type(['4H', '4S', 'AC', '4C'])
[3]
>>> phazed_group_type(['4H', '5S', 'AC', '7C', '8H', 'AH', '0S', 'JC'])
[4]
>>> phazed_group_type(['4H', '5D', 'AC', '7H'])
[5]
>>> phazed_group_type(['KS', '0D', '8C', '3S'])
[6]
>>> phazed_group_type(['KS', '0C', '8C', '3S'])
[6, 7]
>>> phazed_group_type(['2C', '2C', '4C', 'KC', '9C', 'AS', '3C'])
[2, 6, 7]
>>> phazed_group_type(['4H', '5D', '7C', 'AC'])
[]
```
<hr>

### Question 2. Finding Phase Types
Write a function called phazed_phase_type that takes the following single argument:

`phase`
* A combination of card groups in the form of a list of lists of cards, where each card is a 2-character string with the value (drawn from '234567890JQKA') followed by the suit (drawn from 'SHDC'), e.g. [['2C', '2S', '2H'], ['7H', '7C', 'AH']] represents an instance of two sets of three cards of the same value, as it is made up of two groups, each of which is a set of three cards of the same value. 

The function should return a sorted list composed of the following values, indicating the type(s) of the combinations of card groups contained in phase, with an invalid combination indicated by the empty list:

1. Two sets of three cards of the same value, e.g. [['2C', '2S', '2H'], ['7H', '7C', 'AH']] represents a set of three Twos and three Sevens. Note that each set may include Wilds (as we see in our example, with the Ace of Hearts), but must include at least two "natural" cards (i.e. non-Wild cards), which define the value. 
2. One set of 7 cards of the same suit, e.g. [['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC']] represents a single set of seven Clubs. Note that the set may include Wilds (as we see in our example, with the Ace of Hearts), but must include at least two "natural" cards (i.e. non-Wild cards), which define the suit. 
3. Two 34-accumulations, e.g. [['2C', 'KH', 'QS', '7H'], ['3H', '7S', '0D', 'KD', 'AD']], noting that there is no restriction on the suits/colours of cards in either accumulation. 
4. Two sets of four cards of the same value, e.g. [['4H', '4S', 'AC', '4C'], ['7H', '7C', 'AH', 'AC']] represents a set of four Fours and a set of four Sevens. Note that each set may include Wilds (as we see in our example, with the two Aces of Clubs and Ace of Hearts), but must include at least two "natural" cards (i.e. non-Wild cards), which define the value. 
5. One run of eight cards, e.g. [['4H', '5S', 'AC', '7C', '8H', 'AH', '0S', 'JC']] represents a single run of eight cards. Note that the set may include Wilds (as we see in our example, with the Ace of Clubs standing in for a Six and the Ace of Hearts standing in for a Nine), but must include at least two "natural" cards (i.e. non-Wild cards). Note also that the sequence of the cards is significant for this group type, and that [['4H', '5S', 'AC', '8H', '7C', 'AH', '0S', 'JC']], e.g., is not a valid instance of this phase type, as the run is not in sequence. 
6. Two 34-accumulations of the same colour, e.g. [['2C', 'KC', 'QS', '7C'], ['3H', '7H', '0D', 'KD', 'AD']], noting that while each accumulation must be a single colour, the two accumulations do not have to match in colour. 
7. A run of four cards of the same colour and a set of four cards of the same value, e.g. [['4H', '5D', 'AC', '7H'], ['7H', '7C', 'AH', 'AS']] represents a run of four Red cards and a set of four Sevens. Note that each set may include Wilds (as we see in our example, with the Ace of Clubs standing in for a Red Six, and Ace of Hearts and Ace of Spaces standing in for Sevens), but must include at least two "natural" cards (i.e. non-Wild cards), which define the colour/value. Note also that the sequence of the cards within the run is significant for this group type, and also that the sequence of the two groups is significant, in that the run must come before the set of four. 

Example calls to the function are:
```
>>> phazed_phase_type([['2C', '2S', '2H'], ['7H', '7C', 'AH']])
[1]
>>> phazed_phase_type([['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC']])
[2]
>>> phazed_phase_type([['2C', 'KH', 'QS', '7H'], ['3H', '7S', '0D', 'KD', 'AD']])
[3]
>>> phazed_phase_type([['4H', '4S', 'AC', '4C'], ['7H', '7C', 'AH', 'AC']])
[4]
>>> phazed_phase_type([['4H', '5S', 'AC', '7C', '8H', 'AH', '0S', 'JC']])
[5]
>>> phazed_phase_type([['2C', 'KC', 'QS', '7C'], ['3H', '7H', '0D', 'KD', 'AD']])
[3, 6]
>>> phazed_phase_type([['4H', '5D', 'AC', '7H'], ['7H', '7C', 'AH', 'AS']])
[7]
>>> phazed_phase_type([['4H', '5D', '7C', 'AC'], ['AC', 'AS', 'AS']])
[]
```
<hr>

### Question 3. Determining if a play is valid
Write a function called `phazed_is_valid_play` that takes the following arguments:

`play`
* A 2-tuple indicating the play type, and the content of the play, as follows:

    1. Pick up a card from the top of the deck at the start of the player's turn, with the play content being the card that was picked up (e.g. (1, 'JS')). 
    2. Pick up a card from the top of the discard pile at the start of the player's turn, with the play content being the card that was picked up (e.g. (2, '2C')). 
    3. Place a phase to the table from the player's hand, with the play content being a 2-tuple containing the intended phase ID (as an integer, based on the IDs from Q2) and actual phase (as a list of groups) (e.g. (3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]))). 
    4. Place a single card from the player's hand to a phase on the table, with the play content being a 2-tuple made up of the card the player is attempting to play, and the position they are attempting to play it in, itself in the form of a 3-tuple indicating: (1) the player ID of the phase the card is to be placed on; (2) the group within the phase the card is to placed in; and (3) the index of the position within the group the card is to be played to. For example, (4, ('AD', (1, 0, 3))) indicates that an Ace of Diamonds is to be placed on the phase of Player 1, in Group 0 and index position 3 (i.e. it will be the fourth card in the first Group). 
    5. Discard a single card from the player's hand, and in doing so, end the turn (e.g. (5, 'JS') indicates that a Jack of Spades is to be discarded). 

`player_id`
* An integer between 0 and 3 inclusive, indicating the ID of the player attempting the play. 

`table`
* A 4-element list of phase plays for each of Players 0—3, respectively. Each phase play is in the form of a 2-tuple indicating the phase content (as an integer or None, consistent with the output of phazed_phase_type) and a list of lists of cards (of the same format as for phazed_phase_type, but possibly with extra cards played to each of the groups in the phase). An empty phase for a given player will take the form (None, []). As an example of a full 4-player table, [(None, []), (1, [['2S', '2S', '2C'], ['AS', '5S', '5S', '5D']]), (None, []), (None, [])] indicates that Players 0, 2 and 3 are yet to play a phase for the hand, and Player 1 has played Phase 1, in the form of a set of Twos and a set of Fives, the latter of which has had one extra card added to it. 

`turn_history`
* A list of all turns in the hand to date, in sequence of play. Each turn takes the form of a 2-tuple made up of the Player ID and the list of individual plays in the turn (based on the same format as for play above, with the one difference that for any draws from the deck, the card is indicated as 'XX' (as it is not visible to other players). For example, [(0, [(2, 'JS'), (5, 'JS')]), (1, [(2, 'JS'), (3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]))])] indicates that the hand to date is made up of two turns, on the part of Players 0 and 1, respectively. Player 0 first drew the Jack of Spades from the discard pile, then discarded the Jack of Spades (presumably they had a change of heart!). Player 1 then picked up the Jack of Spades from the discard pile, and played a phase, in the form of two sets of three cards of the same value (i.e. Phase 1). 

`phase_status`
* A 4-element list indicating the phases that each of Players 0—3, respectively, have achieved in the game. For example, [0, 4, 0, 0] indicates that Players 0, 2 and 3 have not got any phases, but Player 1 has achieved up to Phase 4. At the start of a game, this is initialised to [0, 0, 0, 0]. 

`hand`
* The list of cards that the current player holds in their hand, each of which is in the form of a 2-element string. 

`discard`
* The top card of the discard stack, in the form of a 2-element string (e.g. '3D') or None in the case the discard pile is empty (e.g. if the first player picks up from the discard pile and hasn't finished their turn). 

Your function should return True if play is valid relative to the current hand state, and False otherwise. For a play to be "valid", the following conditions must be met:

1. if the play is a pick-up play from the deck or discard pile, it must be the first play of the turn (and the card the player is attempting to pick up from the discard pile must match the actual card on the discard pile, e.g.)
2. a phase play must match the declared phase type, must be the phase type that the player is required to play for the current hand, must occur after picking up a single card from the deck or discard pile, the player cannot have played a phase already in the current hand, and must hold all cards in the attempted phase play
3. a play to the table must happen after picking up a card from the deck or discard pile, can only happen if the player has played their phase in the current hand, must be of a card they hold in their hand, and must be consistent (in terms of value, suit, and position) with the group type the player is attempting to play to (e.g. building on either end of a run; see below for comments on plays to accumulations)
4. an attempt to discard a card and end the turn must have been preceded by a pick-up play, must be of a card the player holds, and requires that any accumulations the player has played to in that turn are "complete" (see below)

You may assume that the game state will be consistent at the start of the turn (i.e. all groups on the table will be correctly constituted, and any accumulations will be "complete", in the sense of totalling 34, 34 + 21 = 55, 34 + 21 + 13 = 68, etc. points). A single play to an accumulation must either result in a "complete" accumulation (a total value of 34, 55, 68, etc.), or a value less than the lowest value required to complete the accumulation relative to the value at the start of the play (e.g. if the original value is 43, only cards of value 1–12 can be added, such that the total is ≤ 55; the reason for this is that any plays to an accumulation in a single turn must build it to the next value in the additive sequence, and as long as it is less than 55, it is possible that extra cards can be added to get to 55 in subsequent plays in the given turn). If the play to an accumulation is of the last card the player holds, the accumulation must be completed for the play to be valid, but if the player still holds cards, there is no need to check whether it is theoretically possible to complete the accumulation using the remaining cards (that check happens at the point of the final card play in the turn).

Example calls to the function are:
```
>>> phazed_is_valid_play((3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']])), 0, [(None, []), (None, []), (None, []), (None, [])], [(0, [(2, 'JS')])], [0, 0, 0, 0], ['AS', '2S', '2S', '2C', '5S', '5S', '7S', '8S', '9S', '0S', 'JS'], None)
True
>>> phazed_is_valid_play((4, ('KC', (1, 0, 0))), 1, [(None, []), (2, [['2S', '2S', 'AS', '5S', '5S', '7S', 'JS']]), (None, []), (None, [])], [(0, [(2, 'JS'), (5, 'JS')]), (1, [(1, 'XX'), (3, (2, [['2S', '2S', 'AS', '5S', '5S', '7S', 'JS']]))])], [0, 2, 0, 0], ['5D', '0S', 'JS', 'KC'], 'JS')
False
>>> phazed_is_valid_play((5, 'JS'), 1, [(None, []), (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]), (None, []), (None, [])], [(0, [(2, 'JS'), (5, 'JS')]), (1, [(1, 'XX'), (3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]))])], [0, 1, 0, 0], ['AD', '8S', '9S', '0S', 'JS'], 'JS')
True
```
<hr>

### Question 4. Returning score
Write a function called `phazed_score` that takes the following single argument:

`hand`
* The list of cards that the current player holds in their hand, each of which is in the form of a 2-element string. 

Your function should return the score for the hand (assuming the game has ended, and the player is left with the cards in hand) as a non-negative integer.

Example calls to the function are:
```
>>> phazed_score(['9D', '9S', '9D', '0D', '0S', '0D'])
57
>>> phazed_score(['2D', '9S', 'AD', '0D'])
46
>>> phazed_score([])
0
```
<hr>

### Question 5. Determining best play
Write a function called `phazed_play` that takes the following arguments:

`player_id`
* An integer between 0 and 3 inclusive, indicating the ID of the player attempting the play. 

`table`
* A 4-element list of phase plays for each of Players 0—3, respectively. Each phase play is in the form of a 2-tuple indicating the phase type (as an integer or None, consistent with the output of phazed_phase_type) and a list of lists of cards (of the same format as for phazed_phase_type, but possibly with extra cards played to each of the groups in the phase). An empty phase for a given player will take the form (None, []). As an example of a full 4-player table, [(None, []), (1, [['2S', '2S', '2C'], ['AS', '5S', '5S', '5D']]), (None, []), (None, [])] indicates that Players 0, 2 and 3 are yet to play a phase for the hand, and Player 1 has played Phase 1, in the form of a set of Twos and a set of Fives, the latter of which has had one extra card added to it. 

`turn_history`
* A list of all turns in the hand to date, in sequence of play. Each turn takes the form of a 2-tuple made up of the Player ID and the list if individual plays in the turn (based on the same format as for play above, with the one difference that for any draws from the deck, the card is indicated as 'XX' (as it is not visible to other players). For example, [(0, [(2, 'JS'), (5, 'JS')]), (1, [(2, 'JS'), (3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]))])] indicates that the hand to date is made up of two turns, on the part of Players 0 and 1, respectively. Player 0 first drew the Jack of Spades from the discard pile, then discarded the Jack of Spades (presumably they had a change of heart!). Player 1 then picked up the Jack of Spades from the discard pile, and played a phase, in the form of two sets of three cards of the same value (i.e. Phase 1). 

`phase_status`
* A 4-element indicating the phases that each of Players 0—3, respectively, have achieved in the . For example, [0, 4, 0, 0] indicates that Players 0, 2 and 3 have not got any phases, but Player 1 has achieved up to Phase 4. At the start of a game, this is initialised to [0, 0, 0, 0]. 

`hand`
* The list of cards that the current player holds in their hand, each of which is in the form of a 2-element string. 

`discard`
* The top card of the discard stack, in the form of a 2-element string (e.g. '3D'). 

Your function should return a 2-tuple describing the single play your player wishes to make, made up of a play ID and associated play content, as described below:

1. Pick up a card from the top of the deck at the start of the player's turn. In this case, the card at the top of the deck is unknown at the time the play is determined, so the play content is set to None (i.e. (1, None)). 
2. Pick up a card from the top of the discard pile at the start of the player's turn, with the play content taking the value of discard (e.g. (2, '2C')). 
3. Place a phase to the table from the player's hand, with the play type being the 2-tuple of the phase ID (see Q2) and phase (e.g. (3, (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]))). 
4. Place a single card from the player's hand to a phase on the table, with the play type being a 2-tuple made up of the card the player is attempting to play, and the position they are attempting to play it in, itself in the form of a 3-tuple indicating: (1) the player ID of the phase the card is to be placed on; (2) the group within the phase the card is to placed in; and (3) the index of the position within the group the card is to be played to. For example, (4, ('AD', (1, 0, 3))) indicates that an Ace of Diamonds is to be placed on the phase of Player 1, in Group 0 and index position 3 (i.e. it will be the fourth card in the first Group). 
5. Discard a single card from the player's hand, and in doing so, end the turn (e.g. (5, 'JS') indicates that a Jack of Spades is to be discarded). 

An example call to the function is:
```
>>> print(phazed_play(1, [(None, []), (5, [['2C', '3H', '4D', 'AD', '6S', '7C', '8S', '9H', '0S', 'JS']]), (None, []), (None, [])], [(0, [(2, 'JS'), (5, 'JS')]), (1, [(2, 'JS'), (3, (5, [['2C', '3H', '4D', 'AD', '6S', '7C', '8S', '9H']])), (4, ('0S', (1, 0, 8))), (4, ('JS', (1, 0, 9)))])], [0, 5, 0, 0], ['5D'], None))
(5, '5D')
```

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/arsamsamadi/
