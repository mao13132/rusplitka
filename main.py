import random
from datetime import datetime

from browser.createbrowser import CreatBrowser
from save_result import SaveResult
from save_result_tovar import SaveResultTovar
from src.plu_parse import PluParser
from src.source_parse import SourceParse
from src._no_source_parse_plu import SourceParsePlu

from src.temp import *

from time import perf_counter

from sql.bot_connector import BotDB
from src.tovar_parser import TovarParser


def main():

    collec_count_page = 0

    browser_core = CreatBrowser()



    print(f'Парсер запущен. Получаю данные')

    # data_good = SourceParse(browser_core.driver, collec_count_page).start_pars()
    from src.temp_source_collect import list_col
    data_good = list_col[:2]


    print(f'Собрал {len(data_good)} коллекций на обработку')

    collection_data = PluParser(browser_core.driver, data_good, BotDB).start_pars()
    # collection_data = coll_data

    print(f'Обработал {len(collection_data)} коллекций')

    file_name = f'{datetime.now().strftime("%H_%M_%S")}'

    SaveResult(collection_data).save_file(file_name)


    print()

def save_plu_tovar():
    collec_count_page = 0

    # browser_core = CreatBrowser()

    tavar_data = TovarParser(BotDB).start_pars()
    # tavar_data = TovarParser(browser_core.driver, BotDB).start_pars()
    # from src.temp_good_tovar import good_list
    # tavar_data = good_list

    file_name = f'{datetime.now().strftime("%H_%M_%S")}'

    SaveResultTovar(tavar_data).save_file(file_name)

    print()

def save_plu_tovar_one_theard():
    collec_count_page = 0

    name_brows = f'Profile' + str(random.randint(1, 4))
    browser_core = CreatBrowser(name_brows)

    from src.tovar_parser_one_theard import TovarParserOneTheard
    tavar_data = TovarParserOneTheard(browser_core.driver, BotDB).start_pars()
    # from src.temp_good_tovar import good_list
    # tavar_data = good_list

    file_name = f'{datetime.now().strftime("%H_%M_%S")}'

    SaveResultTovar(tavar_data).save_file(file_name)

    print()



if __name__ == '__main__':
    # main()
    start_job = perf_counter()
    print(f'Начинаю парсинг товаров {datetime.now().strftime("%H_%M_%S")}')
    # save_plu_tovar()
    save_plu_tovar_one_theard()
    over_job = perf_counter() - start_job
    over_job = over_job / 60
    print(f'Закончил парсинг товаров {datetime.now().strftime("%H_%M_%S")} завтратив времени: {over_job} минут')

    print(f'Работу закончил')
