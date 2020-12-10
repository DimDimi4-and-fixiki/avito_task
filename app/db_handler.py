import sqlite3
from .models import AvitoPair


class DataBaseHandler(object):
    def __init__(self, **kwargs):
        self.file_path: str = kwargs.get("path")
        self.connection = None
        try:
            self.create_connection()
        except Exception:
            print("Connection error :(")
        self.add_tables()

    def add_tables(self):
        query1 = "CREATE TABLE \"Pairs\" ( " \
                "\"id\"	INTEGER NOT NULL UNIQUE, " \
                "\"phrase\"	TEXT NOT NULL, " \
                "\"region\"	INTEGER NOT NULL, " \
                "PRIMARY KEY(\"id\" AUTOINCREMENT))"

        self.make_create_query(query=query1)

        query2 = "CREATE TABLE \"TimeStamps\" ( " \
                 "\"id\" INTEGER NOT NULL UNIQUE, " \
                 "\"counter\" TEXT NOT NULL, " \
                 "\"pair_id\" INTEGER NOT NULL, " \
                 "\"timestamp\"	TEXT NOT NULL,  " \
                 "PRIMARY KEY(\"id\" AUTOINCREMENT))"

        self.make_create_query(query=query2)

        query3 = "CREATE TABLE \"TopPosts\" ( " \
                 "\"id\" INTEGER NOT NULL UNIQUE, " \
                 "\"pair_id\" INTEGER NOT NULL UNIQUE, " \
                 "\"links\"	TEXT NOT NULL,  " \
                 "PRIMARY KEY(\"id\" AUTOINCREMENT))"

        self.make_create_query(query=query3)







    def create_connection(self):
        """
        Creates connection to the database
        :return:
        """
        try:
            #  tries to set a connection to the database
            self.connection = sqlite3.connect(self.file_path)
        except Exception as e:
            #  throws an Exception
            print(e)

    def make_select_query(self, query: str) -> list:
        """
        makes a SELECT query to the database and returns rows
        :param query:  query text
        :return: rows
        """

        self.create_connection()  # sets connection
        cursor = self.connection.cursor()  # cursor to execute the query
        cursor.execute(query)
        rows = cursor.fetchall()  # result of the query
        return rows

    def make_insert_query(self, query: str):
        """
        makes an INSERT query to the database
        commits changes to the database
        :param query: query text
        """

        self.create_connection()  # sets connection
        cursor = self.connection.cursor()  # cursor to perform the query
        res = cursor.execute(query)  # result of the query
        self.connection.commit()  # commits changes

    def make_update_query(self, query: str):
        """
        makes an UPDATE query to the database
        commits changes to the database
        :param query: query text
        """

        self.create_connection()  # sets connection
        cursor = self.connection.cursor()  # cursor to execute the query
        res = cursor.execute(query)  # result of the query
        self.connection.commit()  # commits changes

    def make_create_query(self, query: str):
        """
        makes an UPDATE query to the database
        commits changes to the database
        :param query: query text
        """

        self.create_connection()  # sets connection
        cursor = self.connection.cursor()  # cursor to execute the query
        res = cursor.execute(query)  # result of the query
        self.connection.commit()  # commits changes

    def check_pair(self, pair: AvitoPair) -> bool:
        """
        Checks if pair is already in the database
        return : res  True if no pair in the db and False if pair is in the db
        """
        dict_pair = pair.dict()
        phrase = str(dict_pair["phrase"])  # gets phrase from object
        region = str(dict_pair["region"])  # gets region from object

        query = "SELECT * FROM Pairs " \
                "WHERE phrase = \"{}\" " \
                "AND region = \"{}\"".format(phrase, region)
        res = self.make_select_query(query=query)  # result of the query
        return res == []  # checks the result

    def get_pair_id(self, pair: AvitoPair):
        """
        Gets ID of the pair which is in the database
        :param pair:  pair of phrase and region
        :return:  id of the pair
        """
        dict_pair = pair.dict()  # pair packed in a dictionary
        phrase = str(dict_pair["phrase"])  # gets phrase from object
        region = str(dict_pair["region"])  # gets region from object

        # query the select the id
        query = "SELECT * FROM Pairs " \
                "WHERE phrase = \"{}\" " \
                "AND region = \"{}\"".format(phrase, region)
        res = self.make_select_query(query=query)  # result of the query
        return res[0][0]  # id of the pair

    def get_last_id(self) -> int:
        """
        Gets id of the last record in the database
        :return: id
        """
        query = "SELECT COUNT(*) FROM Pairs"  # query to make
        res = self.make_select_query(query=query)  # result of the query
        return res[0][0]  # last id

    def add_pair(self, pair: AvitoPair) -> int:
        """
        Adds new pair to the database
        Returns id of new pair
        Returns existing id of pair was in database before
        :param pair: pair of phrase and region
        :return: id
        """
        dict_pair = pair.dict()  # pair packed in a dictionary
        phrase = str(dict_pair["phrase"])  # gets phrase from object
        region = str(dict_pair["region"])  # gets region from object
        to_add = self.check_pair(pair=pair)  # flag if record should be added
        if to_add:  # need to add record
            query = "INSERT INTO Pairs (phrase, region) " \
                    "VALUES (\"{}\", \"{}\")".format(phrase, region)
            self.make_insert_query(query=query)  # inserts the pair
            return self.get_last_id()  # return a new pair's id
        else:
            return self.get_pair_id(pair=pair)  # returns existing id

    def get_pair(self, pair_id: str) -> dict:
        """
        Gets pair by its id
        :param pair_id: id of the pair in the database
        :return: dictionary with phrase and region
        """

        # query to get the data:
        query = "SELECT * FROM Pairs " \
                "WHERE id = {}".format(pair_id)
        res = self.make_select_query(query=query)  # result of the query
        return {
            "phrase": res[0][1],  # pair's phrase
            "region": res[0][2],  # pair's region
        }

    def add_timestamp(self, params: dict):
        """
        Adds (counter; timestamp) record to the database
        :param params: parameters to add, packed in the dictionary
        """
        pair_id = params["pair_id"]  # id of the pair
        counter = params["counter"]  # counter of number of posts
        timestamp = params["timestamp"]  # current timestamp

        # query which inserts data to the database
        query = "INSERT INTO TimeStamps (counter, pair_id, timestamp) " \
                "VALUES (\"{}\", {}, \"{}\")".format(counter, pair_id, timestamp)
        self.make_insert_query(query=query)  # performs the query

    def get_timestamps(self, pair_id: int) -> dict:
        """
        Returns counters and timestamps for a given id
        :param pair_id: id of a pair of phrase and region
        :return: dictionary of counters and timestamps
        """

        # query to select all timestamps for the id from the database:
        query = "SELECT counter, timestamp FROM TimeStamps " \
                "WHERE pair_id = {}".format(pair_id)

        # result of the query:
        res = self.make_select_query(query=query)

        dict_res = {}  # dictionary to return
        for element in res:
            dict_res[element[-1]] = element[0]  # fills dictionary with elements
        return dict_res

    def check_top_posts(self, pair_id) -> bool:
        """
        Checks if top posts for pair are added in the database
        :param pair_id:
        :returns: True if there is a record and False if there is no record in the database
        """
        #  query which selects a record with top posts:
        query = "SELECT * FROM TopPosts " \
                "WHERE pair_id = {}".format(pair_id)

        # result of the query:
        res = self.make_select_query(query=query)
        return not(res == [])

    def add_top_posts(self, **params):
        """
        Adds top posts' links for the pair_id to the database
        """
        pair_id = str(params.get("pair_id", None))  # id of the pair
        links = str(params.get("links", None))  # links to add
        is_added = self.check_top_posts(pair_id=pair_id)  # if id is already in the database
        if not is_added:  # if id is not in the database
            query = "INSERT INTO TopPosts (pair_id, links) " \
                    "VALUES ({}, \"{}\")".format(pair_id, links)
            self.make_insert_query(query=query)
        else:  # id is already in the database
            query = "UPDATE TopPosts SET pair_id = {}, links = \"{}\" " \
                    "WHERE pair_id = {}".format(pair_id, links, pair_id)
            self.make_update_query(query=query)

    def get_top_posts(self, pair_id: str) -> list:
        """
        Gets list of top posts links for the pair id
        :param pair_id:  id of the pair of phrase and region
        :return: list
        """

        #  query that selects top posts for a given pair_id:
        query = "SELECT links FROM TopPosts " \
                "WHERE pair_id = {}".format(pair_id)

        links = self.make_select_query(query=query)[0][0]  # string with links
        res = links.split(",")  # list with top 5 links
        return res





