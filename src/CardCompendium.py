"""

"""
import random
from copy import deepcopy


class CardMaker(object):
    """
    Creates a card object from a given information block originating
    from CardLibrary.json.
    """

    def __init__(self, card):
        self.ID = card['ID']
        self.Faction_Type = card['Faction_Type']
        self.Card_Type = card['Card_Type']
        self.Name = card['Name']
        self.Text = card['Text']
        self.Target = card['Target']
        self.Effects_List = card['Effects']
        self.features = {}  # Dictionary of static features
        if 'Trigger_Text' in card:
            self.features['Trigger_Text'] = card['Trigger_Text']
        if 'Requirement' in card:
            self.features['Requirement'] = card['Requirement']
        if 'Stamina_Cost' in card:
            self.features['Stamina_Cost'] = card['Stamina_Cost']
        if 'Scar_Cost' in card:
            self.features['Scar_Cost'] = card['Scar_Cost']
        if 'Range' in card:
            self.features['Range'] = card['Range']
        self.Effects = []
        # for i in self.Effects_List:
        #     pass

    def get_range(self, value):
        """
        Calculates the range based on the bonus range given as 'value'.
        Returns a dictionary of the calculated ranges and restrictions
        If Bonus Range is negative, the maximum range is decreased.
        If maximum range is lower than the minimum range, then the minimum range
        is set equal to the maximum range.
        If either the minimum or maximum range is reduced to below 1, it is
        reduced to 1 instead.
        """
        if 'Range' in self.features:
            default_range = self.features['Range']
            calculated_ranges = {}
            if value < 0:  # Negative Bonus Range
                calculated_ranges['Max'] = default_range['Max'] + value
                if calculated_ranges['Max'] < 1:
                    calculated_ranges['Max'] = 1
                if default_range['Min'] > calculated_ranges['Max']:
                    calculated_ranges['Min'] = calculated_ranges['Max']
                else:
                    calculated_ranges['Min'] = default_range['Min']
                if 'Restriction' in default_range:
                    calculated_ranges['Restriction'] = default_range['Restriction']
                else:
                    calculated_ranges['Restriction'] = None

            else:  # Non-Negative Bonus Range
                calculated_ranges['Min'] = default_range['Min']
                calculated_ranges['Max'] = default_range['Max'] + value
                if 'Restriction' in default_range:
                    calculated_ranges['Restriction'] = default_range['Restriction']
                else:
                    calculated_ranges['Restriction'] = None

            return calculated_ranges
        else:
            return None

    def get_stamina_cost(self, value=0):
        if 'Stamina_Cost' in self.features:
            calculated_cost = self.features['Stamina_Cost'] + value
            if calculated_cost > 0:
                return calculated_cost
            else:
                return 0
        else:
            return None

    def get_scar_cost(self, value=0):
        if 'Scar_Cost' in self.features:
            calculated_cost = self.features['Scar_Cost'] + value
            if calculated_cost > 0:
                return calculated_cost
            else:
                return 0
        else:
            return None


class PlayerDeck(object):
    """
    Class which keeps track of ALL cards owned by a player.
    Deck List is the list of cards owned by the player and SHOULD not change
    during the Battle phase.
    Health Deck is the deck of cards that acts like health. When your deck
    becomes empty, you immediately become unconscious.
    Wounds pile is the discard pile.
    Scar Deck is the special discard pile where cards can be placed but never
    removed for the duration of the battle.
    Hand is what cards the player has access to.
    Permanents are the Buffs and Debuffs owned by the Player that are active

    Deck Indexing: Bottom is 0
    """

    # TODO: solution to know when health deck becomes empty

    def __init__(self, deck):
        self.deck_list = deepcopy(deck)  # List containing all cards owned by the player
        self.health_deck = deck  # Functions as Health Pool
        self.shuffle(self.health_deck)
        self.wound_pile = []  # Discard Pile
        self.scar_pile = []  # Special Discard Pile, cards can be added but not removed
        self.hand_size = None
        self.hand = []
        self.permanents = []

    def total_owned(self):
        return len(self.deck_list)

    def current_health(self):
        return len(self.health_deck)

    def current_wounds(self):
        return len(self.wound_pile)

    def current_scars(self):
        return len(self.scar_pile)

    def current_permanents(self):
        return len(self.permanents)

    def current_hand_size(self):
        return len(self.hand)

    def max_health(self):
        value = len(self.deck_list) - len(self.scar_pile)  # TODO: may subtract hand size as well
        return value

    def heal(self, value):
        """
        Heal: takes the 'value' of cards from the top of the player's wound pile
        and puts them on the bottom of their health deck.
        """
        for i in range(value):
            if len(self.wound_pile) > 0:
                card = self.get_top_card(self.wound_pile)
                self.put_card_on_bottom(self.health_deck, card)

    def mill(self, value):
        """
        Mill: Take the 'value' of cards from the top of the player's health deck
        and put them on top of their wound pile.
        """
        for i in range(value):
            if len(self.health_deck) > 0:
                card = self.get_top_card(self.health_deck)
                self.put_card_on_top(self.wound_pile, card)

    def shuffle(self, deck):
        random.shuffle(deck)

    # Generic Functions to be used by any deck
    def get_top_card(self, deck):
        return deck.pop()

    def get_bottom_card(self, deck):
        return deck.pop(0)

    def put_card_on_top(self, deck, card):
        deck.append(card)

    def put_card_on_bottom(self, deck, card):
        deck.insert(0, card)

    def peek(self, deck, value):
        return deck[value]

    # Hand
    def draw(self, value=1):
        for i in range(value):
            if self.current_health() > 0:
                card = self.get_top_card(self.health_deck)
                self.hand.append(card)

    def draw_hand(self):
        draw_number = self.hand_size - len(self.hand)
        if draw_number > 0:
            self.draw(draw_number)

    def discard(self, value):  # Discards a single card at index value in hand
        self.wound_pile.append(self.hand.pop(value))

    def put_card_into_hand(self, card):
        self.hand.append(card)

    def end_mulligan(self):
        self.draw_hand()

    def mulligan_card(self, value):
        card = self.hand.pop(value)
        self.put_card_on_bottom(self.health_deck, card)
