import sqlite3
import os

class Operations:
    """ Class with functions to work with the database """

    def __init__(self):
        database_contents = ''
        self.conn = sqlite3.connect('app/sqlite/library.db', check_same_thread=False)
        self.c = self.conn.cursor()

    # def insert_user(self, user):
    #     if self.check_user_exist_name(user) == False:
    #         with self.conn:
    #             # """ First possiblity to insert upper data to the database """
    #             # c.execute("INSERT INTO users VALUES (?, ?, ?)", (user.first, user.last, user.id))

    #             """ Second possiblity to insert upper data to the database """
    #             self.c.execute("INSERT INTO users VALUES (:first, :last, :id)", {"first": user.first, "last": user.last, "id": user.id})
    #             print("\n!!!User created!!!\n")
    #     else:
    #         print("User already exist!")

    def insert_data(self):
        with self.conn:
            self.c.execute("INSERT INTO users VALUES (:userId, :userFirst, :userLast, :userEmail, :userRfid)",{"userId": 1, "userFirst": "marvin", "userLast": "willms", "userEmail" : "marvin.willms@code.berlin", "userRfid": 0})
            self.c.execute("INSERT INTO book VALUES (:bookId, :bookTitle)",{"bookId": 0, "bookTitle": "Python Course for Beginners"})
            self.c.execute("INSERT INTO bookcopy VALUES (:bookcopyId, :bookId, :bookRfid, :bookLent, :userId)",{"bookcopyId": 0, "bookId": 0, "bookRfid" : 5678765456789, "bookLent": 0, "userId": 1})


    def get_data_by_userId(self, userId):
        self.c.execute("SELECT * FROM users WHERE userId=:userId", {"userId":userId})
        return self.c.fetchall()


    def update_id(self, userId, id):
        print("Should update now!")
        print(userId)
        print(type(userId))
        with self.conn:
            self.c.execute("""UPDATE users SET userRfid = :id
                        WHERE userId = :userId""",
                    {"userId": userId, 'id': id})
        return True
            


    def remove_user(self, user):
        with self.conn:
            self.c.execute("DELETE from users WHERE first = :first AND last = :last",
                    {'first': user.first, 'last': user.last})


    def check_user_exist_name(self, user):
        self.c.execute("SELECT * FROM users WHERE userFirst = :first AND userLast = :last", {"first":user.first,"last":user.last})
        check = self.c.fetchall()
        if check != []:
            if len(check) != 1:
                print("There are more than one user with this name....")
                return False
            else:
                return check[0][0]
        else:
            return False


    def check_user_exist_id(self, id):
        self.c.execute("SELECT * FROM users WHERE userRfid = :id", {"id" : id})
        check = self.c.fetchall()
        if check != []:
            return check[0][0]
        else: 
            return False

        
    def check_book_exist_id(self, id):
        self.c.execute("SELECT * FROM book_bookcopies WHERE bookRfid = :id", {"id": id})
        check = self.c.fetchall()
        if check != []:
            return check[0][0]
        else:
            False

    
    def connect_ID_with_user(self, user, id):
        userId = self.check_user_exist_name(user)
        if userId:
            update = self.update_id(userId, id)
            return update
        else:
            return False

    def check_confirm_with_userId(self, userId):
        self.c.execute("SELECT * FROM users WHERE userId = :userId", {"userId": userId})
        check = self.c.fetchall()
        if check[0][5] == 1:
            return True
        else: 
            return False

    def confirm_with_userId(self, userId):
        print("Should confirm now!")
        print(userId)
        print(type(userId))
        with self.conn:
            self.c.execute("""UPDATE users SET userConfirm = :userConfirm
                        WHERE userId = :userId""",
                    {"userId": userId, 'userConfirm': 1})
        return True

    def reset_confirm_with_userId(self, userId):
        print("Should reset confirm now!")
        print(userId)
        print(type(userId))
        with self.conn:
            self.c.execute("""UPDATE users SET userConfirm = :userConfirm
                        WHERE userId = :userId""",
                    {"userId": userId, 'userConfirm': 0})
        return True


