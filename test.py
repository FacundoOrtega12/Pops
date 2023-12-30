import random

def main():
    level = get_level()
    ans_count = 0
    question_count = 0
    score = 0
    while question_count < 10:
        x = generate_integer(level)
        y = generate_integer(level)
        while ans_count < 3:
            ans = input(f"{x} + {y} = ")
            try:
                ans = int(ans)
                actans = x + y
                if ans == actans:
                    question_count = question_count + 1
                    score = score + 1
                    break
                else:
                    print("EEE")
                    ans_count = ans_count + 1
                    if ans_count == 3:
                        print(f"{x} + {y} = {actans}")
                        ans_count = 0
                        question_count = question_count + 1
                        break
                    else:
                        pass

            except ValueError:
                print("EEE")
                ans_count = ans_count + 1
                if ans_count == 3:
                    print(f"{x} + {y} = {actans}")
                    ans_count = 0
                    question_count = question_count + 1
                    break
                else:
                    pass
    print(f"Score: {score}")

def get_level():
    while True:
        level = input("Level: ")
        try:
            level = int(level)
            if level == 1 or level == 2 or level == 3:
                return level
            else:
                pass
        except ValueError:
            pass

def generate_integer(level):
    if level == 1:
        rand = random.randint(0,9)
        return rand
    elif level == 2:
        rand = random.randint(10,99)
        return rand
    else:
        rand = random.randint(100,999)
        return rand



if __name__ == "__main__":
    main()

