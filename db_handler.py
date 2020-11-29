import sqlite3
from models import AvitoPair


class DataBaseHandler(object):
    def __init__(self, **kwargs):
        self.file_path: str = kwargs.get("path")
        self.connection = None
        try:
            self.create_connection()
        except Exception:
            print("Connection error :(")

    def create_connection(self):
        try:
            #  tries to set a connection to the database
            self.connection = sqlite3.connect(self.file_path)
        except Exception as e:
            #  throws an Exception
            print(e)

    def make_select_query(self, query: str):
        """
        makes a SELECT query to the database and returns rows
        :param query:  query text
        :return: rows
        """

        self.create_connection()  # sets connection
        print(query)
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
        print(query)
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
        print(query)
        cursor = self.connection.cursor()  # cursor to execute the query
        res = cursor.execute(query)  # result of the query
        self.connection.commit()  # commits changes

    def check_pair(self, pair: AvitoPair) -> bool:
        """
        Checks if pair is already in the database
        return : res  True if no pair in db and False if pair is in db
        """
        dict_pair = pair.dict()
        phrase = str(dict_pair["phrase"])  # gets phrase from object
        region = str(dict_pair["region"])  # gets region from object

        query = "SELECT * FROM Pairs " \
                "WHERE phrase = \"{}\" " \
                "AND region = \"{}\"".format(phrase, region)
        res = self.make_select_query(query=query)  # result of the query
        return res == []

    def get_pair_id(self, pair: AvitoPair):
        """
        Gets ID of the pair which is in the database
        :param pair:  pair of phrase and region
        :return:  id of the pair
        """
        dict_pair = pair.dict()
        phrase = str(dict_pair["phrase"])  # gets phrase from object
        region = str(dict_pair["region"])  # gets region from object

        query = "SELECT * FROM Pairs " \
                "WHERE phrase = \"{}\" " \
                "AND region = \"{}\"".format(phrase, region)
        res = self.make_select_query(query=query)  # result of the query
        return res[0][0]

    def get_last_id(self) -> int:
        """
        Gets id of the last record in the database
        :return: id
        """
        query = "SELECT COUNT(*) FROM Pairs"  # query to make
        res = self.make_select_query(query=query)  # result of the query
        return res[0][0]

    def add_pair(self, pair: AvitoPair) -> int:
        """
        Adds new pair to the database
        Returns id of new pair
        Returns existing id of pair was in database before
        :param pair: pair of phrase and region
        :return: id
        """
        dict_pair = pair.dict()
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
        # query to get the data
        query = "SELECT * FROM Pairs " \
                "WHERE id = {}".format(pair_id)
        res = self.make_select_query(query=query)  # result of the query
        return {
            "phrase": res[0][1],
            "region": res[0][2],
        }

    def add_timestamp(self, params: dict):
        """
        Adds counter and timestamp record to the database
        :param params: parameters to add
        """
        pair_id = params["pair_id"]
        counter = params["counter"]
        timestamp = params["timestamp"]
        query = "INSERT INTO TimeStamps (counter, pair_id, timestamp) " \
                "VALUES (\"{}\", {}, \"{}\")".format(counter, pair_id, timestamp)
        self.make_insert_query(query=query)

    def get_timestamps(self, pair_id: int):
        """
        Gets counters and timestamps for a given id
        :param pair_id: id of a pair of phrase and region
        :return: dictionary of counters and timestamps
        """
        query = "SELECT counter, timestamp FROM TimeStamps " \
                "WHERE pair_id = {}".format(pair_id)
        res = self.make_select_query(query=query)
        dict_res = {}  # dictionary to return
        for element in res:
            dict_res[element[-1]] = element[0]
        return dict_res




