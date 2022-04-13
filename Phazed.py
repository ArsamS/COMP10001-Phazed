from itertools import groupby, combinations, permutations
from collections import defaultdict as dd

''' Question 1. Finding Group Types '''
def calculate_run(group, special):
    '''
    Converts a group of cards into a format that can be easily
    compared by converting colours, values, and Wilds. Returns the converted
    group in a list
    '''
    # Assign colours to a list with the format [[value, colour], etc.]
    run = []
    for x in range(len(group)):
        if group[x][1] == 'H' or group[x][1] == 'D':
            # Red for Hearts and Diamonds
            colour = 'R' 
        elif group[x][1] == 'S' or group[x][1] == 'C':
            # Black for Spades and Clubs
            colour = 'B'
        run.append([group[x][0], colour])
    
    # Convert run to numbers that can be easily compared
    for v in range(len(run)):
        if run[v][0] in special:
            run[v][0] = special[run[v][0]]
        # Rule for aces
        elif run[v][0] == 'A':
            # If it's the first in a list
            if v == 0:
                run[v][0] = 1
                run[v].append('A')
            else:
                if len(run[v - 1]) == 3:
                    without_aces = [card for card in run[v:] if card[0] != 'A']
                    if without_aces:
                        # Follow behind the next card that's not an Ace
                        next_card = without_aces[0]
                        next_index = run.index(next_card)
                        difference = next_index - v
                        if next_card[0] in special:
                            run[v][0] = special[next_card[0]] - difference
                        else:
                            run[v][0] = int(next_card[0]) - difference
                    else:
                        # Otherwise just follow the previous card
                        run[v][0] = run[v - 1][0] + 1
                else:
                    run[v][0] = run[v - 1][0] + 1
                run[v].append('A')
        # Convert to ints
        else:
            run[v][0] = int(run[v][0])
    return run

def case_1_3(values_dict, length, wild):
    '''
    Called by the phazed_group_type function to test Case 1 (set of three
    cards of the same value) and Case 3 (set of four cards of the same value),
    returning 1 or 3 if one of the cases is true.
    '''
    result = False
    for value in values_dict:
        if value != 'A':
            # Case 1: Set of 3 cards of the same value
            if length == 3:
                same = len(list(values_dict[value]))
                if same == 3:
                    result = 1
                # Make sure there are 2 natural cards
                elif same == 2 and wild == 1:
                    result = 1
            # Case 3: Set of four cards of the same value
            if length == 4:
                same = len(list(values_dict[value]))
                if same == 4:
                    result = 3
                # Make sure there are 2 natural cards
                elif same + wild == 4 and wild <= 2:
                    result = 3
    return result

def case_4_5(run, special, wild, length):
    '''
    Called by the phazed_group_type function to test Case 4 (run of eight
    cards) and Case 5 (run of four cards of the same colour),
    returning 4 or 5 if one of the cases is true.
    '''
    result = False
    # Calculate successful run
    sequence_4 = 1
    sequence_5 = 1
    without_wild = [card for card in run if len(card) != 3]
    if without_wild:
        colour = without_wild[0][1]
    else:
        return False
    for v in range(len(run) - 1):
        colour_match = True
        # Check colour matching for non Aces
        if len(run) == 2:
            if run[v][1] != colour:
                colour_match = False
        # Check the last card in a list
        if v == len(run) - 2:
            if run[v + 1][1] != colour:
                colour_match = False
        # Add to run if the first card is a wild
        if run[v][0] == 1:
            sequence_4 += 1
            sequence_5 += 1
        # Add if the next number matches
        elif run[v][0] + 1 == run[v + 1][0]:
            sequence_4 += 1
            if colour_match:
                sequence_5 += 1
        # Allow wrapping around of numbers
        elif run[v][0] == 13 and run[v + 1][0] == 2:
            sequence_4 += 1
            if colour_match:
                sequence_5 += 1
    # Calculate whether Case 4 or 5 are fulfilled and makes sure
    # there are 2 natural numbers
    if length == 8 and sequence_4 == 8 and wild <= 6:
        result = 4
    if length == 4 and sequence_5 == 4 and wild <= 2:
        result = 5
    return result

