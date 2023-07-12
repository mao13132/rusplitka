import random
from datetime import datetime

from browser.createbrowser_theard import CreatBrowser
from save_result_tovar import SaveResultTovar

from time import perf_counter

from sql.bot_connector import BotDB
from src._start_parser import start_parser
from src.temp_plu_in_coll import coll_data
from src.tovar_parser_one_theard import TovarParserOneTheard


def main(step1, step2, step3, step4):

    start_job = perf_counter()
    print(f'Начинаю работу парсинга {datetime.now().strftime("%H:%M:%S")}')

    status_running = start_parser(step1, step2, step3, step4)

    over_job = perf_counter() - start_job
    over_job = over_job / 60
    print(f'Закончил работу парсинга  {datetime.now().strftime("%H_%M_%S")} затратив времени: {over_job} минут '
          f'Результат парсинга: "{status_running}"')

    # start_job = perf_counter()
    # print(f'Начинаю парсинг товаров {datetime.now().strftime("%H_%M_%S")}')
    # save_plu_tovar()
    # over_job = perf_counter() - start_job
    # over_job = over_job / 60
    # print(f'Закончил парсинг товаров {datetime.now().strftime("%H_%M_%S")} завтратив времени: {over_job} минут')
    #
    # print(f'Работу закончил')

    # status_running = start_parser(step1, step2, step3, step4)
    #
    # if not status_running:
    #     return False
    #
    # return True


def save_plu_tovar():
    pass
    # browser_core = CreatBrowser('collection', True)
    #
    # tavar_data = TovarParserOneTheard(browser_core.driver, BotDB).start_pars()
    #
    # # from src.temp_over_tovar import tovar_over
    # # tavar_data = tovar_over
    #
    # file_name = f'{datetime.now().strftime("%H_%M_%S")}'
    #
    # SaveResultTovar(tavar_data).save_file(file_name)
    #
    # print()


if __name__ == '__main__':
    step1_get_brand = False  # Шаг с парсингом брендов

    step2_pars_brand_collections = False     # Шаг с парсингом коллекций в бренде

    step3_pars_in_collection_product = True     # Шаг с парсингом внутренностей коллекций и забором товаров из них

    step4_pars_product = True       # Шаг с парсингом внутренностей товаров

    main(step1_get_brand, step2_pars_brand_collections, step3_pars_in_collection_product, step4_pars_product)
