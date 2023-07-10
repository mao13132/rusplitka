from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class GetPluInColl:
    def __init__(self, driver, collect, BotDB):
        self.driver = driver
        self.source_name = 'profiplitka'
        self.links_post = []
        self.collect = collect
        self.BotDB = BotDB


    def get_all_post(self):
        try:
            rows_post = self.driver.find_elements(by=By.XPATH,
                                                  value=f"//div[@id='charAll']"
                                                        f"//*[contains(@class, 'favorites__row')]/div")


        except Exception as es:
            print(f'Ошибка при получение постов"{es}"')
            return False

        return rows_post

    def get_link(self, row):
        try:
            link_post = row.find_element(by=By.XPATH, value=f".//a[contains(@class, 'link')]") \
                .get_attribute('href')
        except:
            link_post = ''

        return link_post

    def get_name(self, row):
        try:
            name_post = row.find_element(by=By.XPATH, value=f".//a[contains(@class, 'link')]").text
        except:
            name_post = ''

        return name_post


    def get_coutry(self, row):
        try:
            har_ = row.find_element(by=By.XPATH, value=f".//p[contains(@class, 'info')]").text
        except:
            return '', ''

        try:
            coutry = har_.split()[-1]
        except:
            coutry = ''
            print(f'Нулевой страна coutry')
        _artikl = har_.split('\n')


        try:
            artikl = _artikl[0].split(':')[1].strip()
        except:
            artikl = ''
            print(f'Нулевой артикул get_plu_in_coll')




        return coutry, artikl

    def get_proiz(self, row):
        try:
            har_ = row.find_element(by=By.XPATH, value=f".//p[contains(@class, 'info')]").text
        except:
            return ''

        try:
            pro_ = har_.split('\n')[-1]
        except:
            pro_ = ''
        try:
            pro = pro_.split(' -')[0]
        except:
            pro = ''




        return pro




    def itter_rows_post(self, rows_post):

        for count, row in enumerate(rows_post):
            status = True

            link = self.get_link(row)
            name = self.get_name(row)
            coutry, artikl = self.get_coutry(row)
            proiz = self.get_proiz(row)

            good_itter = {}

            good_itter['link'] = link
            good_itter['name'] = name
            good_itter['coutry'] = coutry
            good_itter['artikl'] = artikl
            good_itter['proiz'] = proiz
            good_itter['collection'] = self.collect

            chech_double = self.BotDB.exist_plu(artikl, proiz)

            if chech_double != []:
                status = False
                print(f'Найден дубль')
                res_update = self.BotDB.update_double(artikl, self.collect, proiz)


            if status:
                self.BotDB.add_plu(link, name, artikl, self.collect, proiz)
                print(f'Добавил в базу данных "{name}"')

            if count % 5 == 0 and count != 0:
                print(f'Обработал {count} товаров в коллекции')

            self.links_post.append(good_itter)

        return True



    def start_plu_parse(self):
        rows_post = self.get_all_post()

        if rows_post == [] or rows_post is None:
            return False

        response = self.itter_rows_post(rows_post)

        return self.links_post

