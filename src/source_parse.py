import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime


class SourceParse:
    def __init__(self, driver, count_page):
        self.driver = driver
        self.source_name = 'profiplitka'
        self.links_post = []
        self.count_page = count_page

    def load_page(self, url):
        try:
            self.driver.get(url)
            return True
        except Exception as es:
            print(f'Ошибка при заходе на стартовую страницу "{es}"')
            return False

    def __check_load_page(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='collections']")))
            return True
        except:
            return False

    def loop_load_page(self):
        count = 0
        count_ower = 5

        while True:

            count += 1

            if count >= count_ower:
                print(f'Не смог открыть {self.source_name}')
                return False

            start_page = self.load_page(self.url)

            if not start_page:
                continue

            check_page = self.__check_load_page()

            if not check_page:
                self.driver.refresh()
                continue

            print(f'Успешно зашёл на {self.source_name}')

            return True

    def get_all_post(self):
        try:
            rows_post = self.driver.find_elements(by=By.XPATH,
                                                  value=f"//*[@class='favorites__grid']"
                                                        f"//*[contains(@class, 'compilation__item')]")


        except Exception as es:
            print(f'Ошибка при получение постов"{es}"')
            return False

        return rows_post

    def click_paginator(self):
        try:
            next_paginator = self.driver.find_elements(by=By.XPATH,
                                                       value=f"//*[contains(@class, 'page-n')]"
                                                             f"//a[contains(@class, 'active')]/following-sibling::a")


        except Exception as es:
            print(f'Ошибка при переключение страницы "{es}"')
            return False

        if next_paginator == []:
            return False

        try:
            next_paginator[0].click()
        except Exception as es:
            print(f'Ошибка при кликен на пагинатор "{es}"')
            return False

        return True

    def get_link(self, row):
        try:
            link_post = row.find_element(by=By.XPATH, value=f".//a[contains(@class, 'compilation__pic')]") \
                .get_attribute('href')
        except:
            link_post = ''

        return link_post

    def get_name(self, row):
        try:
            name_post = row.find_element(by=By.XPATH, value=f".//a[contains(@class, 'name')]").text
        except:
            name_post = ''

        return name_post

    def get_color(self, row):
        try:
            name_post = row.find_elements(by=By.XPATH, value=f".//a[contains(@class, 'name')]//parent::div//img")
        except:
            return ''

        color_list = [x.get_attribute('title') for x in name_post]

        return color_list

    def get_coutry(self, row):
        try:
            coutry = row.find_element(by=By.XPATH, value=f".//span[contains(text(), 'Страна')]//parent::div").text
        except:
            return ''

        try:
            coutry = coutry.replace('Страна: ', '')
        except:
            coutry = coutry

        return coutry

    def get_size(self, row):
        try:
            size = row.find_element(by=By.XPATH, value=f".//span[contains(text(), 'Размер')]//parent::div").text
        except:
            return ''

        try:
            size = size.replace('Размер: ', '')
            size = size.replace(' см', '').strip()
            size = size.replace(',', '')
        except:
            size = size

        try:
            size = size.split()
        except:
            size = size

        return size

    def get_type(self, row):
        try:
            type = row.find_element(by=By.XPATH, value=f".//span[contains(text(), 'Тип')]//parent::div").text
        except:
            return ''

        try:
            type = type.replace('Тип: ', '')
        except:
            type = type

        try:
            type = type.split(', ')
        except:
            type = type

        return type

    def get_price(self, row):
        try:
            price = row.find_element(by=By.XPATH, value=f".//span[contains(@class, 'price_real')]").text
        except:
            return ''

        try:
            price = price.replace(' руб./м2', '')
        except:
            price = price

        return price



    def itter_rows_post(self, rows_post):

        for row in rows_post:
            link = self.get_link(row)
            name = self.get_name(row)
            color = self.get_color(row)
            coutry = self.get_coutry(row)
            size = self.get_size(row)
            type_ = self.get_type(row)
            price = self.get_price(row)

            good_itter = {}

            good_itter['link'] = link
            good_itter['name'] = name
            good_itter['color'] = color
            good_itter['coutry'] = coutry
            good_itter['size'] = size
            good_itter['type'] = type_
            good_itter['price'] = price

            self.links_post.append(good_itter)

        return True

    def step_one_parse(self):

        _count_page = 0

        while True:

            rows_post = self.get_all_post()

            if rows_post == [] or rows_post is None:
                return False

            response = self.itter_rows_post(rows_post)

            _count_page += 1

            if _count_page >= self.count_page and self.count_page != 0:
                print(f'Сработал ограничитель в {self.count_page} страниц')
                return True
            print(f'Обработал {_count_page} страниц(у)')

            click_paginator = self.click_paginator()

            if not click_paginator:
                return True

            # time.sleep(0.5)

            # return True

    def start_pars(self):
        from src.temp_collect import temp_collect

        for url in temp_collect:

            self.url = url
            result_start_page = self.loop_load_page()

            if not result_start_page:
                continue

            response_one_step = self.step_one_parse()



        return self.links_post
