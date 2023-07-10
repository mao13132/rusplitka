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
                EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "{name_post[:-3]}")]')))
            return True
        except Exception as es:
            print(f'Ошибка при загрузке "{name_post}" поста "{es}"')
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

    def get_name_xarakter(self, xar):
        try:
            name_xar = xar.find_element(by=By.XPATH, value=f".//span[contains(@class, 'label')]").text
        except Exception as es:
            print(f'Ошибка при получении get_name_xarakter "{es}"')

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
            print(f'Ошибка при получении get_value_name_xarakter2 "{es}"')

            return '', ''
        try:
            name_xar = _xar[0].text.replace(':', '')
        except:
            name_xar = ''
        try:
            value_xar = _xar[1].text.strip()
        except:
            value_xar = ''

        return name_xar, value_xar

    def get_value_xarakter(self, xar):
        try:
            list_xar = xar.find_element(by=By.XPATH, value=f".//*[contains(@class, 'prop')]").text
        except Exception as es:
            print(f'Ошибка при получении get_value_xarakter "{es}"')

            return False

        return list_xar

    def itter_xarakter(self, all_list):

        good_list = {}

        for xar in all_list:
            # dict_one_xar = {}
            name_xar = self.get_name_xarakter(xar)
            value_xar = self.get_value_xarakter(xar)

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

            if name_xar == '' and value_xar == '':
                continue

            if name_xar == 'Назначение':
                value_xar = ';'.join(x.replace('-', '').strip() for x in value_xar.split('\n'))

            list_har[name_xar] = value_xar
            # good_list[name_xar] = value_xar

            if name_xar not in self.all_xarakt:
                self.all_xarakt.append(name_xar)

        return good_list

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
        try:
            xarakt_list = self.driver.find_elements(by=By.XPATH, value=f"//div[@id='charCharacters']//tr")

        except Exception as es:
            print(f'Ошибка при получении all_list_xarakt "{es}"')

            return []

        return xarakt_list

    def get_xarakt_list(self):

        all_list = self.all_list_xarakt()
        if all_list == []:
            return []

        good_dict = self.itter_xarakter(all_list)

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

    def get_text(self):

        try:
            text = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@itemprop, 'description')]").text
        except Exception as es:
            print(f'Ошибка при получении get_text "{es}"')

            return ''

        try:
            text = '\n'.join(x for x in text.split('\n')[:-1])
        except:
            text = text

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
            print(f'Ошибка при получении _get_image_in_row "{es}"')

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
                                                                 f"//*[contains(@class, 'slick-active')]")\
                .get_attribute('href')
        except Exception as es:
            print(f'Ошибка при получении галерии get_one_image "{es}"')

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



    def start_pars(self):

        self.links_post = []

        good_over_count = 0

        count_db_tovar = self.BotDB.get_all_count()

        for id_pk_ in range(140, count_db_tovar):
        # for id_pk_ in range(count_db_tovar):

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

            post['text'] = self.get_text()

            self.get_xarakt_list2(post['xarakt'])

            post['price'] = self.get_price()

            post['edinicha'] = self.get_edinicha()

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