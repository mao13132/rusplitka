from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import getpass


class CreatBrowser:
    """Класс создаёт браузер с настройками.
    Параметр create_head принимает или True или False обозначает что будет ли появляться браузер
    """

    def __init__(self, name_profile, header):
        self.windowsUser = getpass.getuser()

        options = webdriver.ChromeOptions()

        self.display_x = 1920
        self.display_y = 1080

        options.add_argument(f'window-size={self.display_x},{self.display_y}')

        prefs = {"enable_do_not_track": True}
        options.add_experimental_option("prefs", prefs)

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-infobars")

        path_dir = (f'C:\\Users\\{self.windowsUser}\\AppData\\Local\\Google\\Chrome\\User Data\\{name_profile}')
        options.add_argument(f"user-data-dir={path_dir}")  # Path to your chrome profile

        options.add_argument("--ignore-certificate-errors")
        options.add_argument("no-sandbox")

        options.add_argument(
            "--disable-application-cache")

        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")

        options.add_argument("--headless")

        options.add_argument("--log-level=3")

        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        tz_params = {'timezoneId': 'Asia/Almaty'}

        s = Service(executable_path=r"chromedriver.exe")
        try:
            self.driver = webdriver.Chrome(service=s, options=options)
        except Exception as es:
            print(f'fОшибка при создании браузера "{es}"')
            return False

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                  '''
        })

        self.driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)
