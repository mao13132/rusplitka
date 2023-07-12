import time
from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GetBrands:
    def __init__(self, driver):
        self.driver = driver
        self.links_post = []
        self.source_name = 'rusplitka'

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

    def get_all_rows_brand(self):
        try:
            get_rows = self.driver.find_elements(by=By.XPATH,
                                                 value=f"//*[contains(@class, 'manufacturer__alphabet')]"
                                                       f"//*[contains(@class, 'title')]//a")



        except Exception as es:
            print(f'Ошибка при get_all_rows_brand"{es}"')
            return []

        print(f'Получаю {len(get_rows)} бренда(ов)')

        try:
            brand_links_list = '\n'.join(x.get_attribute('href') for x in get_rows)
        except Exception as es:
            print(f'Ошибка при обработке списка брендов "{es}"')
            return []

        return brand_links_list





    def start_pars_brands(self):
        self.url = 'https://www.rusplitka.ru/catalog/'

        result_start_page = self.loop_load_page()

        if not result_start_page:
            return False

        links_brands = self.get_all_rows_brand()

        from save_result_tovar import SaveResultTovar
        res_save = SaveResultTovar.save_brands(links_brands)

        if res_save:
            print(f'Файл с брендами сохранил в brands.txt ')

            return True

        return False
