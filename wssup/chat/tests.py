from django.conf import settings

from channels.testing import ChannelsLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait


class ChatTests(ChannelsLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        try:
            # requires "chromedriver" to be installed in $PATH
            cls.driver = webdriver.Chrome(settings.CHROMEDRIVER_PATH)
        except:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    # ---- TESTS ----
    def test_posted_message_seen_by_all_room_members(self):

        try:
            self._enter_room('test1')

            self._open_new_window(0)
            self._enter_room('test1')

            self._switch_to_window(0)

            self._post_msg('hiya')

            WebDriverWait(self.driver, 2).until(
                lambda _ : 'hiya' in self._chat_log_val, 'Message not received by window1 from window1`'
            )

            self.switch_to_window(1)
            WebDriverWait(self.driver, 2).until(
                lambda _ : 'hiya' in self._chat_log_val, 'Message not received by window2 from window1'
            )

        finally:
            self._close_all_new_windows()


    # ---- HELPERS ----
    def _enter_room(self, name):

        self.driver.get(self.live_server_url + '/chat/')

        ActionChains(self.driver).send_keys(name + '\n').perform()

        WebDriverWait(self.driver, 2).until(
            lambda _ : name in self.driver.current_url
        )

    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self.driver.switch_to_window(self.driver.window_handles[-1])

    def _close_all_new_windows(self):

        while len(self.driver.window_handles) > 1:
            self.driver.switch_to_window(self.driver.window_handles[-1])
            self.driver.execute_script('window.close();')

        if len(self.driver.window_handles) == 1:
            self.driver.switch_to_window(self.driver.window_handles[0])

    def _switch_to_window(self, window_index):
        self.driver.switch_to_window(self.driver.window_handles[window_index])

    def _post_msg(self, msg):
        ActionChains(self.driver).send_keys(msg + '\n').perform()

    @property
    def _chat_log_val(self):
        return self.driver.find_element_by_css_selector('#chat-log').get_property('value')
