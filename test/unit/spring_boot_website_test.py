import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from os import path
import time
import zipfile
import shutil
import xml.etree.ElementTree as ET


test_url = "https://start.spring.io/"
download_dir = '/home/student/Downloads/selenium/'
artifact_name = 'my_kotlin'
download_file = download_dir + artifact_name + '.zip'
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_dir,
})


class SpringBootWebTestCase(unittest.TestCase):
    def setUp(self):
        if path.exists(download_file):
            os.remove(download_file)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)
        self.driver.get(test_url)


    def tearDown(self):
        self.driver.quit()

    def test_should_open_website(self):
        """
        Open website and verify that it is load successfully.
        :return:
        """
        search_str = "//*[text()='Generate']"
        els = self.driver.find_elements_by_xpath(search_str)
        self.assertGreater(len(els), 0, 'Page loads failed!')

    def test_should_choose_maven(self):
        """
        Verify can select Maven option
        :return:
        """
        search_str = "//*[text()='Maven Project']"
        els = self.driver.find_elements_by_xpath(search_str)
        self.assertGreater(len(els), 0, 'Maven project is not found!')
        els[0].click()

    def test_should_choose_kotlin(self):
        search_str = "//*[text()='Kotlin']"
        els = self.driver.find_elements_by_xpath(search_str)
        self.assertGreater(len(els), 0, 'Kotlin is not found!')
        els[0].click()

    def test_should_choose_spring_boot_version(self):
        search_str = "//*[text()='2.2.8']"
        els = self.driver.find_elements_by_xpath(search_str)
        self.assertGreater(len(els), 0, 'spring-boot version is not found!')
        els[0].click()

    def test_should_enter_group_name(self):
        search_str = 'input-group'
        els = self.driver.find_elements_by_id(search_str)
        self.assertGreater(len(els), 0, 'input-group is not found!')
        els[0].clear()
        els[0].send_keys('com.drkiettran')

    def test_should_enter_artifact_name(self):
        search_str = 'input-artifact'
        els = self.driver.find_elements_by_id(search_str)
        self.assertGreater(len(els), 0, 'input-artifact is not found!')
        els[0].clear()
        els[0].send_keys(artifact_name)

    def test_should_choose_packaging_type(self):
        search_str = "//*[text()='War']"
        els = self.driver.find_elements_by_xpath(search_str)
        self.assertGreater(len(els), 0, 'Packaging type War is not found!')
        els[0].click()

    def test_should_choose_jdk_version(self):
        search_str = "//*[text()='11']"
        els = self.driver.find_elements_by_xpath(search_str)
        self.assertGreater(len(els), 0, 'JDK version 11 is not found!')
        els[0].click()

    def test_should_select_generate_button(self):
        search_str = "//*[text()='Generate']"
        els = self.driver.find_elements_by_xpath(search_str)
        self.assertGreater(len(els), 0, 'Generate button is not found!')
        els[0].click()

    def test_should_receive_a_zip_file(self):
        self.test_should_choose_maven()
        self.test_should_choose_kotlin()
        self.test_should_choose_spring_boot_version()
        self.test_should_enter_group_name()
        self.test_should_enter_artifact_name()
        self.test_should_choose_packaging_type()
        self.test_should_choose_jdk_version()
        self.test_should_select_generate_button()
        self.assertTrue(self.wait_for_zip_file(), 'zip file not found!')

    def test_should_download_correct_spring_boot_project(self):
        self.test_should_receive_a_zip_file()
        
    def it_takes_too_long(self, count):
        return count > 5

    def wait_for_zip_file(self):
        count = 0
        while True:
            time.sleep(1)
            count += 1
            if path.exists(download_file) or self.it_takes_too_long(count):
                break

        self.assertTrue(path.exists(download_dir))
        return True

    def process_zip_file(self):
        tmp_dir = '/tmp/'
        extracted_dir = tmp_dir + artifact_name + '/'

        if path.exists(extracted_dir):
            shutil.rmtree(extracted_dir)

        with zipfile.ZipFile(download_file, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)

if __name__ == '__main__':
    unittest.main()
