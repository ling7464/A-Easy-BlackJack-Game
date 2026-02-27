"""
Card类: 代表一张牌
├── 属性: suit(花色♠♥♦♣), rank(牌面A/2-10/J/Q/K)
└── 方法: show()显示牌面

Deck类: 一副牌
├── 属性: cards列表(52张Card对象)
├── __init__: 生成52张牌并shuffle
└── deal(): 弹出最后一张牌

Player类: 玩家/庄家
├── 属性: hand(手牌列表), name
└── 方法: 
    ├── add_card(card): 加牌到手牌
    ├── calculate_score(): 计算点数(核心难点)
    └── show_hand(hidden=False): 显示手牌,hidden=True时隐藏第一张

Game类: 游戏控制
├── 属性: deck, player, dealer
└── 方法:
    ├── play_round(): 进行一局游戏
    ├── player_turn(): 玩家回合循环
    ├── dealer_turn(): 庄家自动逻辑
    └── determine_winner(): 判断胜负
"""
import random
import time


# 定义一张牌，确定他的样式和数值
class Card:
    # 定义扑克的花色和牌面
    SUITS = ['♠', '♥', '♦', '♣']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    # 初始化Card对象的参数
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # 显示牌面
    "使用__repr__魔术方法可以在打印对象时同步返回值"
    def __repr__(self):
        return f"{self.suit}{self.rank}"
    
    # 确定卡牌的面值
    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # A初始值为11，后续根据需要调整为1
        else:
            return int(self.rank)


# 定义牌组，并且可以洗牌和发牌
class Deck:

    "__init__会在用类生成对象的时候自动执行"
    def __init__(self, num: int):
        # 笛卡尔积生成一副牌，同时洗牌
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS] * num
        random.shuffle(self.cards)

    # 整牌，将牌的顺序打乱并从牌堆顶层发牌
    def deal(self, count: int = 1): # count表示发牌的数量，默认为1
        if len(self.cards) < count:
            return None
        return [self.cards.pop() for _ in range(count)]

# 使用Deck生成的对象，只需要直接调用deal方法就可以发牌了


class Player:

    # 初始化玩家的名字和手牌
    def __init__(self, name: str):
        self.name = name
        self.hand = []

    # 添加手牌 
    # (此处若不加以区分，直接append会导致发多张牌时手牌列表嵌套
    # 从而导致sum(card.value() for card in self.hand)处无法正确调用单张扑克里的方法)
    def add_card(self, card):
        if card is None:
            return  None 
        else:
            self.hand.extend(card)

    # 计算点数
    def calculate_score(self) -> int:
        score = sum(card.value() for card in self.hand) # for后的主体“card”被使用了，即func(x) for x in iterable

        # 调整A的点数，如果总分超过21且有A，则将A的点数从11调整为1
        aces = sum(1 for card in self.hand if card.rank == 'A')
        while score > 21 and aces: # and等价于合取，且大于0的整数都可以认为是True
            score -= 10
            aces -= 1
        return score
    
    # 判断是否爆仓
    def is_bust(self) -> bool:
        return self.calculate_score() > 21

    # 清空手牌
    def clear_hand(self):
        self.hand = []


class Game:
    # 初始化流程
    def __init__(self, num: int): # num表示有几副牌
        self.deck = Deck(num)
        self.player = Player("玩家")
        self.dealer = Player("庄家")


    # 结算
    def determine_winner(self):
        player_score = self.player.calculate_score()
        dealer_score = self.dealer.calculate_score()
        print(f"玩家最终点数: {player_score}, 庄家最终点数: {dealer_score}")
        if player_score > dealer_score:
            print("玩家获胜！")
        elif player_score < dealer_score:
            print("庄家获胜！")
        else:
            print("平局！")


    # 进行一局游戏
    def play_round(self):
        # 1、清空上一局的手牌
        self.player.clear_hand()
        self.dealer.clear_hand()

        # 2、发牌
        self.player.add_card(self.deck.deal(2))
        self.dealer.add_card(self.deck.deal(2))

        # 显示初始手牌，庄家第一张牌隐藏
        print(f"玩家手牌: {self.player.hand}, 当前点数: {self.player.calculate_score()}")
        print(f"庄家手牌: ['??', {self.dealer.hand[1]}], 当前点数: {self.dealer.hand[1].value()}") 

        # 3、检查是否有Blackjack
        if self.check_blackjack():
            return
        
        # 4、玩家回合
        self.player_round()
        if self.player.is_bust():
            return
        
        # 5、庄家回合
        self.dealer_round()
        if self.dealer.is_bust():
            return
        
        # 6、结算
        self.determine_winner()


    # 检查合牌
    def check_blackjack(self):
        if self.player.calculate_score() == 21 and self.dealer.calculate_score() == 21:
            print("双方Blackjack,平局")
            return True
        elif self.player.calculate_score() == 21 and self.dealer.calculate_score() != 21:
            print("玩家Blackjack,玩家获胜")
            return True
        elif self.player.calculate_score() != 21 and self.dealer.calculate_score() == 21:
            print("庄家Blackjack,庄家获胜")
            return True
        else:
            return False
            
    # 玩家回合
    def player_round(self):
        # 玩家选择是否要牌，直到玩家选择停牌或爆仓
        while True:
            time.sleep(1)
            choice = input("要牌(Get)还是停牌(Stop)?\n").lower()
            if not choice in ['get', 'stop']:
                print("无效输入，请重新选择。")
                continue
            time.sleep(1)
            if choice == "get":
                self.player.add_card(self.deck.deal())
                print(f"玩家手牌: {self.player.hand}, 当前点数: {self.player.calculate_score()}")
                if self.player.is_bust():
                    print("玩家爆仓，庄家获胜！")
                    return
            elif choice == "stop":
                break
            else:
                print("无效输入，请重新选择。")

    # 庄家回合
    def dealer_round(self):
        # 庄家小于17点持续要牌，否则停牌
        while self.dealer.calculate_score() < 17:
            self.dealer.add_card(self.deck.deal())
            print(f"庄家手牌: {self.dealer.hand}, 当前点数: {self.dealer.calculate_score()}")
            if self.dealer.is_bust():
                print("庄家爆仓，玩家获胜！")
                return
        

if __name__ == "__main__":
    game = Game(num=5) # num表示洗牌次数
    while True:
        game.play_round()
        again = input("再来一局吗？(yes/no)\n").lower()
        if again != 'yes':
            break

    