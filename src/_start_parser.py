import os

from browser.createbrowser_theard import CreatBrowser
from save_coll_and_products import SaveCollAndProduct
from save_result_tovar import SaveResultTovar

from sql.bot_connector import BotDB
from save_result import SaveResult
from src.get_brands import GetBrands
from src.plu_parse import PluParser
from src.source_parse import SourceParse
from datetime import datetime

from src.tovar_parser_one_theard import TovarParserOneTheard

from check_dir import check_dirs


def start_parser(step1, step2, step3, step4):
    try:
        check_dirs()

        collec_count_page = 0

        browser_core = CreatBrowser('collection', True)

        if step1:
            """GetBrands"""
            print(f'Шаг1 запущен. Получаю данные')
            GetBrands(browser_core.driver).start_pars_brands()

        if step2:
            print(f'Шаг2 запущен. Получаю данные')

            check_file = SaveResultTovar.check_brands()

            if not check_file:
                print(f'Ошибка, нет файла с брендами не могу запустить шаг 2. Запустите шаг 1')
                return False

            list_url_brands = SaveResultTovar.load_file()

            if list_url_brands == []:
                print(f'Ошибка, файл с брендами пуст не могу запустить шаг 2. Запустите шаг 1')
                return False

            list_brands = [x for x in list_url_brands.split('\n') if x != '']

            for url in list_brands:
                name_collection = url.split('/')[-2]

                print(f'Запускаю парсинг "{name_collection}"')
                data_good = SourceParse(browser_core.driver, collec_count_page).start_pars(url)

                file_name_json = SaveResultTovar.save_collection(name_collection, data_good)

                print(f'Сохранил коллекцию {name_collection} в файл {file_name_json}')

        if step3:
            print(f'Шаг3 запущен. Получаю данные')
            # from src.temp_source_collect import list_col
            # data_good = list_col[:10]

            dir_ = os.getcwd() + r'/files/collections/'
            # dir_ = os.getcwd() + f'\\files\\collections\\'
            collection_list_files = [f'{x}' for x in os.listdir(dir_) if 'json' in x]

            if collection_list_files == []:
                print(f'Нет данных для парсинга по коллекциям. Запустите шаг2')
                return False

            full_tavar_data = {}
            full_tavar_data['name_colums'] = []
            full_tavar_data['result'] = []
            collection_data_full = []

            for file_collection in collection_list_files:

                _file_collection = dir_ + file_collection

                data_good = SaveResultTovar.load_collection(_file_collection)

                proiz = data_good[0]['proiz']

                print(f'Собрал {len(data_good)} коллекций на обработку')

                collection_data = PluParser(browser_core.driver, data_good, BotDB).start_pars()

                collection_data_full.extend(collection_data)

                print(f'Обработал {len(collection_data)} коллекций')

                _file_name = file_collection.split('.')[0]

                file_name = f'{_file_name}_{datetime.now().strftime("%H_%M_%S")}'

                file_name_json = SaveResultTovar.save_col_and_tovar(file_name, data_good)

                # SaveResult(collection_data).save_file(file_name)
                if step4:

                    tavar_data = TovarParserOneTheard(browser_core.driver, BotDB).start_pars(proiz)

                    if not tavar_data:
                        continue

                    file_name = f'full_{proiz}_collections_and_products_{datetime.now().strftime("%H_%M_%S")}'

                    try:
                        full_tavar_data['name_colums'].extend(tavar_data['name_colums'])
                        full_tavar_data['result'].extend(tavar_data['result'])
                    except:
                        pass

                    SaveCollAndProduct(collection_data, tavar_data).save_file(file_name)
                    # SaveResultTovar(tavar_data).save_file(file_name)
            file_name = f'all_{proiz}_collections_and_products_{datetime.now().strftime("%H_%M_%S")}'
            SaveCollAndProduct(collection_data_full, full_tavar_data).save_file(file_name)

        print()
    except BaseException as es:
        print(f'Ошибка _start_parser потока "{es}"')

        return False

    return True
