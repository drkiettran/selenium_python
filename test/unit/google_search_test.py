from selenium import webdriver
import unittest

_URL = 'https://google.com'
_SEARCH_STR = 'selenium webdriver'


class GoogleSearchTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.quit()

    def test_should_open_search_page(self):
        self.driver.get(_URL)
        q = self.driver.find_elements_by_name('q')
        self.assertTrue(q)

    def test_should_search_successfully(self):
        self.driver.get(_URL)
        q = self.driver.find_elements_by_name('q')
        search_buttons = self.driver.find_elements_by_xpath('//input[@name="btnK"]')
        print(len(search_buttons))
        q[0].clear()
        q[0].send_keys(_SEARCH_STR)
        search_buttons[0].click()
        results = self.driver.find_elements_by_xpath("//h3[contains(text(),'selenium') and contains(text(),'driver')]")
        self.assertTrue(results)


if __name__ == '__main__':
    unittest.main()
