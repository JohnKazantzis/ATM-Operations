import sqlite3
import interface
import Pyro4

@Pyro4.expose
class AtmOperations:

    @staticmethod
    def createConnection():
        try:
            conn = sqlite3.connect("atm.db")
        except:
            print("There was an error connecting to the database")

        c = conn.cursor()

        return conn

    @staticmethod
    def createTables(conn):
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    name text NOT NULL,
                    deposits real NOT NULL
                    );""")

    @staticmethod
    def addUsers(conn):
        c = conn.cursor()

        c.execute("""INSERT INTO users (name, deposits) VALUES ('Giannis Kazantzis', 100)""")
        c.execute("""INSERT INTO users (name, deposits) VALUES ('Babis Makrinakis', 250.30)""")
        c.execute("""INSERT INTO users (name, deposits) VALUES ('Vaggelis Antonaros', 100000.32)""")

    @staticmethod
    def authentication(conn, name):
        details = []

        while not details:

            c = conn.cursor()
            c.execute("""SELECT * FROM users WHERE name='{}'""".format(name))
            details = c.fetchall()

            return details[0][0]

    @staticmethod
    def getBalance(name):
        conn = AtmOperations.createConnection()
        AtmOperations.createTables(conn)
        AtmOperations.addUsers(conn)

        # Authenticating the users
        id = AtmOperations.authentication(conn, name)

        c = conn.cursor()

        c.execute("""SELECT deposits FROM users WHERE id='{}'""".format(id))
        details = c.fetchall()

        conn.commit()

        return details[0][0]

    @staticmethod
    def deposit(name, depositMoney):
        conn = AtmOperations.createConnection()
        AtmOperations.createTables(conn)
        AtmOperations.addUsers(conn)

        # Authenticating the users
        id = AtmOperations.authentication(conn, name)

        c = conn.cursor()

        c.execute("""SELECT deposits FROM users WHERE id='{}'""".format(id))
        details = c.fetchall()
        balance = details[0][0]

        newBalance = balance + depositMoney

        c.execute("""Update users set deposits = {} where id = {}""".format(newBalance, id))

        c.execute("""SELECT deposits FROM users WHERE id='{}'""".format(id))
        details = c.fetchall()
        newbalance = details[0][0]

        conn.commit()

        return newbalance

    @staticmethod
    def withdraw(name, withdrawMoney):
        conn = AtmOperations.createConnection()
        AtmOperations.createTables(conn)
        AtmOperations.addUsers(conn)

        # Authenticating the users
        id = AtmOperations.authentication(conn, name)

        c = conn.cursor()
        
        c.execute("""SELECT deposits FROM users WHERE id='{}'""".format(id))
        details = c.fetchall()
        balance = details[0][0]

        newBalance = balance - withdrawMoney

        c.execute("""Update users set deposits = {} where id = {}""".format(newBalance, id))

        conn.commit()

        return newBalance

def main():

    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()

    uri = daemon.register(AtmOperations)
    print(uri)
    ns.register("atmOperations",uri)

    print("Ready...")
    daemon.requestLoop()


if __name__ == '__main__':
    main()