def case_6_7(run, special, wild, length):
    '''
    Called by the phazed_group_type function to test Case 6 (34-accumulation
    of cards) and Case 7 (34-accumulation of cards of the same colour),
    returning a list of the cases that are true.
    '''
    result = []
    total = 0
    # Set a colour to compare to (ignoring Wild cards)
    if length - wild > 2:
        without_wild = [card for card in run if len(card) == 2]
        colour = without_wild[0][1]
        same_colour = True
        for v in range(len(run)):
            # Aces are in the format [Number, Colour, 'A']
            if len(run[v]) == 3:
                total += 1
            else:
                total += run[v][0]
            if run[v][1] != colour:
                # If one of the colours doesn't match, Case 7 fails
                same_colour = False
        if total == 34:
            result.append(6)
            if same_colour:
                result.append(7)
    return result

def phazed_group_type(group):
    '''
    Calculates whether a group of cards uphold Cases 1 - 7 using a variety
    of helper functions. Returns a sorted list of which cases are true.
    '''
    # Initialise variables
    length = len(group)
    results = []
    wild = 0
    values_dict = dd(list)
    suits_dict = dd(list)
    # Assign special cards to a dictionary to use later for values
    special = {'0': 10, 'J': 11, 'Q': 12, 'K': 13}  
    # Create separate dictionaries for sorting by values and suits
    group_values = groupby(group, lambda x: x[0])
    for category, contents in group_values:
        values_dict[category] += list(contents)
    group_suits = groupby(group, lambda x: x[1])
    for category, contents in group_suits: 
        members = list(contents)
        # Add non Wilds to a dictionary of suits
        for member in members:
            if member[0] != 'A':
                suits_dict[category] += [member]
    # Count number of wild cards
    for x in group:
        if x[0] == 'A':
            wild += 1
    
    # Case 1 and 3 testing
    one_three = case_1_3(values_dict, length, wild)
    if one_three:
        results.append(one_three)
              
    # Case 2: Set of seven cards of the same suit
    for suit in suits_dict:
        if len(group) == 7:
            same = len(list(suits_dict[suit]))
            if same == 7 and wild == 0:
                results.append(2)
            # Make sure there are 2 natural cards
            elif same + wild == 7 and wild <= 5:
                results.append(2)
                
    # Testing for Cases 4 - 7 requires a conversion of the group
    run = calculate_run(group, special)
    
    # Case 4 and 5 testing
    if length == 4 or length == 8:
        four_five = case_4_5(run, special, wild, length)
        if four_five:
            results.append(four_five)
    
    # Case 6 and 7 testing
    results.extend(case_6_7(run, special, wild, length))
    
    return sorted(results)
  
  
''' Question 2. Finding Phase Types '''

def phazed_phase_type(phase):
    '''
    Calculates whether a combination of card groups is a valid part of
    phases 1 - 7 by calling phazed_group_type from the first question.
    Returns a sorted list of which phases apply to the given combination.
    '''
    length = len(phase)    
    results = []
    groups = []
    # Use a dictionary for any time a Case is successful from Question 1
    groups_dict = dd(int)
    for group in phase:
        # Imported from Q1 (in a file called group.py)
        groups.extend(phazed_group_type(group))
    for result in groups:
        groups_dict[result] += 1
    
    # Case 1: Two sets of three cards of the same value
    if groups_dict[1] == 2 and length == 2:
        results.append(1)
    # Case 2: One set of 7 cards of the same suit
    if groups_dict[2] == 1 and length == 1:
        results.append(2)
    # Case 3: Two 34-accumulations
    if groups_dict[6] == 2 and length == 2:
        results.append(3)
    # Case 4: Two sets of four cards of the same value
    if groups_dict[3] == 2 and length == 2:
        results.append(4)
    # Case 5: One run of eight cards
    if groups_dict[4] == 1 and length == 1:
        results.append(5)
    # Case 6: Two 34-accumulations of the same colour
    if groups_dict[7] == 2 and length == 2:
        results.append(6)
    # Case 7: A run of four cards of the same colour and a
    # set of four cards of the same value
    if groups_dict[3] == 1 and groups_dict[5] == 1 and length == 2:
        if phazed_group_type(phase[0]) == [5]:
            results.append(7)
    
    return sorted(results)
  
  
