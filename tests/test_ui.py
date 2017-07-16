import unittest
from selenium import webdriver
import time


class TestURLs(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def test_add_new_post(self):
        """Tests if the new post page saves a Post object to the database"""
        #
        # Log the user in
        #
        self.driver.get("http://127.0.0.1:5000/login")
        username_field = self.driver.find_element_by_name("username")
        username_field.send_keys("test")
        password_field = self.driver.find_element_by_name("password")
        password_field.send_keys("test")
        login_button = self.driver.find_element_by_name("login")
        login_button.click()
        #
        # Go to the new_post page
        #
        self.driver.get("http://127.0.0.1:5000/blog/new")
        #
        # Need to give the Javascript enough time to set up the iframe
        #
        time.sleep(1)
        #
        # Fill out the fields and submit the form
        #
        title_field = self.driver.find_element_by_name("title")
        title_field.send_keys("Test Title")
        self.driver.switch_to.frame(
            self.driver.find_element_by_tag_name("iframe")
        )
        post_field = self.driver.find_element_by_class_name(
            "cke_editable"
        )
        post_field.send_keys("Test content")
        self.driver.switch_to.parent_frame()
        post_button = self.driver.find_element_by_class_name(
            "btn-primary"
        )
        post_button.click()
        #
        # Go to the blog home page and verify that the post is there
        #
        self.driver.get("http://127.0.0.1:5000/blog")
        self.assertIn("Test Title", self.driver.page_source)
        self.assertIn("Test content", self.driver.page_source)
