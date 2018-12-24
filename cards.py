class Card:
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    ranks = ["this shouldn't happen", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=0, rank=0):
        self.suit = suit
        self.rank = rank
        if rank == 1:
            self.value = 11
        elif rank > 1 and rank < 10:
            self.value = rank
        else:
            self.value = 10

    def __str__(self):
        return self.ranks[self.rank] + " of " + self.suits[self.suit]

    def cmp(self, other):
        if self.suit > other.suit: return 1
        if self.suit < other.suit: return -1
        if self.rank == 1:
            if other.rank == 1:
                return 0
            return 1
        if other.rank == 1:
            if self.rank == 1:
                return 0
            return -1
        if self.rank > other.rank: return 1
        if self.rank < other.rank: return -1
        return 0

    def __eq__(self, other):
        return self.cmp(other) == 0

    def __le__(self, other):
        return self.cmp(other) <= 0

    def __ge__(self, other):
        return self.cmp(other) >= 0

    def __gt__(self, other):
        return self.cmp(other) > 0

    def __lt__(self, other):
        return self.cmp(other) < 0

    def __ne__(self, other):
        return self.cmp(other) != 0


class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))

    def __str__(self):
        s = ""
        for i in range(len(self.cards)):
            s = s + " " * i + str(self.cards[i]) + "\n"
        return s

    def multiply_deck(self, num):
        temp = self.cards[:]
        for i in range(num):
            self.cards.extend(temp)

    def shuffle(self):
        import random
        rng = random.Random()
        rng.shuffle(self.cards)

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False

    def pop(self):
        return self.cards.pop()

    def is_empty(self):
        return self.cards == []

    def deal(self, hands, num_cards=999):
        num_hands = len(hands)
        for i in range(num_cards):
            if self.is_empty():
                break
            card = self.pop()
            hand = hands[i % num_hands]
            hand.add(card)
            if num_cards == 1:
                if hand.total_value() == 21:
                    return 1
                if hand.total_value() > 21:
                    return -1
                return 0


class Hand(Deck):
    def __init__(self, name=""):
        self.cards = []
        self.name = name

    def add(self, card):
        self.cards.append(card)

    def __str__(self):
        s = "**" + self.name + "'s hand**"
        if self.is_empty():
            s += " is empty\n"
        else:
            s += " contains:\n```"
        return s + Deck.__str__(self) + "```"

    def total_value(self):
        total = 0
        for card in self.cards:
            total += card.value
        if total > 21:
            for card in self.cards:
                if card.rank == 1:
                    total -= 10
        return total


class BlackJack:
    def __init__(self):
        self.deck = Deck()
        self.deck.multiply_deck(6)
        self.deck.shuffle()
