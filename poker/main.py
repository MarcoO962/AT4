from player import Player

def create_deck():
    deck = Player("deck", 0)
    x = 1
    for i in ["Spades", "Diamonds", "Clubs", "Hearts"]:
        suit = i
        for i in ["Ace","King","Queen","Jack","10","9","8","7","6","5","4","3","2"]:
            rank = i
            card = f"{rank} of {suit}"
            deck.cards.append(card)

    for i in deck.cards:
        print(i)

dealer = Player("dealer", 0)
create_deck()
