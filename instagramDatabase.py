import psycopg2
import sys
import login_data


class DatabaseFunctionality(object):

    """
    Class initializing a database functionality to save the information
    retrieved in InstagramScraper.py
    """

    def __init__(self):
        self.user = login_data.DATABASE_USERNAME
        self.password = login_data.PASSWORD_DATABASE
        self.host = login_data.HOST
        self.port = login_data.PORT
        self.database = login_data.DATABASE
        self.connection = None
        self.cursor = None

    def connect(self):

        """
        Connects with the database with information saved in the login_data.py file,
        if it doesn't succeed, it will raise an exception
        """

        try:
            self.connection = psycopg2.connect(user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               port=self.port,
                                               database=self.database)
            self.cursor = self.connection.cursor()
            print('Database connected.')

        except Exception as exc:
            if str(exc)[:6] == 'FATAL:':
                sys.exit("Database connection error: %s" % str(exc)[8:])
            else:
                raise exc

    def close(self):
        """
        Closes the connection
        """

        if self.connection:
            self.connection.close()
        self.connection = None

    def commit(self):
        """
        Commits the changes
        """

        self.connection.commit()

    def rollback(self):
        """
        Rollsback the changes made with a query
        """

        self.connection.rollback()

    def execute_insert_post_details(self, url, post_type, likes, time_posted, caption, username):
        """
        Executes the insert query to the database with the information from function get_post_details
        from InstagramScraper.py

        :param url: str, the link to the post
        :param post_type: str, photo/video
        :param likes: int, number of likes
        :param time_posted: datetime object
        :param caption: str, caption under a the post
        :param username: str, username of the author of the post
        :return: cursor
        """

        self.query_insert_post_details = "INSERT INTO post_details (URL, POST_TYPE, LIKES, TIME_POSTED, " \
                                         "CAPTION, USER_NAME) VALUES (%s, %s, %s, %s, %s, %s);"

        try:
            self.record_to_insert = (url, post_type, likes, time_posted, caption, username)
            self.cursor.execute(self.query_insert_post_details, self.record_to_insert)
            self.commit()
            print("Commited.")
        except psycopg2.errors.DatabaseError as ex:
            self.rollback()
            self.cursor = self.connection.cursor()
            raise ex
        return self.cursor

    def execute_insert_comment_details(self, url_post, comment_author, contents, time_of_post):
        """
        Executes the insert query to the database with the information from function get_comments
        from InstagramScraper.py

        :param url_post: str, link to the post
        :param comment_author: str, name of the author of the comment
        :param contents: str, the comment
        :param time_of_post: datetime object, time of the posting the comment
        :return: cursor
        """

        self.query_insert_comment = "INSERT INTO post_comments (URL, COMMENT_AUTHOR, CONTENTS, TIME_POSTED, " \
                                    "USER_NAME_POST_AUTHOR) VALUES (%s, %s, %s, %s, %s);"

        try:
            self.record_to_insert_comment = (url_post, comment_author, contents, time_of_post)
            self.cursor.execute(self.query_insert_comment, self.record_to_insert_comment)
            self.commit()
            print('Committed.')
        except psycopg2.errors.DatabaseError as e:
            self.rollback()
            self.cursor = self.connection.cursor()
            raise e
        return self.cursor
