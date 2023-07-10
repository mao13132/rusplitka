import random
import time
from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import threading

# from threading import BoundedSemaphore

from browser.createbrowser_theard import CreatBrowser
from save_result import SaveResult

from src.get_plu_in_coll import GetPluInColl


class TovarParser:
    def __init__(self, BotDB):
        self.post_data = {}
        self.all_xarakt = []
        self.BotDB = BotDB

        self.task_list = []
        self.error_list = []

    def load_page(self, url, name_theard):
        try:

            self.driver.get(url)
            return True
        except TimeoutException:
            # print(f'Поток: {name_theard} вышел таймаут - перезагружаю страницу')
            return False

        except Exception as es:
            # print(f'Ошибка при заходе на "{url}" "{es}" {self.name}')

            return False

    def check_load_page(self, name_post):

        if len(name_post) > 15:
            name_print = name_post
            name_post = name_post[:15]

        try:
            # WebDriverWait(self.driver, 15).until(
            #     EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "{name_post[:-3]}")]')))
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "Написать директору")]')))
            return True
        except Exception as es:
            print(f'Ошибка при загрузке "{name_post}" поста  {self.name}')
            return False

    def loop_load_page(self, post, name_theard):
        coun = 0
        coun_ower = 4

        while True:
            coun += 1

            if coun >= coun_ower:
                print(f'Не смог зайти в пост {post["name"]}')
                self.error_list.append(self.id_pk)
                return False

            response = self.load_page(post['link'], name_theard)

            if not response:
                continue

            result_load = self.check_load_page(post['name'])

            if not result_load:
                self.driver.refresh()
                time.sleep(1)
                continue

            return True

    def get_name_xarakter(self, xar):
        try:
            name_xar = xar.find_element(by=By.XPATH, value=f".//span[contains(@class, 'label')]").text
        except Exception as es:
            res = self.check_load_page('123123')
            if not res:
                print(f'Ошибка при получение get_name т.к. страница не открылась')
                return 'error'

            print(f'Ошибка при получении get_name_xarakter  {self.name}')

            return ''
        try:
            name_xar = name_xar.replace(':', '')
        except:
            pass

        return name_xar

    def get_value_name_xarakter2(self, xar):
        try:
            _xar = xar.find_elements(by=By.XPATH, value=f".//td")
        except Exception as es:
            # print(f'Ошибка при получении get_value_name_xarakter2 " имя {self.name}')
            check_load = self.check_load_page('123')
            if not check_load:
                # print(f'Ошибка из за пустой страницы {self.name}')
                return 'error', 'error'

            return '', ''
        try:
            name_xar = _xar[0].text.replace(':', '')
        except:
            # print(f'Ошибка при получении name_xar имя {self.name}')
            name_xar = ''
        try:
            value_xar = _xar[1].text.strip()
        except:
            # print(f'Ошибка при получении value_xar  имя {self.name}')
            value_xar = ''

        return name_xar, value_xar

    def get_value_xarakter(self, xar):
        try:
            list_xar = xar.find_element(by=By.XPATH, value=f".//*[contains(@class, 'prop')]").text
        except Exception as es:
            check_paga = self.check_load_page('123')
            if not check_paga:
                print(f'Пустая страница get_value_xarakter')
                return False

            # print(f'Ошибка при получении get_value_xarakter "{es}" {self.name}')

            return ''

        return list_xar

    def itter_xarakter(self, all_list):

        good_list = {}

        for xar in all_list:
            # dict_one_xar = {}
            name_xar = self.get_name_xarakter(xar)

            if name_xar == 'error':
                return False

            value_xar = self.get_value_xarakter(xar)

            if value_xar == '' or not value_xar or name_xar == False or name_xar == '':
                # print(f'Добавил ошибочный id_pk на повторную обработку')
                return False

            good_list[name_xar] = value_xar

            val_black_list = ['Производитель', 'Коллекция', 'Артикул', 'Размер', 'Страна', 'Тип']

            if name_xar not in self.all_xarakt and name_xar not in val_black_list:
                self.all_xarakt.append(name_xar)

        return good_list

    def itter_xarakter2(self, all_list, list_har):

        good_list = {}

        for xar in all_list:
            # dict_one_xar = {}
            name_xar, value_xar = self.get_value_name_xarakter2(xar)
            # value_xar = self.get_value_xarakter2(xar)
            if name_xar == 'error':
                return False

            if name_xar == '' and value_xar == '':
                # print(f'Не смог найти характеристики у {self.name}')
                continue

            if name_xar == 'Назначение':
                value_xar = ';'.join(x.replace('-', '').strip() for x in value_xar.split('\n'))

            list_har[name_xar] = value_xar
            # good_list[name_xar] = value_xar

            if name_xar not in self.all_xarakt:
                self.all_xarakt.append(name_xar)

        return list_har

    def all_list_xarakt(self):
        try:
            xarakt_list = self.driver.find_elements(by=By.XPATH, value=f"//div[contains(@class, 'cart__infos')]"
                                                                       f"//*[contains(@class, 'cart__infos-col')]"
                                                                       f"//*[contains(@class, 'infos-line')]")

        except Exception as es:
            print(f'Ошибка при получении all_list_xarakt "{es}"')

            return []

        return xarakt_list

    def all_list_xarakt2(self):
        count = 0
        while True:
            count += 1

            if count > 3:
                return False
            try:
                xarakt_list = self.driver.find_elements(by=By.XPATH, value=f"//div[@id='charCharacters']//tr")

            except Exception as es:
                print(f'Ошибка при получении all_list_xarakt "{es}"')

                continue

            check_res, _ = self.get_value_name_xarakter2(xarakt_list[0])

            if check_res == '':
                # print(f'Слишком рано берёться все характеристики2 {self.name}')
                time.sleep(1)
                continue
            else:
                # print(f'Подтверждаю успешное взятие хар2 {check_res} {self.name}')

                return xarakt_list

        # return xarakt_list

    def get_xarakt_list(self):

        all_list = self.all_list_xarakt()
        if all_list == []:
            return []

        good_dict = self.itter_xarakter(all_list)

        if not good_dict:
            return False

        return good_dict

    def get_xarakt_list2(self, list_har):

        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'Характеристики')]").click()
        except Exception as es:
            print(f'Не смог переключить характеристики нижние 2 "{es}"')
            return []

        all_list = self.all_list_xarakt2()

        # print(f'Всего общих хакрактеристик2: {len(all_list)}')

        if all_list == []:
            return []

        good_dict = self.itter_xarakter2(all_list, list_har)

        return good_dict

    def get_text(self):

        try:
            text = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@itemprop, 'description')]").text
        except Exception as es:
            print(f'Ошибка при получении get_text "{es}"')
            check_load_page = self.check_load_page('123')
            if not check_load_page:
                print(f'Пустая страница парсинг текста')

                return ''

            return ''

        if text == '':
            print(f'Пустое описание')

        try:
            text = '\n'.join(x for x in text.split('\n')[:-1])
        except:
            text = text


        return text

        return text

    def get_price(self):
        try:
            text_post = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'cart__down')]"
                                                                    f"//*[contains(@class, 'price-real')]").text


        except:
            return 0

        try:
            int(text_post)
        except Exception as es:

            print(f'Ошибка при get_price "{es}"')

            return 0

        return text_post

    def get_edinicha(self):
        try:
            text_post = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'cart__down')]"
                                                                    f"//*[contains(@class, 'cart__price cart__price_pc')]").text


        except:
            return 'шт'

        try:
            ed = text_post.split('/')[-1]
        except Exception as es:

            print(f'Ошибка при get_price "{es}"')

            return 'шт'

        return ed

    def _get_image_in_row(self, row):
        try:
            link_image = row.find_element(by=By.XPATH, value=f".//img").get_attribute('src')
        except Exception as es:
            # print(f'Ошибка при получении _get_image_in_row "{es}" имя "{self.name}" игнорировать можно')

            return ''

        return link_image

    def itter_get_image(self, rows_list):
        good_list_photo = []

        for row in rows_list:
            get_image = self._get_image_in_row(row)
            if get_image:
                good_list_photo.append(get_image)

        return good_list_photo

    def get_one_image(self):
        try:
            _image = self.driver.find_element(by=By.XPATH, value=f"//*[@class='cart__images']"
                                                                 f"//*[contains(@class, 'slick-active')]") \
                .get_attribute('href')
        except Exception as es:
            print(f'Ошибка при получении галерии get_one_image "{es}"  имя "{self.name}"')

            return []

        return [_image]

    def _get_image_gallery_list(self):
        try:
            image_gallery_list = self.driver.find_elements(by=By.XPATH, value=f"//*[@class='cart__images']"
                                                                              f"//picture")
        except Exception as es:
            print(f'Ошибка при получении галерии PLU "{es}"')

            return []

        return image_gallery_list

    def get_photo(self):
        rows_List = self._get_image_gallery_list()

        if rows_List == []:
            rows_List = self.get_one_image()
            return rows_List

        good_image_list = self.itter_get_image(rows_List)

        return good_image_list

    def _one_pars(self, sql_tovar, browser_itter):
        # print(f'Получил браузер {browser_itter}')
        with self.pool:

            name_theard = threading.currentThread().name

            browser_core = browser_itter

            if not browser_core:
                self.semafor_browser.append(browser_itter)
                return False

            try:
                id_pk, url, name, _, artikle, collection, prozvoditel, _ = sql_tovar
            except:
                self.error_list.append(id_pk)
                self.semafor_browser.append(browser_itter)
                return False

            try:
                # print(f'Начинаю работать с {name}')

                self.driver = browser_core.driver

                self.id_pk = id_pk
                self.name = name

                if not sql_tovar:
                    self.error_list.append(id_pk)
                    self.semafor_browser.append(browser_itter)
                    return False
                # print(f'Поток: {name_theard} начал обработку {name}')

                post = {}
                post['name'] = name
                post['id_pk'] = id_pk
                post['link'] = url
                post['artikle'] = artikle
                post['collection'] = collection
                post['prozvoditel'] = prozvoditel

                self.driver.set_page_load_timeout(15)

                result_load_page = self.loop_load_page(post, name_theard)

                if not result_load_page:
                    self.error_list.append(id_pk)
                    self.semafor_browser.append(browser_itter)
                    return False

                res_xart = self.get_xarakt_list()

                if not res_xart:
                    self.error_list.append(id_pk)
                    # browser_core.driver.close()
                    # browser_core.driver.quit()
                    self.semafor_browser.append(browser_itter)
                    return False

                post['xarakt'] = res_xart

                post['text'] = self.get_text()

                res = self.get_xarakt_list2(post['xarakt'])
                if not res:
                    self.error_list.append(id_pk)
                    # browser_core.driver.quit()
                    self.semafor_browser.append(browser_itter)
                    return False

                post['price'] = self.get_price()

                post['edinicha'] = self.get_edinicha()

                image_list = self.get_photo()

                try:
                    image_list = ' '.join(x for x in image_list)
                except:
                    image_list = ''

                post['image'] = image_list

                self.links_post.append(post)

                print(f'Поток: {name_theard} успешно обработал {name}')

            except Exception as es:
                print(f'Ошибка внутри потока "{es}"')
                self.error_list.append(id_pk)
                self.semafor_browser.append(browser_itter)
            finally:
                # browser_core.driver.close()
                # browser_core.driver.quit()
                self.semafor_browser.append(browser_itter)

            return True

    def start_pars(self):

        self.links_post = []

        good_over_count = 0

        max_connections = 5
        self.pool = threading.BoundedSemaphore(value=max_connections)

        count_db_tovar = self.BotDB.get_all_count()

        self.semafor_browser = []
        self.ower_browser = []

        for x in range(max_connections):
            # browser = f'Браузер - {x}'
            browser = CreatBrowser(x, True)

            self.semafor_browser.append(browser)
            self.ower_browser.append(browser)

        # for id_pk_ in range(100):
        for id_pk_ in range(count_db_tovar):

            sql_tovar = self.BotDB.get_tovar(id_pk_ + 1)
            name_th = f'thr-{random.randint(1, 50)}'

            with self.pool:

                while self.semafor_browser == []:
                    print(f'Список браузеров пуст имя потока {name_th}')
                    time.sleep(5)

                try:
                    browser_itter = self.semafor_browser.pop()
                except Exception as es:

                    print(f'Список браузеров пуст "{es}" имя потока {name_th}')
                    self.error_list.append(id_pk_ + 1)
                    continue


            try:
                trh = threading.Thread(target=self._one_pars,
                                       args=(sql_tovar, browser_itter), name=(name_th))

                # trh.setDaemon(True)
                trh.browser = browser_itter

                trh.start()

                self.task_list.append(
                    {
                        'trh': trh,
                        'task': sql_tovar
                    }
                )

            except Exception as es:
                print(f'Ошибка потока: {es}')

            if id_pk_ % 10 == 0 and id_pk_ != 0:

                print(f'Обработал {id_pk_} товаров итерация {id_pk_}')
                print(f'Успешно {len(self.links_post)} товаров')
                print(f'Повторная обработка: {len(self.error_list)}')

        print(f'Итог: собрал информацию с {len(self.links_post)} товаров')
        [x['trh'].join() for x in self.task_list]
        [x.driver.quit() for x in self.ower_browser]

        result_dict = {}
        result_dict['name_colums'] = self.all_xarakt
        result_dict['result'] = self.links_post
        print(f'Ошибочный лист: {self.error_list}')

        return result_dict
