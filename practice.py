import random
from typing import Dict, List
from datetime import datetime

def generate_problems(qty: int = 10, multiple: int | None = None) -> List[Dict[str, int]]:
    """"""
    problems = []
    for _ in range(qty):
        if multiple is None:
            a = random.randint(0, 9)
        elif 0 <= multiple <= 9:
            a = multiple
        else:
            a = random.randint(0, 9)
        if problems:
            last_b = problems[-1]["b"]
        else:
            last_b = -1
        b = random.randint(0, 9)
        while b == last_b:
            b = random.randint(0, 9)
        problem = {
            "a": a,
            "b": b,
            "correct_answer": a * b,
            "user_answer": None,
        }
        problems.append(problem)
    return problems


def present_problems(problems):
    for i, p in enumerate(problems, start=1):
        response = input(f"{i}. {p['a']} x {p['b']} = ")
        p["user_answer"] = int(response)
    return problems


def present_results(problems, duration):
    total_problems = len(problems)
    for p in problems:
        p["correct"] = p["user_answer"] == p["correct_answer"]
    correct_count = len([x for x in problems if x["correct"]])
    
    print()
    print("Here are your detailed results:")
    # print()
    for i, p in enumerate(problems, start=1):
        # print(f"{i}. {p['a']} x {p['b']} = {p['correct_answer']}")
        print(f"{i}. {p['a']} x {p['b']} = {p['correct_answer']}. You answered {p['user_answer']}: {'✅' if p['correct'] else '❌'}")
        # print()
    print(f"You completed this problem set in {duration}")
    print(
        f"You got {correct_count} correct answers out of {total_problems}. "
        f"That's {round(correct_count / total_problems * 100, 2)}%"
    )

def main(multiple):
    problems = generate_problems(multiple=multiple)
    start = datetime.now()
    answers = present_problems(problems)
    duration = datetime.now() - start
    present_results(answers, duration)
    return


if __name__ == "__main__":
    print("Welcome to multiplication practice!".upper())
    multiple = input("Would you like to practice a specific number? (Enter for random): ")
    if multiple in [str(x) for x in range(10)]:
        multiple = int(multiple)
    else:
        multiple = None
    print(f"{multiple = }")
    main(multiple)

