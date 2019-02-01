"""

"""


class CardMaker(object):
    """
    Creates a card object from a given information block originating
    from CardLibrary.json.
    """

    def __init__(self, card):
        self.card_info = card
        self. ID = self.card_info['ID']
        self.Faction_Type = self.card_info['Faction_Type']
        self.Card_Type = self.card_info['Card_Type']
        self.Name = self.card_info['Name']
        self.Text = self.card_info['Text']
        self.Target = self.card_info['Target']
        self.Effects = self.card_info['Effects']
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

    def print_info(self):
        print('Card Name:', self.Name)
        print('Card Typing:', self.Faction_Type, self.Card_Type)
        print('Text:', self.Text)
        # print('Requirement:', self.Requirement)
        # print('Stamina Cost:', self.Stamina_Cost)
        # print('Scar Cost:', self.Scar_Cost)
        # print Range