''' Question 3. Determining if a play is valid '''
def already_played(plays, history):
    '''
    Determines if a player has already completed certain play types in a
    given turn by returning either True or False
    '''
    for p in plays:
        for action in history:
            if p in action:
                return True
    return False

def missing_card(cards, hand):
    '''
    Determines if a list of cards is present in a player's current hand
    by returning either True or False
    '''
    for card in cards:
        if card not in hand:
            return True
    return False

def calculate_total(run):
    '''
    Calculuates accumulations for a given list of cards by returning
    the total value of the list and the colour of the list. If the group
    of cards aren't matching in colour, it will be given as False.
    '''
    total = 0
    # Picks a colour based on a non-Wild card
    without_wild = [card for card in run if len(card) != 3]
    colour = without_wild[0][1]
    same_colour = True
    for v in range(len(run)):
        total += run[v][0]
        if run[v][1] != 'A':
            if run[v][1] != colour:
                # If non-Wilds don't match in colour, the group no longer
                # matches
                same_colour = False
    # Return False if there is no colour match
    if not same_colour:
        colour = False
    return(total, colour)

def test_run(played_card, index, match_group, group_size, group_type):
    '''
    Tests whether an addition of a card (at either end) to a phase
    matches the desired group type by returning either True or False
    '''
    if played_card[0] != 'A':
        new_run = []
        if index == 0:
            new_run.append(played_card)
            new_run.extend(match_group[:group_size - 1])
        elif index == group_size:
            new_run.extend(match_group[1:])
            new_run.append(played_card)
        run_phase = phazed_group_type(new_run)
        if group_type not in run_phase:
            return False
    return True

