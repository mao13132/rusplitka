import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from save_result import SaveResult
from save_result_tovar import SaveResultTovar

from src.get_plu_in_coll import GetPluInColl


class TovarParserOneTheard:
    def __init__(self, driver, BotDB):
        self.driver = driver
        self.post_data = {}
        self.all_xarakt = []
        self.BotDB = BotDB

    def load_page(self, url):
        try:

            self.driver.get(url)
            return True
        except Exception as es:
            print(f'Ошибка при заходе на "{url}" "{es}"')
            return False

    def __check_load_page(self, name_post):

        if len(name_post) > 15:
            name_post = name_post[:15]

        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "тзывы")]')))
            return True
        except Exception as es:
            # print(f'Ошибка при загрузке "{name_post}" поста "{es}"')
            return False

    def loop_load_page(self, post):
        coun = 0
        coun_ower = 10

        while True:
            coun += 1

            if coun >= coun_ower:
                print(f'Не смог зайти в пост {post["name"]}')
                return False

            response = self.load_page(post['link'])

            if not response:
                continue

            result_load = self.__check_load_page(post['name'])

            if not result_load:
                self.driver.refresh()
                return False

            return True

    def all_list_xarakt(self):
        try:
            xarakt_list = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@class, 'detail-navigates')]"
                                                                       f"//dl[contains(@class, 'characteristic')]")

        except Exception as es:
            print(f'Ошибка при получении all_list_xarakt "{es}"')

            return []

        return xarakt_list

    def format_har(self, gar_list):
        har_dict = {}
        for har in gar_list:
            try:
                har_row = har.text.split('\n')
            except:
                continue

            name_har = har_row[0]

            val_black_list = ['Производитель', 'Коллекция', 'Артикул', 'Размер', 'Страна', 'Тип', 'Помещение',
                              'Назначение']

            if name_har not in self.all_xarakt and name_har not in val_black_list:
                self.all_xarakt.append(name_har)

            try:
                har_dict[name_har] = ';'.join(x for x in har_row[1:])
            except:
                continue

        return har_dict

    def get_xarakt_list(self):

        all_list = self.all_list_xarakt()
        if all_list == []:
            return []

        good_dict = self.format_har(all_list)

        return good_dict

    def get_xarakt_list2(self, list_har):

        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'Характеристики')]").click()
        except Exception as es:
            print(f'Не смог переключить характеристики нижние 2 "{es}"')
            return []

        all_list = self.all_list_xarakt2()
        if all_list == []:
            return []

        good_dict = self.itter_xarakter2(all_list, list_har)

        return good_dict

    def get_price(self):
        try:
            price_post = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'offer__price')]").text

        except:
            return 0

        try:
            price = price_post.split()[0]
        except Exception as es:

            print(f'Ошибка при get_price "{es}"')

            return 0

        return price

    def get_edinicha(self):
        try:
            edinic_ = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'offer__price')]").text

        except:
            return 'м2'

        try:
            edinic = edinic_.split('/')[-1]
        except Exception as es:

            print(f'Ошибка при get_edinicha "{es}"')

            return 'м2'

        if 'комплект' in edinic:
            edinic = 'кмп'

        return edinic

    def _get_image_in_row(self, row):
        try:
            link_image = row.find_element(by=By.XPATH, value=f".//img").get_attribute('src')
        except Exception as es:
            print(f'Ошибка при получении _get_image_in_row "{es}"')

            return ''

        return link_image

    def get_name_full(self):
        try:
            name_post = self.driver.find_element(by=By.XPATH, value=f"//h1").text
        except:
            name_post = ''

        return name_post

    def get_one_image(self):
        try:
            _image = self.driver.find_element(by=By.XPATH, value=f"//*[@class='cart__images']"
                                                                 f"//*[contains(@class, 'slick-active')]") \
                .get_attribute('href')
        except Exception as es:
            print(f'Ошибка при получении галерии get_one_image "{es}"')

            return []

        return [_image]

    def _get_image_gallery_list(self):
        try:
            photo_rows = self.driver.find_elements(by=By.XPATH,
                                                   value=f"(//*[contains(@class, 'product')])"
                                                         f"//*[contains(@class, 'slider__node')]//picture/img")
        except Exception as es:
            print(f'Ошибка при получении фото "{es}"')
            return []

        try:
            photo_list = [x.get_attribute('src') for x in photo_rows]
        except Exception as es:
            print(f'Ошибка при формирования ссылок на фото "{es}"')
            return []

        return photo_list

    def get_photo(self):
        rows_List = self._get_image_gallery_list()

        if rows_List == []:
            rows_List = self.get_one_image()
            return rows_List

        return rows_List

    def start_pars(self):

        self.links_post = []

        good_over_count = 0

        count_db_tovar = self.BotDB.get_all_count()

        # for id_pk_ in range(10):
        # for id_pk_ in range(265, 283):
        for id_pk_ in range(count_db_tovar):

            sql_tovar = self.BotDB.get_tovar(id_pk_ + 1)
            try:
                id_pk, url, name, _, artikle, collection, prozvoditel, _ = sql_tovar
            except:
                continue

            if not sql_tovar:
                continue

            post = {}
            post['name'] = name
            post['id_pk'] = id_pk
            post['link'] = url
            post['artikle'] = artikle
            post['collection'] = collection
            post['prozvoditel'] = prozvoditel

            result_load_page = self.loop_load_page(post)

            if not result_load_page:
                continue

            post['xarakt'] = self.get_xarakt_list()

            post['price'] = self.get_price()

            post['edinicha'] = self.get_edinicha()

            post['full_name'] = self.get_name_full()

            image_list = self.get_photo()

            try:
                image_list = ' '.join(x for x in image_list)
            except:
                image_list = ''

            post['image'] = image_list


            self.links_post.append(post)

            if id_pk_ % 5 == 0 and id_pk_ != 0:
                print(f'Обработал {id_pk_} товаров')

            if id_pk_ % 30 == 0 and id_pk_ != 0:
                file_name = f'tovar_{id_pk_} {datetime.now().strftime("%H_%M_%S")}'

                save_dict = {}
                save_dict['name_colums'] = self.all_xarakt
                save_dict['result'] = self.links_post

                SaveResultTovar(save_dict).save_file(file_name)
                print(f'Сохранил {id_pk_} PLU')

            # print()

        print(f'Итог: собрал информацию с {len(self.links_post)} товаров')

        result_dict = {}
        result_dict['name_colums'] = self.all_xarakt
        result_dict['result'] = self.links_post

        return result_dict
