import sqlite3
import Image
class Group:
    id = None
    statement = None
    images = [0,0,0,0,0,0,0,0,0]
    answer = [0,0,0,0,0,0,0,0,0] # RIGHT ANS TAKES FROM THE DATABASE
    response = [0,0,0,0,0,0,0,0,0] # BASED ON USER RESPONSE IT WILL CREATE A LIST

    def __init__(self,id):
        self.id=id # setting the group id
        connection = sqlite3.connect("database.db")
        cursor = connection.execute("SELECT id FROM IMAGES WHERE GROUP_ID=:ID", {"ID": self.id}).fetchall()
        i=0
        # NOW CALL THE IMAGE CLASS AND SET ATTRIBUTES FOR EVERY IMAGE
        for c in cursor:
            self.images[i] = Image.Image(c[0])
            # NOW SET THE RIGHT ANSWER FROM THE DATABASE
            self.set_answer_for(i,self.images[i].is_right)
            print(self.images[i].get_image_path())
            i += 1
        print(self.answer)
        #Now set the statement
        self.set_statement()

    def set_answer_for(self,index,value):
        self.answer[index] = value

    def get_answer_list(self):
        return self.answer

    def set_response_for(self,index):
        # just we have to apply toggle here
        if self.response[index]==1:
            self.response[index]=0
        else:
            self.response[index]=1

    # def get_answer_list(self):
    #     return self.response

    def set_statement(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.execute("SELECT * FROM GROUPS WHERE ID=:ID",{"ID":self.id}).fetchall()
        self.statement = cursor[0][1]
        print(self.statement)
        
    def get_image_path(self):
        return self.images