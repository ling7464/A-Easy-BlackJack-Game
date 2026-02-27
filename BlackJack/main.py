import Porke

def main():
    game = Porke.Game(num=8) # num表示有几副牌
    while True:
        print("\n--- 新的一局 ---\n")
        game.play_round()
        again = input("再来一局吗？(yes/no)\n").lower()
        if again != 'yes':
            break


if __name__ == "__main__":
    main()