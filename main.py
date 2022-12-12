import os
import random
import time

playFields = []
playModes = ["Player vs BOT", "Player vs Player", "BOT vs BOT"]
playDifficulty = ["Easy (RNG)", "Normal", "Hard (Impossible)"]
numpad = [7, 8, 9, 4, 5, 6, 1, 2, 3]


def get_symbol(num):
    list_symbols = [' ', '✕', '◯']
    return str(list_symbols[int(num)])


def clear_play_field():
    global playFields
    playFields = [0 for i in range(9)]


def print_hi(name):
    print(f'Hi, {name}')


def rand(min_rand, max_rand):
    return random.random() * (max_rand + 1 - min_rand) + min_rand


def get_low_num(num):
    low = "₁₂₃₄₅₆₇₈₉"
    return low[num-1]


def check_field():
    field = playFields
    winLines = [789, 753, 741, 852, 951, 963, 456, 159, 123]
    for xo in [1, 2]:
        for line in winLines:
            score = 0
            for place in str(line):
                num = int(place) - 1
                if field[num] == xo:
                    score += 1
                else:
                    continue
            if score == 3:
                return True
    return False


def print_field(step, _settings, print_out_xo):
    mode = _settings['mode']
    xo = _settings['xo']
    difficulty = _settings['difficulty']
    os.system("cls")
    print("Режим: " + get_mode_name(mode))
    if mode != 1:
        print("Сложность: " + playDifficulty[difficulty])

    if step == 0 and mode:
        print("Первым ходит: " + str(get_symbol(print_out_xo)))
    elif mode != 2:
        print("Сейчас ходит: " + str(get_symbol(print_out_xo)))
    else:
        print("Сейчас ходит: " + str(get_symbol(print_out_xo)))
    print("-=-=-=[" + str((step + 1) if (int(step) + 1 != 10) else "X") + "]=-=-=-")
    field_num = 0
    str_play_field = "    "
    for field in playFields:
        field_num += 1
        if field == 0:
            str_play_field += str(get_low_num(numpad[field_num-1])) + "  "
        else:
            str_play_field += get_symbol(field) + "  "
        if field_num % 3 == 0 and field_num != len(playFields):
            str_play_field += str("\n    ")

    print(str(str_play_field))
    print("-=-=-=-=-=-=-=-")


def check_input(word, length, symbols):
    if not (len(word) <= int(length)) or len(word) == 0:
        return False  # Is not needed length
    for letter in word:
        allowed = False
        for symbol in symbols:
            if letter == str(symbol):
                allowed = True  # letter in allow array
                break
        if not allowed:  # letter out allow array
            return False
    return True


def get_mode_name(num):
    return playModes[num]


def get_user_name(mode, step):
    return ("Player"
            + str((int(step) - 1) % 2 + 1)
            + str(" (BOT)" if mode == 2 or (mode == 0 and (int(step - 1) % 2) == 1) else "")
            )  # PlayerN // PlayerN (BOT)


def play_game(mode, difficulty, xo):
    repeat_game = True
    while repeat_game:

        clear_play_field()
        for step in range(len(playFields) + 1):
            print_out_xo = ((step + int(xo)) % 2) + 1
            _settings = {"mode": int(mode), "difficulty": int(difficulty), "xo": int(xo)}
            print_field(step, _settings, print_out_xo)
            if check_field():
                print(get_user_name(mode, step) + ": WIN!!!")  # Player n: WIN!!! // Player {(BOT)} n: WIN!!!
                break
            if step == len(playFields):
                print(" > DRAW < ")

                continue
            if mode == 1 or (((step % 2) == 0) and (int(mode) != 2)):
                right_place = False
                while not right_place:
                    player_input = input(get_user_name(mode, step - 1) + ", выберите клетку:")
                    valid = check_input(player_input, 1, "0123456789")
                    if not valid:
                        print("Wrong input!")
                        continue
                    player_input = str(numpad[int(player_input) - 1])
                    player_input = int(player_input)-1
                    if 9 > player_input >= 0:
                        if playFields[player_input] == 0:
                            right_place = not right_place
                        else:
                            print("the place is occupied!\n")
                    else:
                        print("Wrong place! (1-9)\n")
                playFields[player_input] = print_out_xo
            else:
                if difficulty == 0:
                    bot_input = bot_random()
                else:
                    bot_input = bot_normal(print_out_xo)
                if bot_input is None:
                    bot_input = bot_random()
                playFields[int(bot_input)] = print_out_xo
            if mode == 2:
                time.sleep(1.5)  # For some visual succ
        verify = False
        while not verify:
            end_game = input("Повторим? (y/n): ")
            verify = check_input(end_game, 1, "yn")
            if not verify:
                print("Wrong input!")
        if end_game == "n":
            repeat_game = False