def phazed_is_valid_play(play, player_id, table, turn_history, phase_status, 
                         hand, discard):
    '''
    Determines whether a play by a player in a given turn is valid based
    on a variety of factors. Returns either True or False based on the 
    move's validity.
    '''
    # Initialise variables
    result = True
    history_dict = dd(list)
    for player in turn_history:
        history_dict[player[0]] = player[1]
    
    # Condition 1: Picking up from the deck or the discard pile
    if play[0] == 1 or play[0] == 2:
        # Case 1.1: Pick up a card not as the first
        if already_played([1, 2], history_dict[player_id]):
            return False
        # Case 1.2: Card picked up not in discord
        if play[0] == 2 and play[1] != discard:
            return False
    
    # Condition 2: Matching phase play
    if play[0] == 3:
        # Case 2.1: Phase doesn't match declared phase type
        aim = play[1][0]
        actual = phazed_phase_type(play[1][1])
        if aim not in actual:
            return False
        # Case 2.2: Not the required phase type
        if aim != phase_status[player_id] + 1:
            return False
        # Case 2.3: Plays occurs before picking up a card
        if not already_played([1, 2], history_dict[player_id]):
            return False
        # Case 2.4: Player has already played a phase
        if already_played([3], history_dict[player_id]):
            return False
        # Case 2.5: Does not hold all the required cards
        played_cards = []
        for group in play[1][1]:
            played_cards.extend(group)
        if missing_card(played_cards, hand):
            return False

    # Condition 3: Play to the table
    if play[0] == 4:
        # Create some variables to make referencing easier
        played_card = play[1][0]
        group = play[1][1][1]
        match_phase = phase_status[play[1][1][0]]
        target_player = play[1][1][0]
        # Case 3.1: Group ID not matching
        if group in range(len(table[target_player][1])):
            match_group = table[target_player][1][group]
        else:
            return False
        group_size = len(match_group)
        without_wild = [card for card in match_group if card[0] != 'A']
        special = {'0': 10, 'J': 11, 'Q': 12, 'K': 13} 

        # Case 3.2: Play occurs before picking up a card
        if not already_played([1, 2], history_dict[player_id]):
            return False
        # Case 3.3: Happens before a player has played their phase
        if not already_played([3], history_dict[player_id]):
            return False
        # Case 3.4: Player does not have the played card
        if missing_card([played_card], hand):
            return False
        # Case 3.5: Invalid index
        index = play[1][1][2]
        if index > group_size:
            return False
        # Case 3.6: Play doesn't match phase
        if match_phase == 1 or match_phase == 4:
            # Phase 1 or Phase 4, test whether values match
            value = without_wild[0][0]
            if played_card[0] != value and played_card[0] != 'A':
                return False
        if match_phase == 2:
            # Phase 2, test whether suits match
            suit = without_wild[0][1]
            if played_card[1] != suit and played_card[0] != 'A':
                return False
        if match_phase == 3 or match_phase == 6:
            # Phase 3 or 6, test whether the play is a valid move
            # based on the fibonacci numbers and if colours match
            fibonacci = [34, 55, 68, 76, 81, 84, 86, 87]
            # Calculate totals for what is already on the table
            special = {'0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 1} 
            old_run = calculate_run(match_group, special)
            old_total = calculate_total(old_run)
            # Convert the played card into the format used in previous
            # questions
            converted = calculate_run([played_card], special)[0]
            for num in range(len(fibonacci) - 1):
                # If a number falls between two fibonacci numbers,
                # the maximum that the played card can be is the
                # higher number
                if (old_total[0] >= fibonacci[num] and
                    old_total[0] < fibonacci[num + 1]):
                    maximum = fibonacci[num + 1] - old_total[0]
            # Test whether the played card exceeds the maximum
            if converted[0] > maximum:
                return False
            # Makes sure if the card is the last in the hand,
            # the accumulation is completed
            if len(hand) == 1:
                test_total = converted[0] + old_total[0]
                if test_total not in fibonacci:
                    return False
            if len(hand) == 2:
                hand_converted = calculate_run(hand, special)
                test_total = 0 
                for card in hand_converted:
                    test_total += card[0]
                test_total += old_total[0]
                if test_total not in fibonacci:
                    return False
            # Tests whether the played card's colour matches the colour
            # of the existing accumulation (if on Phase 6)
            if match_phase == 6:
                if converted[1] != 'A':
                    if old_total[1] != converted[1]:
                        return False
        if match_phase == 5:
            # Phase 5, test whether addition continues the run
            if group_size == 12:
                return False
            if index != group_size and index != 0:
                return False
            else:
                if not test_run(played_card, index, match_group,
                                group_size, 4):
                    return False
        if match_phase == 7:
            # Phase 7, tests depending on the group type
            if group == 0:
                # If testing the first group, make sure the added card
                # continues the run
                if not test_run(played_card, index, match_group,
                                group_size, 5):
                    return False
            else:
                # Make sure added card is of the same value if the
                # second group is being tested
                if not test_run(played_card, index, match_group,
                                group_size, 3):
                    return False
    
    # Condition 4: Discard a card and end the turn
    if play[0] == 5:
        played_card = play[1]
        # Case 4.1: Discard occurs before picking up a card
        if not already_played([1, 2], history_dict[player_id]):
            return False
        # Case 4.2: Discard has already occured
        if already_played([5], history_dict[player_id]):
            return False 
        # Case 4.3: Player does not have the played card
        if missing_card([played_card], hand):
            return False
        # Case 4.4 Accumulations of the player are not complete
        if already_played([3, 4], history_dict[player_id]):
            if table[player_id][0] == 3 or table[player_id][0] == 6:
                test_phase = phazed_phase_type(table[player_id][1])
                if 3 not in test_phase and 4 not in test_phase:
                    return False  
    return result
  
  
''' Question 4. Returning score '''
def phazed_score(hand):
    '''
    Returns the score of a a player's hand to determine a player's score
    at the end of a hand
    '''
    re_assign = {'J': 11, 'Q': 12, 'K': 13, 'A': 25, '0': 10}
    total = 0
    for score in hand:
        value = score[0]
        if value in re_assign:
            value = re_assign[value]
        else:
            value = int(value)
        total += value
    return total
 
''' Question 5. Determining best play '''
def this_turn_played(play_type, history):
    '''
    Determines if a player has already completed certain play types in a
    given turn by returning either True or False
    '''
    play_dict = dd(list)
    play_no = 0
    for play in history:
        play_dict[play_no] += [play]
        if play[0] == 5:
            play_no += 1
            play_dict[play_no] = []
    
    current = len(play_dict) - 1
    current_run = play_dict[current]  
    for p in play_type:
        for action in current_run:
            if p in action:
                return True
    return False

def valid_cards(cards, hand_dict, two_groups):
    '''
    Determines if cards in either one or two groups can be played based
    on a dictionary of the player's hand
    '''
    plays = []
    for play in cards:
        # Add all of the cards in the combination (if there are two groups)
        if two_groups:
            added = play[0] + play[1]
        else:
            # Keep it the same for phases with one group
            added = play
        play_dict = dd(int)
        for card in added:
            play_dict[card] += 1
        success = True
        # Compare a dictionary of the cards in the play
        # to a dictionary of the hand to remove duplicates
        for card in play_dict:
            if card in hand_dict:
                if play_dict[card] > hand_dict[card]:
                    success = False
            else:
                success = False
        if success:
            plays.append(play)
    return plays

def find_combinations(hand, no_of_cards, group, two_groups):
    '''
    Returns a list of combinations based on a player's hand,
    how many cards should be in each group in the combination (1 or 2),
    and tested on a provided group type
    '''
    possible_plays = []
    combs = [list(x) for x in list(combinations(hand, no_of_cards))]
    # Testing using the Q1 function
    for combination in combs:
        if group in phazed_group_type(combination):
            possible_plays.append(combination)
    # Returns two groups if the phase type requires it
    if two_groups:
        return [list(x) for x in list(combinations(possible_plays, 2))]
    else:
        return possible_plays

def minimum_combinations(sorted_list):
    '''
    Returns the minimum number of combinations that can take place for
    an accumulation to save processing time based on a sorted and converted
    list of the player's hand
    '''
    if calculate_total(sorted_list)[0] >= 34:
        count = -1
        total = 0
        # Count how many of the highest value cards are needed to achieve
        # a 34-accumulation
        for card in sorted_list:
            total += sorted_list[count][0]
            if total >= 34:
                break
            else:
                count -= 1
        return abs(count)
    else:
        return False
    
def maximum_combinations(sorted_list):
    '''
    Returns the maximum number of combinations that can take place for
    an accumulation to save processing time based on a sorted and converted
    list of the player's hand
    '''
    if calculate_total(sorted_list)[0] >= 34:
        count = 0
        total = 0
        for card in sorted_list:
            total += sorted_list[count][0]
            # Count how many of the lowest value cards are needed to achieve
            # a 34-accumulation
            if total >= 34:
                break
            else:
                count += 1
        return count
    else:
        return False

def best_play(valid_plays, two_groups):
    '''
    Returns whichever play in a list of plays is the most beneficial
    to the player by making sure the play leaves the player with a score
    as low as possible
    '''
    if len(valid_plays) == 1:
        return valid_plays[0]
    else:
        if two_groups:
            # Add two groups together for certain phases
            testing_group = []
            for play in valid_plays:
                added = play[0] + play[1]
                testing_group.append(added)
        else:
            testing_group = valid_plays
        score_dict = dd(int)
        index = 0
        for play in testing_group:
            # Create a dictionary of scores based on the score of each play
            score_dict[index] = phazed_score(play)
            index += 1
        if score_dict.values():
            # Return the play with the max score
            highest_score = max(score_dict.values())
            swapped = []
            for key, value in score_dict.items():
                swapped.append((value, key))
            for x in swapped:
                if x[0] == highest_score:
                    index = x[1]
                    return valid_plays[index]
        
def convert_for_run(group, special):
    '''
    Uses a simplified version of the Q1 finding run function to convert
    a group of cards into a format that can be easily compared
    in order to be able to identify a run
    '''
    run = []
    for x in range(len(group)):
        run.append([group[x][0], group[x][1]])
    # Convert run to numbers that can be easily compared
    for v in range(len(run)):
        if run[v][0] in special:
            run[v][0] = special[run[v][0]]
        # Make aces follow from the last number
        elif run[v][0] == 'A':
            run[v][0] = 1
            run[v].append('A')
        # Convert to ints
        else:
            run[v][0] = int(run[v][0])
    return run

def find_run(hand, special):
    '''
    Returns a sorted list of a group of cards to be able to more easily
    identify runs
    '''
    wilds = []
    hand_without_dupes = list(set(hand))
    converted = convert_for_run(hand_without_dupes, special)
    # Remove duplicates (both of the same card and for the same value)
    for card in converted:
        if card[0] == 1:
            wilds.append(card)
            converted.remove(card)

    for card in converted:
        val = card[0]
        index = converted.index(card)
        for x in converted:
            if x[0] == val and x[0] != 1:
                index2 = converted.index(x)
                if index2 != index:
                    converted.remove(x)
    # Sort the list based on its value
    convert = sorted(converted, key=lambda x: x[0])
    special_reverse = {10: '0', 11: 'J', 12: 'Q', 13: 'K', 1: 'A'}
    # Reverse the conversion
    reverse = []
    for card in convert:
        suit = card[1]
        if card[0] in special_reverse:
            val = special_reverse[card[0]]
        else:
            val = str(card[0])
        new_card = val + suit
        reverse.append(new_card)

    wilds_reverse = []
    for card in wilds:
        suit = card[1]
        if card[0] in special_reverse:
            val = special_reverse[card[0]]
        else:
            val = str(card[0])
        new_card = val + suit
        wilds_reverse.append(new_card)
    
    result = []
    result.extend(reverse)
    result.extend(wilds_reverse)    
    return result

def able_to_play_phase(phase, hand, hand_dict):
    '''
    If the player is able to play a phase, this function uses a variety
    of helper functions to return the best play based on the player's hand
    and phase
    '''
    special = {'0': 10, 'J': 11, 'Q': 12, 'K': 13}  
    if phase == 1:
        # Phase 1: Two sets of three cards of the same value
        group = 1
        two_groups = True
        combs = find_combinations(hand, 3, group, two_groups)
        # Test which combination is a valid play
        valid_plays = valid_cards(combs, hand_dict, two_groups)
        return best_play(valid_plays, two_groups)
    if phase == 2:
        # Phase 2: One set of 7 cards of the same suit
        group = 2
        two_groups = False
        combs = find_combinations(hand, 7, group, False)
        valid_plays = valid_cards(combs, hand_dict, False)
        return [best_play(valid_plays, two_groups)]
    if phase == 3:
        # Phase 3: Two 34-accumulations
        group = 6
        two_groups = True
        possible_combinations = []
        possible_plays = []
        converted = calculate_run(hand, special)
        convert = sorted(converted, key=lambda x: x[0])
        # Finds the min and max to minimise processing time
        # and finds a list of combinations that give a 34 accumulation
        minimum = minimum_combinations(convert)
        maximum = maximum_combinations(convert)
        for x in range(minimum, maximum + 1):
            combs = [list(x) for x in list(combinations(hand, x))]
            possible_combinations.extend(combs)
        # Finds combinations of two groups of 34 accumulation
        for combination in possible_combinations:
            if group in phazed_group_type(combination):
                possible_plays.append(combination)
        tests = [list(x) for x in list(combinations(possible_plays, 2))]
        # Find which of these can actually be played based on the hand
        valid_plays = valid_cards(tests, hand_dict, True)
        return best_play(valid_plays, two_groups)
    if phase == 4:
        # Phase 4: Two sets of four cards of the same value
        group = 3
        two_groups = True
        combs = find_combinations(hand, 4, group, True)
        valid_plays = valid_cards(combs, hand_dict, True)
        return best_play(valid_plays, two_groups)
    if phase == 5:
        # Phase 5: One run of eight cards
        group = 4
        two_groups = False
        run_find = find_run(hand, special)
        combs = find_combinations(run_find, 8, group, False)
        valid_plays = valid_cards(combs, hand_dict, False)
        return [best_play(valid_plays, two_groups)]
    if phase == 6:
        # Phase 6: Two 34-accumulations of the same colour
        group = 7
        two_groups = True
        possible_combinations = []
        possible_plays = []
        # The same process as phase 3, now testing on group 7
        # to check that accumulations are of the same colour
        converted = calculate_run(hand, special)
        convert = sorted(converted, key=lambda x: x[0])
        minimum = minimum_combinations(convert)
        maximum = maximum_combinations(convert)
        for x in range(minimum, maximum + 1):
            combs = [list(x) for x in list(combinations(hand, x))]
            possible_combinations.extend(combs)
        for combination in possible_combinations:
            if group in phazed_group_type(combination):
                possible_plays.append(combination)
        tests = [list(x) for x in list(combinations(possible_plays, 2))]
        valid_plays = valid_cards(tests, hand_dict, True)
        return best_play(valid_plays, two_groups)
    if phase == 7:
        # Phase 7: A run of four cards of the same colour and
        # a set of four cards of the same value
        # Find valid runs of four cards
        run_find = find_run(hand, special)
        combs_1 = find_combinations(run_find, 4, 5, False)
        valid_1 = valid_cards(combs_1, hand_dict, False)
        # Find valid set of four cards of the same value
        combs_2 = find_combinations(hand, 4, 3, False)
        valid_2 = valid_cards(combs_2, hand_dict, False)
        
        possible_plays = []
        
        for x in valid_1:
            for y in valid_2:
                added = [x, y]
                # Test the combination of the two groups together
                # to find valid plays
                valid = valid_cards([added], hand_dict, True)
                if valid:
                    possible_plays.append(added)
        
        return best_play(possible_plays, True)

def able_to_place(hand, player, phase_info):
    '''
    Returns which play would be best on a single player's phase on the table
    '''
    phase = phase_info[0]
    played = phase_info[1]
    possible_plays = []
    for card in hand:
        group_id = 0
        for group in played:
            for index in range(len(group) + 1):
                # Create dummy variables to test valid placements
                # based on a group and index
                play = (4, (card, (1, group_id, index)))
                player_id = 0
                table = [(None, []), (phase, played), (None, []), (None, [])]
                turn_history = [(0, [(2, 'JS'), (3, 'JS')]),
                                (1, [(2, 'JS'), (3, 'JS'), (5, 'JS')])]
                phase_status = [1, phase, 0, 0]
                hand = [card]
                discard = '3D'
                test = phazed_is_valid_play(play, player_id, table,
                        turn_history, phase_status, hand, discard)
                if test:
                    possible_plays.append([card, group_id, index])
            # If there are two groups, test the other as well
            group_id += 1
    possible_cards = [[play[0]] for play in possible_plays]
    if possible_cards:
        best_card = best_play(possible_cards, False)[0]
        # If there is a possible play, determine which is the best
        for play in possible_plays:
            if best_card in play:
                return (4, (play[0], (player, play[1], play[2])))

def placing(phase_status, turn_history, table, hand):
    '''
    If the player can play a card on the table, this function returns
    which card is the best to play based on a player's hand and the
    phase progress of others on the table
    '''
    possible_plays = []
    non_zero = [p for p in range(len(phase_status))
                if phase_status[p] > 0]
    phase_in_this_hand = [p[0] for p in turn_history
                          if p[0] in non_zero]
    table_phases = dd(list)
    # Finds which players have played a phase this hand
    for player in phase_in_this_hand:
        p = table[player]
        phase = p[0]
        played = p[1]
        table_phases[player] = [phase, played]
    for player in table_phases:
        # Test what plays can be completed on the table
        success = able_to_place(hand, player, table_phases[player])
        if success:
            possible_plays.append(success)
    if possible_plays:
        possible_cards = []
        for x in range(len(possible_plays)):
            # Finds the best play based on the highest scoring card
            # that can be played
            possible_cards.append([possible_plays[x][1][0]])
            best_card = best_play(possible_cards, False)[0]
            if best_card:
                for play in possible_plays:
                    if best_card in play[1]:
                        return play
    else:
        return False
            
def phazed_play(player_id, table, turn_history, phase_status, hand, discard): 
    '''
    Returns what a player can do based on their status and others on the table.
    Returns the best possible play
    '''
    # Create a dictionary of the players' history
    history_dict = dd(list)
    for player in turn_history:
        history_dict[player[0]] += player[1]

    # Create a dictionary of the player's hand to find
    # if the player holds 0, 1, or 2 of the same card
    hand_dict = dd(int)
    for card in hand:
        hand_dict[card] += 1
        
    discarding = False
       
    if this_turn_played([1, 2], history_dict[player_id]):
        if not already_played([3], history_dict[player_id]):
            # Test if player able to play a phase if they have already
            # picked up a card
            phase = phase_status[player_id] + 1
            result = able_to_play_phase(phase, hand, hand_dict)
            print(result)
            # Discard if a phase can't be played
            if result is None:
                discarding = True
            elif isinstance(result, list) and None in result:
                discarding = True
            else:
                return (3, (phase, result))
        else:
            # If a phase has been played, try playing a card on the table
            # If a play can't be made, discard
            able_to_place = placing(phase_status, turn_history, table, hand)
            if able_to_place:
                return able_to_place
            else:
                discarding = True

        if discarding: 
            # Discard the highest scoring non Wild card if possible
            # as Wilds can be very versatile
            hand_list = [[card] for card in hand]
            if hand_list:
                without_aces = [card for card in hand_list
                                if card[0][0] != 'A']
                if without_aces:
                    best_discard = best_play(without_aces, False)[0]
                else:
                    best_discard = best_play(hand_list, False)[0]
                return (5, best_discard)
    else:
        # Test whether you should pick up a card from the top of the deck
        # or the discard
        preview_hand = hand + [discard]
        preview_hand_dict = dd(int)
        for card in preview_hand:
            preview_hand_dict[card] += 1
        if not already_played([3], history_dict[player_id]):
            phase = phase_status[player_id] + 1
            able_to_play = able_to_play_phase(phase, hand, hand_dict)

            discard_able = able_to_play_phase(phase, preview_hand,
                                              preview_hand_dict)
            if able_to_play:
                # If you are already able to place a phase, there is no
                # need to pickup a card from a discard which could be high
                # in value
                return (1, None)
            elif discard_able:
                # If you can make a phase play with the discard card in 
                # the hand, pick it up
                return (2, discard)
            else:
                return (1, None)
        else:
            # If you have already played a phase, attempt the same thing 
            # with placing a card on the table
            able_to_place = placing(phase_status, turn_history,
                                    table, hand)
            discard_able = placing(phase_status, turn_history,
                                   table, preview_hand)
            if able_to_place:
                return (1, None)
            elif discard_able:
                return (2, discard)
            else:
                return (1, None)

