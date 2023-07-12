import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime

from save_result_tovar import SaveResultTovar


class SourceParse:
    def __init__(self, driver, count_page):
        self.driver = driver
        self.source_name = 'rusplitka'
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
                EC.presence_of_element_located((By.XPATH, "//*[@class='pagination']")))
            return True
        except:
            return False

    def loop_load_page(self, url):
        count = 0
        count_ower = 5

        while True:

            count += 1

            if count >= count_ower:
                print(f'Не смог открыть {self.source_name}')
                return False

            start_page = self.load_page(url)

            if not start_page:
                continue

            check_page = self.__check_load_page()

            if not check_page:
                self.driver.refresh()
                continue

            print(f'Успешно зашёл на {self.source_name}')

            return True

    def get_all_post(self):
        count = 0
        while True:
            count += 1
            if count > 5:
                print(f'Не сомг включить коллекцию')
                return False


            try:
                rows_post = self.driver.find_elements(by=By.XPATH,
                                                      value=f"//*[@id='container_elements_catalog']"
                                                            f"//*[@itemscope='product']")



            except Exception as es:
                print(f'Ошибка при получение постов"{es}"')
                continue

            if rows_post == []:
                try:
                    self.driver.find_element(by=By.XPATH,
                                             value=f"//*[contains(@class, 'catalog_type')]//*[contains(text(), 'оллекции')]").click()
                    continue
                except:
                    continue


            return rows_post



    def click_paginator(self):
        try:
            next_paginator = self.driver.find_elements(by=By.XPATH,
                                                       value=f"//*[contains(@class, 'pagination')]"
                                                             f"//*[contains(@class, 'active')]/following-sibling::a")


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
            link_post = row.find_element(by=By.XPATH, value=f".//a[contains(@class, 'name')]") \
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
            color_ = row.find_elements(by=By.XPATH, value=f".//*[contains(@class, 'colors')]"
                                                          f"//span[contains(@class, 'colors')]")
        except:
            return ''

        color_list = [x.get_attribute('title') for x in color_]

        return color_list

    def get_coutry(self, row):
        try:
            coutry = row.find_element(by=By.XPATH, value=f".//*[contains(@class, 'country')]"
                                                         f"//*[contains(@class, 'country-img')]").text
        except:
            return ''

        return coutry

    def get_proiz(self, row):
        try:
            proiz = row.find_element(by=By.XPATH, value=f".//*[contains(@class, 'country')]").text
        except:
            return ''

        try:
            proiz = proiz.split('\n')[0]
        except:
            proiz = proiz

        return proiz

    def get_size(self, row):
        try:
            size = row.find_elements(by=By.XPATH, value=f".//*[contains(@class, 'size')]/span")
        except:
            return []

        try:
            size_list = [x.text for x in size]
        except:
            size_list = []

        return size_list

    def get_price(self, row):
        try:
            price = row.find_element(by=By.XPATH, value=f".//*[contains(@class, 'price')]").text
        except:
            return ''

        try:
            price = price.split()[1]
        except:
            price = price

        return price

    def itter_rows_post(self, rows_post):
        for row in rows_post:

            link = self.get_link(row)
            name = self.get_name(row)
            color = self.get_color(row)
            coutry = self.get_coutry(row)
            proiz = self.get_proiz(row)
            size = self.get_size(row)
            price = self.get_price(row)

            good_itter = {}

            good_itter['link'] = link
            good_itter['name'] = name
            good_itter['color'] = color
            good_itter['coutry'] = coutry
            good_itter['proiz'] = proiz
            good_itter['size'] = size
            good_itter['price'] = price

            self.links_post.append(good_itter)

            count_good = len(self.links_post)

            if count_good % 5 == 0 and count_good != 0:
                print(f'! Собрал {count_good} коллекций')

        print(f'Всего собрал {len(self.links_post)} коллекций')

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

    def start_pars(self, url):

        result_start_page = self.loop_load_page(url)

        if not result_start_page:
            return False

        response_one_step = self.step_one_parse()
        # TODO написать сохранение в json
        return self.links_post
