#! python3
# coding: UTF-8

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from app import database_manager


PORTAL_URL = "https://portal.nap.gsic.titech.ac.jp/GetAccess/Login?Template=userpass_key&AUTHMETHOD=UserPassword"



def start_browse(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')
    options.add_experimental_option("detach", True)
    s = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=s, options=options)
    browser.get(url)
    return browser


def for_login(browser):
    stored_portal_password = database_manager.get_stored_portal_password()

    ele_account1 = browser.find_element_by_css_selector(
        "body > center:nth-child(5) > form > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > div > div > input"
    )
    ele_account1.send_keys(stored_portal_password["student_number"])

    ele_password1 = browser.find_element_by_css_selector(
        "body > center:nth-child(5) > form > table > tbody > tr > td > table > tbody > tr:nth-child(3) > td > div > div > input"
    )
    ele_password1.send_keys(stored_portal_password["portal_password"])

    ele_botton1 = browser.find_element_by_css_selector(
        "body > center:nth-child(5) > form > table > tbody > tr > td > table > tbody > tr:nth-child(5) > td > input[type=submit]:nth-child(1)"
    )
    ele_botton1.click()

    return


def login_portal():
    browser = start_browse(PORTAL_URL)

    # login1
    for_login(browser)

    # login2

    for i in range(4, 7):
        element = browser.find_element_by_xpath(
            f"//*[@id='authentication']/tbody/tr[{i}]/th[1]"
        )

        l = element.text
        char = l[1]
        ind = int(l[3]) - 1
        stored_matrix = database_manager.get_stored_matrix()

        try:
            matrix_element = stored_matrix[char][2*ind]
        except IndexError:
            browser.close()
            return

        element_input = browser.find_element_by_xpath(
            f"//*[@id='authentication']/tbody/tr[{i}]/td/div/div/input"
        )
        element_input.send_keys(matrix_element)

        element_button = browser.find_element_by_xpath(
            "//*[@id='authentication']/tbody/tr[8]/td/input[1]"
        )

    element_button.click()

    # for i, j in enumerate([4, 6, 8]):
    #     i += 3
    #     alphabet = ele_matrix[j].text[1]
    #     number = int(ele_matrix[j].text[3]) - 1
    #     code = MATRIX_CODE[alphabet][number]
    #
    #     ele_password2 = browser.find_element(By.NAME, f'message{i}')
    #     ele_password2.send_keys(code)
    #
    # ele_botton2 = browser.find_element(By.NAME, 'OK')
    # ele_botton2.click()
    #
    # if page_to_open != 'リソースメニュー':
    #     browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
    #     print(page_to_open)
    #     page_url = pages_in_portal[page_to_open]
    #     print(page_url)
    #     browser.get(page_url)

    return
