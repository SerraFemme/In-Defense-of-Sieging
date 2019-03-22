"""

"""
import random


class CardMaker(object):
    """
    Creates a card object from a given information block originating
    from CardLibrary.json.
    """

    def __init__(self, card):
        self.card_info = card  # TODO: remove, redundant?
        self.ID = self.card_info['ID']
        self.Faction_Type = self.card_info['Faction_Type']
        self.Card_Type = self.card_info['Card_Type']
        self.Name = self.card_info['Name']
        self.Text = self.card_info['Text']
        self.Target = self.card_info['Target']
        self.Effects_List = self.card_info['Effects']
        if 'Trigger_Text' in self.card_info:
            self.Trigger_Text = self.card_info['Trigger_Text']
        if 'Requirement' in self.card_info:
            self.Requirement = self.card_info['Requirement']
        if 'Stamina_Cost' in self.card_info:
            self.Stamina_Cost = self.card_info['Stamina_Cost']
        if 'Scar_Cost' in self.card_info:
            self.Scar_Cost = self.card_info['Scar_Cost']
        if 'Range' in self.card_info:
            self.Range = self.card_info['Range']
        self.Effects = []
        for i in self.Effects_List:
            pass


class PlayerDeck(object):
    """
    Class which keeps track of ALL cards owned by a player.
    Deck List is the list of cards owned by the player and SHOULD not change during the Battle phase.
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
        self.deck_list = deck  # List containing all cards owned by the player
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

    def current_hand_size(self):
        return len(self.hand)

    def max_health(self):
        value = len(self.deck_list) - len(self.scar_pile)  # TODO: may subtract hand size as well
        return value

    def heal(self, value):
        """
        Heal: takes the top X cards of their wound pile and puts them on the bottom of their health deck.
        """
        for i in range(value):
            if len(self.wound_pile) > 0:
                card = self.get_top_card(self.wound_pile)
                self.put_card_on_bottom(self.health_deck, card)

    def mill(self, value):
        """
        Mill: Take the top X cards of your health deck and put them on top of your wound pile
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

    def discard(self, value):  # Discards a single card at index value in hand
        self.wound_pile.append(self.hand.pop(value))

    def put_card_into_hand(self, card):
        self.hand.append(card)

    def mulligan(self):
        # TODO: discard selected cards
        draw_number = self.hand_size - len(self.hand)
        if draw_number > 0:
            self.draw(draw_number)
