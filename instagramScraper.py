import time
import pickle
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import login_data
from instagramDatabase import DatabaseFunctionality


class InstagramComments(object):
    """
    Instagram scraper
    """

    def __init__(self):
        """
        Initializes the instance of the webdriver.
        Keeps all new opening links in one window.
        """
        self.firefox_options = Options()
        self.browser = Firefox(options=self.firefox_options)

    def login(self):
        """
        Login functionality
        Requires the log in information to be stored in the additional file: login_data
        """

        self.browser.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        print('Opening the page')
        time.sleep(8)
        self.usernameInput = self.browser.find_elements_by_css_selector('form input')[0]
        self.usernameInput.send_keys(login_data.USERNAME_INSTAGRAM)
        print('Input username')
        time.sleep(3)
        self.passwordInput = self.browser.find_elements_by_css_selector('form input')[1]
        self.passwordInput.send_keys(login_data.PASSWORD_INSTAGRAM)
        print('Input password')

        try:
            self.button_login = self.browser.find_element_by_class_name('button')
        except:
            self.button_login = self.browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button/div')

        time.sleep(4)

        self.button_login.click()
        print('Logged in')
        time.sleep(5)

        self.cookies = pickle.dump(self.browser.get_cookies(), open('cookies.pkl', 'wb'))

        try:
            self.notnow = self.browser.find_element_by_css_selector(
                'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
            self.notnow.click()
        except:
            pass

    def get_post_links(self, username, post_count):
        """
        Crawler to get a list of links to the posts starting from the chronologically most recent
        :param username: str, the username of the account
        :param post_count: int, amount of links desired to save
        :return: a list of links to the post of the specific user
        """

        self.post_links = []
        self.browser.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        self.cookies = pickle.load(open('cookies.pkl', 'rb'))
        for cookie in self.cookies:
            self.browser.add_cookie(cookie)
        self.username = username
        self.url = 'https://www.instagram.com/' + username + '/'
        self.browser.get(self.url)
        time.sleep(10)
        self.post = 'https://www.instagram.com/p/'
        while len(self.post_links) < post_count:
            self.links = [a.get_attribute('href')
                          for a in self.browser.find_elements_by_tag_name('a')]
            for link in self.links:
                if self.post in link and link not in self.post_links:
                    self.post_links.append(link)
            self.scroll_down = 'window.scrollTo(0, document.body.scrollHeight);'
            self.browser.execute_script(self.scroll_down)
            time.sleep(10)
        else:
            print(self.post_links)
            print(len(self.post_links))
            return self.post_links[:post_count]

    def get_post_details(self, url):
        """
        Saves the information about the instagram post: number of likes,
        type of the post (photo or video), caption, timestamp with timezone
        of when it was posted, username of the author
        :param url: str, link to the post
        :return: all the elements and send them to the database functionality
        """

        self.browser.get(url)
        try:
            self.likes = self.browser.find_element_by_xpath(
                """//*[@id="react-root"]/section/main/div/div/
                    article/div[2]/section[2]/div/div/button/span""").text
            self.post_type = 'photo'
        except:
            self.likes = self.browser.find_element_by_xpath(
                """//*[@id="react-root"]/section/main/div/div/
                    article/div[2]/section[2]/div/span""").text.split()[0]
            self.post_type = 'video'
        self.time_posted = self.browser.find_element_by_xpath('//a/time').get_attribute("datetime")
        try:
            self.caption = self.browser.find_element_by_xpath(
                """/html/body/div[1]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span""").text
        except NoSuchElementException as e:
            self.caption = ""
        try:
            return DatabaseFunctionality.execute_insert_post_details(url, self.post_type, self.likes, self.time_posted,
                                                                     self.caption)
        except psycopg2.errors.DatabaseError:
            pass
        time.sleep(8)

    def get_comments(self, url):
        """
        Saves the comments of the post: username of the authour of the comment, comment itself,
        timestamp with timezone,
        :param url: link to the post
        :return:
        """

        self.browser.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        self.cookies = pickle.load(open('cookies.pkl', 'rb'))
        for cookie in self.cookies:
            self.browser.add_cookie(cookie)
        self.browser.get(url)
        time.sleep(5)

        try:
            self.load_more_comments = self.browser.find_element_by_class_name(
                'glyphsSpriteCircle_add__outline__24__grey_9 u-__7')
            self.action = ActionChains(self.browser)
            self.action.move_to_element(self.load_more_comments)
            self.load_more_comments.click()
            time.sleep(4)
            self.action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
        except Exception as e:
            pass

        time.sleep(5)
        comment = self.browser.find_elements_by_class_name('gElp9 ')
        for c in comment:
            container = c.find_element_by_class_name('C4VMK')
            name = container.find_element_by_class_name('_6lAjh').text
            content = container.find_element_by_tag_name('span').text
            content = content.replace('\n', ' ').strip().rstrip()
            time_of_post = self.browser.find_element_by_xpath('//a/time').get_attribute("datetime")
            comment_details = {'url_post': url, 'profile name': name, 'comment': content,
                               'time': time_of_post}
            print(comment_details)
            try:
                return DatabaseFunctionality.execute_insert_comment_details(url, name, content, time_of_post)
            except psycopg2.errors.DatabaseError as e:
                pass
