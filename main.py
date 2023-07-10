import random
from datetime import datetime

from browser.createbrowser_theard import CreatBrowser
from save_result import SaveResult
from save_result_tovar import SaveResultTovar
from src.plu_parse import PluParser
from src.source_parse import SourceParse


from time import perf_counter

from sql.bot_connector import BotDB
from src.temp_plu_in_coll import coll_data
from src.tovar_parser_one_theard import TovarParserOneTheard


def main():

    collec_count_page = 1

    browser_core = CreatBrowser('collection', True)



    print(f'Парсер запущен. Получаю данные')

    data_good = SourceParse(browser_core.driver, collec_count_page).start_pars()
    # from src.temp_source_collect import list_col
    # data_good = list_col[:2]


    print(f'Собрал {len(data_good)} коллекций на обработку')

    collection_data = PluParser(browser_core.driver, data_good, BotDB).start_pars()
    # collection_data = coll_data

    print(f'Обработал {len(collection_data)} коллекций')

    file_name = f'{datetime.now().strftime("%H_%M_%S")}'

    SaveResult(collection_data).save_file(file_name)


    print()

def save_plu_tovar():
    browser_core = CreatBrowser('collection', True)

    tavar_data = TovarParserOneTheard(browser_core.driver, BotDB).start_pars()

    # from src.temp_over_tovar import tovar_over
    # tavar_data = tovar_over

    file_name = f'{datetime.now().strftime("%H_%M_%S")}'

    SaveResultTovar(tavar_data).save_file(file_name)

    print()




if __name__ == '__main__':
    start_job = perf_counter()
    print(f'Начинаю парсинг коллекций {datetime.now().strftime("%H_%M_%S")}')
    main()
    over_job = perf_counter() - start_job
    over_job = over_job / 60
    print(f'Закончил парсинг коллекций {datetime.now().strftime("%H_%M_%S")} завтратив времени: {over_job} минут')




    start_job = perf_counter()
    print(f'Начинаю парсинг товаров {datetime.now().strftime("%H_%M_%S")}')
    save_plu_tovar()
    over_job = perf_counter() - start_job
    over_job = over_job / 60
    print(f'Закончил парсинг товаров {datetime.now().strftime("%H_%M_%S")} завтратив времени: {over_job} минут')

    print(f'Работу закончил')
