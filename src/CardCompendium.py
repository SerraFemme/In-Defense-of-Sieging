"""

"""
import random


class CardMaker(object):
    """
    Creates a card object from a given information block originating
    from CardLibrary.json.
    """

    def __init__(self, card):
        self.card_info = card
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

    def print_info(self):
        print('Card Name:', self.Name)
        print('Card Typing:', self.Faction_Type, self.Card_Type)
        print('Text:', self.Text)
        # print('Requirement:', self.Requirement)
        # print('Stamina Cost:', self.Stamina_Cost)
        # print('Scar Cost:', self.Scar_Cost)
        # print Range


class PlayerDeck(object):
    """
    Class which keeps track of ALL cards owned by a player.
    Deck List is the list of cards owned by the player and SHOULD not change during the Battle phase.
    Health Deck is the deck of cards that acts like health.
    Wounds pile is the discard pile.
    Scar Deck is the special discard pile where cards can be placed but never
    removed for the duration of the battle.
    Hand is what cards the player has access to.
    Permanents are the Buffs and Debuffs owned by the Player that are active

    Deck Indexing: Bottom is 0
    """

    def __init__(self, deck):
        self.deck_list = deck  # Contains all cards owned by the player
        self.health_deck = deck  # Functions as Health Pool
        self.shuffle(self.health_deck)
        self.wound_pile = []  # Discard Pile
        self.scar_pile = []  # Inaccessible Discard Pile
        self.hand = []
        self.permanents = []

    def total_owned(self):
        return len(self.deck_list)

    def current_health(self):
        return len(self.health_deck)

    def current_wounds(self):
        return len(self.wound_pile)

    def current_hand(self):
        return len(self.hand)

    def max_health(self):
        value = len(self.deck_list) - len(self.scar_pile)
        return value

    def heal(self, value):
        for i in range(value):
            if len(self.wound_pile) >= 0:
                card = self.get_top_card(self.wound_pile)
                self.put_card_on_bottom(self.health_deck, card)

    def mill(self, value):
        for i in range(value):
            if len(self.health_deck) >= 0:
                card = self.get_top_card(self.health_deck)
                self.put_card_on_top(self.wound_pile, card)

    def shuffle(self, deck):
        random.shuffle(deck)

    # Generic Functions
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
    def draw(self, value):
        for i in range(value):
            if len(self.health_deck) >= 0:
                card = self.health_deck.pop()
                self.hand.append(card)

    def discard(self, value):
        for i in range(value):
            print('Select card to discard:')
            for j in self.hand:
                print(j.Name)
            while True:
                try:
                    v = int(input('Enter digit of card to discard: '))
                except ValueError:
                    print('Invalid input, try again')
                else:
                    self.wound_pile.append(self.hand.pop(v))

    def put_card_into_hand(self, card):
        self.hand.append(card)

    def mulligan(self):
        if len(self.hand) == 0:
            print('0 cards in hand, skipping Mulligan Phase')
        else:
            print('Mulligan Phase:')
            while len(self.hand) > 0:
                try:
                    print('0: Pass Mulligan Phase')
                    for j in self.hand:
                        print(j.Name)
                    v = int(input('Enter digit for selection: '))
                except ValueError:
                        print('Invalid input, try again')
                else:
                    if v == 0:
                        break
                    else:
                        self.wound_pile.append(self.hand.pop(v-1))
