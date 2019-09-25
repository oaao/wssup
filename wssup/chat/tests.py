from channels.testing import ChannelsLiveServerTestCase

from selenium import webdriver


class ChatTests(ChannelsLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        try:
            # requires "chromedriver" to be installed in $PATH
            cls.driver = webdriver.Chrome('./chromedriver')
        except:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()