def bot_normal(xo):
    field = playFields
    winLines = [789, 753, 741, 852, 951, 963, 456, 159, 123]
    scoreLines = []

    # Get score all lines
    for line in winLines:
        score = 0
        for place in str(line):
            num = numpad[int(place)-1] - 1
            if field[num] == xo:
                score += 1
            elif not field[num] == 0:
                score -= 1
        scoreLines.append({'line': line, 'score': score})
    # sort by score
    scoreLines.sort(key=lambda i: i['score'])
    lowestScore = scoreLines[0]
    biggestScore = scoreLines[len(scoreLines)-1]
    # check low & big lines
    if lowestScore['score'] == -2:
        bestLine = lowestScore['line']
    elif biggestScore['score'] == 2:
        bestLine = lowestScore['line']
    else:
        return bot_random()

    # place in bestLine
    for place in str(bestLine):
        num_place = numpad[int(place)-1]-1
        if playFields[num_place] == 0:
            return int(num_place)


def bot_random():
    rng = int(rand(1, 9)) - 1
    place_clear = False
    modifier = 0
    while not place_clear:
        if (int(rng) + int(modifier)) < len(playFields):
            if playFields[rng + int(modifier)] == int(0):  # Проверка свободно ли поле?
                place_clear = not place_clear
                return rng + int(modifier)
        if (int(rng) - int(modifier)) >= int(0):
            if playFields[rng - int(modifier)] == int(0):  # Проверка свободно ли поле?
                place_clear = not place_clear
                return rng - int(modifier)
        if 10 < (int(rng) + int(modifier)) < 0:
            quit("Find place loop")
        modifier += 1


def settings_game():
    valid_inputs = False
    xo_bool = False
    difficulty_bool = False
    while not valid_inputs:
        mode = input("vsBOT(0) vsPlayer(1) AFK(2): \n")
        valid = check_input(mode, 1, "0123456789")
        if not valid:
            print("Wrong input!")
            continue
        if 0 <= int(mode) <= 2:
            valid_inputs = True
        else:
            print("Wrong input: [" + str(mode) + "].")

    if int(mode) != 2:
        valid_inputs = False
        while not valid_inputs:
            question = ["Choose", "Who is first"]
            xo = input(question[int(mode)] + " ☓[0] or 0[1]: \n")
            valid = check_input(xo, 1, "0123456789")
            if not valid:
                print("Wrong input!")
                continue
            if xo == "0" or xo == "1":
                valid_inputs = True
            else:
                print("Wrong input: [" + xo + "].")
    else:
        xo = 0
    if int(mode) != 1:
        valid_inputs = False
        while not valid_inputs:
            difficulty = input("""Difficulty: (Hard'nt)
0 - Easy
1 - Normal
2 - Hard
Set a difficulty: """)
            valid = check_input(difficulty, 1, "0123456789")
            if not valid:
                print("Wrong input!")
                continue
            if 0 <= int(difficulty) <= 2:
                valid_inputs = True
            else:
                print("Wrong input: [" + difficulty + "].")
    else:
        difficulty = 0
    return {"mode": int(mode), "difficulty": int(difficulty), "xo": int(xo)}


# main start
if __name__ == '__main__':
    os.system("title XO the Game")
    os.system("mode con cols=50 lines=10")
    print_hi('this is XO the Game!')

    reset_game = True
    while reset_game:
        settings = settings_game()
        play_game(settings["mode"], settings["difficulty"], settings["xo"])
        verify = False
        while not verify:
            change_options_game = input("Новая игра с новыми настройками? (y/n): ")
            verify = check_input(change_options_game, 1, "yn")
            if not verify:
                print("Wrong input!")
        if change_options_game == "n":
            reset_game = False

    input("Нажмите ENTER чтобы завершить программу...")
    # TODO:
    #  - P2P Lan
