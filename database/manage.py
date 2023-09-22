import redis
import mysql.connector
import requests
import datetime
from addons.config import config

config = config()


# ! USED TO UPDATE WEB APPLICATION DATA. DEPRECATED
class UpdateWebApp:
    def __init__(self):
        self.WEB_URL = "http://192.168.0.118:5500/api/receive/data"
        self.auth = "auth1234"

    def update(self, type: str, data: dict):
        """
        Updates the API with the provided type and data.

        Parameters:
            type (str): The type of data being updated.
            data (dict): The data to be updated.

        Returns:
            None
        """
        try:
            r = requests.post(
                self.WEB_URL,
                json={"type": type, "data": data},
                headers={"Authorization": self.auth},
            )
            print("Completed request => ", r.json())
        except Exception as e:
            print("Could not finish request due to", e)
        return None
        pass


class Database:
    def __init__(self):
        self.conn = None
        self.host = config["database"]["host"]
        self.user = config["database"]["user"]
        self.password = config["database"]["pass"]
        self.database = config["database"]["database"]
        self.port = config["database"]["port"]
        self.webapp = UpdateWebApp()

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
        self.conn.autocommit = True
        self.conn.cursor().execute("USE users")

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def check_user_existence(self, user_id):
        self.connect()
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        exists = bool(result)
        cursor.close()
        self.disconnect()
        return exists

    def execute_query(self, query, *args):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, args)
        cursor.close()
        self.disconnect()
        print(query)

        try:
            if " balance " in query.lower():
                user_id = args[1]
                print(user_id)
                if user_id:
                    self.webapp.update("balance", {"user_id": str(user_id)})

            if "last_claim_time" in query.lower():
                user_id = args[1]
                print(user_id)
                if user_id:
                    self.webapp.update("last_claim_time", {"user_id": str(user_id)})

            if "warnings" in query.lower():
                user_id = args[0]
                print(user_id)
                if user_id:
                    self.webapp.update("warnings", {"user_id": (str(user_id))})
        except:
            pass

    def execute_read_query(self, query, *args):
        self.connect()
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(query, args)
        rows = cursor.fetchall()
        cursor.close()
        self.disconnect()
        return rows

    def create_user(self, user_id):
        query = "INSERT INTO users (user_id) VALUES (%s)"
        self.execute_query(query, user_id)
        return True

    def get_user_balance(self, user_id):
        query = "SELECT balance FROM users WHERE user_id = %s"
        result = self.execute_read_query(query, user_id)
        if result:
            return result[0]["balance"]
        return 0

    def update_user_balance(self, user_id, amount):
        timestamp = datetime.datetime.now().timestamp()
        insert_query = "INSERT INTO user_balance_history (user_id, balance, timestamp) VALUES (%s, %s, %s)"
        query = "UPDATE users SET balance = %s WHERE user_id = %s"
        self.execute_query(insert_query, user_id, amount, timestamp)
        self.execute_query(query, amount, user_id)

    def increment_user_balance(self, user_id, amount):
        timestamp = datetime.datetime.now().timestamp()
        insert_query = "INSERT INTO user_balance_history (user_id, balance, timestamp) VALUES (%s, %s, %s)"
        query = "UPDATE users SET balance = balance + %s WHERE user_id = %s"
        self.execute_query(insert_query, user_id, amount, timestamp)
        self.execute_query(query, amount, user_id)

    def ban_user(self, user_id):
        query = "UPDATE users SET banned = 1 WHERE user_id = %s"
        self.execute_query(query, user_id)

    def unban_user(self, user_id):
        query = "UPDATE users SET banned = 0 WHERE user_id = %s"
        self.execute_query(query, user_id)

    def get_user_warning(self, user_id):
        query = "SELECT warnings FROM users WHERE user_id = %s"
        result = self.execute_read_query(query, user_id)
        if result:
            return result[0]["warnings"]
        return 0

    def increment_user_warning(self, user_id):
        query = "UPDATE users SET warnings = warnings + 1 WHERE user_id = %s"
        self.execute_query(query, user_id)

    def reset_user_warning(self, user_id):
        query = "UPDATE users SET warnings = 0 WHERE user_id = %s"
        self.execute_query(query, user_id)

    def transfer_balance(self, user_id1, user_id2, amount):
        user1_balance = self.get_user_balance(user_id1)
        user2_balance = self.get_user_balance(user_id2)

        if user1_balance < amount:
            return False

        new_user1_balance = user1_balance - amount
        new_user2_balance = user2_balance + amount

        self.update_user_balance(user_id1, new_user1_balance)
        self.update_user_balance(user_id2, new_user2_balance)
        return new_user1_balance, new_user2_balance

    def get_last_claim_time(self, user_id):
        query = "SELECT last_claim_time FROM users WHERE user_id = %s"
        result = self.execute_read_query(query, user_id)
        if result:
            return result[0]["last_claim_time"]
        return 0

    def update_last_claim_time(self, user_id, last_claim_time):
        query = "UPDATE users SET last_claim_time = %s WHERE user_id = %s"
        self.execute_query(query, last_claim_time, user_id)
        return True

    def get_top_balance_holders_all(self, limit=10):
        query = "SELECT user_id, balance FROM users ORDER BY balance DESC LIMIT %s"
        result = self.execute_read_query(query, limit)
        return result

    def get_user_balances(self, user_ids: list, limit=10):
        balance_holders = []
        query = "SELECT user_id, balance FROM users WHERE user_id IN ({}) ORDER BY balance DESC LIMIT %s".format(
            ",".join("%s" for _ in user_ids)
        )
        result = self.execute_read_query(query, *user_ids, limit)
        for row in result:
            if row["user_id"] is not None and row["balance"] is not None:
                balance_holders.append((row["user_id"], row["balance"]))
        return balance_holders


class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=config["redis"]["host"],
            port=config["redis"]["port"],
            password=config["redis"]["pass"],
        )

    def set_data(self, key, value, expiration=None):
        self.redis_client.set(key, value)
        if expiration is not None:
            self.redis_client.expire(key, expiration)

    def get_data(self, key):
        return self.redis_client.get(key)

    def delete_data(self, key):
        self.redis_client.delete(key)

    def pipeline(self):
        return self.redis_client.pipeline()

    def transfer_balance(self, user_id1, user_id2, balance1, balance2, expiration):
        self.set_data(f"user_balance:{user_id1}", str(balance1), expiration)
        self.set_data(f"user_balance:{user_id2}", str(balance2), expiration)

    def increment_balance(self, key, amount):
        self.redis_client.incrby(key, amount)

    def sadd(self, key, value):
        self.redis_client.sadd(key, value)

    def smembers(self, key):
        return self.redis_client.smembers(key)

    def expire(self, key, expiration):
        self.redis_client.expire(key, expiration)
