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


if __name__ == '__main__':
    step1_get_brand = False  # Шаг с парсингом брендов

    step2_pars_brand_collections = True  # Шаг с парсингом коллекций в бренде

    step3_pars_in_collection_product = True  # Шаг с парсингом внутренностей коллекций и забором товаров из них

    step4_pars_product = True  # Шаг с парсингом внутренностей товаров

    main(step1_get_brand, step2_pars_brand_collections, step3_pars_in_collection_product, step4_pars_product)
