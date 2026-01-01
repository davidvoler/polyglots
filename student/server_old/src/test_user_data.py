from models.user_data_new.user_data import UserData
from models.user_data_new.user_params import UserParams
from models.user_data_new.app_params import AppParams
from models.user_data_new.results import Results
import random





def create_user_data(user_id: str, lang: str) -> UserData:
    return UserData(user_id=user_id, lang=lang)

def evaluate_results(user_data: UserData, results: list[Results]) -> UserData:
    return user_data.history.update_score(results)


def gen_parts(user_data: UserData):
    return user_data.history.get_parts()


def gen_results(user_data: UserData, parts: list[int], success_rate: float = 0.6) -> list[Results]:
    correct_parts = int(round(len(parts) * success_rate))
    incorrect_parts = len(parts) - correct_parts
    results = []
    for i in range(correct_parts):
        results.append(Results(
            user_id=user_data.user_id,
            lang=user_data.lang,
            part_id=parts[i],
            answer_delay_ms=random.randint(500, 5000),
            play_times=random.randint(1, 4),
            attempts=1,
            ))
    for i in range(incorrect_parts):
        results.append(Results(
            user_id=user_data.user_id,
            lang=user_data.lang,
            part_id=parts[i + correct_parts],
            answer_delay_ms=random.randint(500, 5000),
            play_times=random.randint(1, 4),
            attempts=random.randint(2, 4),
            ))
    return results

def iterate_test(rounds: int = 100):
    user_data = create_user_data(f"test", "eng")
    for i in range(rounds):
        parts = gen_parts(user_data)
        results = gen_results(user_data, parts)
        evaluate_results(user_data, results)
        print(f"Round {i} done")

def print_user_data(user_data: UserData):
    print(f"User ID: {user_data.user_id}")
    print(f"Lang: {user_data.lang}")
    print(f"History: {user_data.history}")
    print(f"User Params: {user_data.user_params}")
    print(f"App Params: {user_data.app_params}")
    print(f"Results: {user_data.results}")

if __name__ == "__main__":
    iterate_test()



