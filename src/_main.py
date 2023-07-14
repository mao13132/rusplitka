import random
from datetime import datetime
from time import perf_counter
from src._start_parser import start_parser


def main(step1, step2, step3, step4):
    start_job = perf_counter()
    print(f'Начинаю работу парсинга {datetime.now().strftime("%H:%M:%S")}')

    status_running = start_parser(step1, step2, step3, step4)

    over_job = perf_counter() - start_job
    over_job = over_job / 60
    print(f'Закончил работу парсинга  {datetime.now().strftime("%H_%M_%S")} затратив времени: {over_job} минут '
          f'Результат парсинга: "{status_running}"')
