import sqlite3
class Image:
    id=None
    path=None
    is_right=None

    def __init__(self,id):
        self.id = id
        connection = sqlite3.connect("database.db")
        cursor = connection.execute("SELECT * FROM IMAGES WHERE ID=:ID",{"ID":self.id}).fetchall()
        self.path = cursor[0][1]
        self.is_right = cursor[0][3]

    def get_image_path(self):
        return self.path

    def get_is_right(self):
        return self.is_right



