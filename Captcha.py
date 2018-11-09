from Image import Image
from Group import Group
# import Group
# import Image
import sqlite3
from tkinter import *
from PIL import Image, ImageTk
class Captcha(Group):
    num_groups = None
    num_failed_submissions = None
    panel = [0,0,0,0,0,0,0,0,0]
    img = [0,0,0,0,0,0,0,0,0]
    root = None
    frame = None
    result_panel=None
    chances=5

    def __init__(self,root,group_id):
        super().__init__(group_id)
        self.root=root
        self.group_id = group_id
        self.show_welcome_page()
        
   
    
    def show_welcome_page(self):
        self.frame = Frame(self.root, height=600, width=1000)
        heading = Label(self.frame,text=" WELCOME TO IMAGE BASED CAPTCHA ",fg="GREEN",font=('helvetica', 20, 'underline italic'))
        heading.grid(row=1,column=1)
        button = Button(self.frame,text="I am not a ROBOT",pady=10,bg='#07c', command=self.show_captcha)
        button.grid(row=2,column=1,sticky=N+S+E+W)
        self.frame.pack()
        
    
        
    def show_captcha(self):
        self.frame.destroy()
        self.frame = Frame(self.root, padx=10,pady=10)
        heading = Label(self.frame, text="Please verify yourself",fg="red",font=('helvetica', 15, 'underline italic')).grid(row=0,column=0,columnspan=5)
        statement = Label(self.frame, text=self.statement,fg="purple",font=('helvetica', 20,'bold')).grid(row=1,column=0,columnspan=5)
        iteration_valiable = 0
        for i in range(2,5):
            for j in range(2,5):
                self.img[iteration_valiable] = Image.open(self.images[iteration_valiable].get_image_path())
                self.img[iteration_valiable] = self.img[iteration_valiable].resize((150, 150), resample = Image.ANTIALIAS)
                self.img[iteration_valiable] = ImageTk.PhotoImage(self.img[iteration_valiable])
                self.panel[iteration_valiable] = Button(self.frame,image=self.img[iteration_valiable],padx=30,pady=30,bg="red",
                                                        command=lambda i=i,j=i,index=iteration_valiable: self.image_clicked(index,i,j))
                self.panel[iteration_valiable].grid(row=i,column=j)
                print(i," ",j)
                iteration_valiable += 1
        
        submit_button = Button(self.frame,text="VERIFY", command=self.verify).grid(row=6,sticky=N+S+E+W,column=2)
        reset = Button(self.frame,text="RESET", command=self.reset).grid(row=6,sticky=N+S+E+W,column=3,columnspan=1)
        next = Button(self.frame,text="NEW CAPTCHA", command=self.next_captcha).grid(row=6,sticky=N+S+E+W,column=4)
        self.frame.pack()
        
    def image_clicked(self,index,i,j):
        print("the index is ",index)
        # Now we have to save the response
        self.set_response_for(index)
        print(self.answer)
        print(self.response)
        print(self.panel[index])
        self.panel[index].config(bg='green')
        self.panel[index].grid()
        
    def verify(self):
        self.chances -= 1
        # we are going to compare the answer and response
        count=0
        if(self.answer ==self.response):
            count = 9
        else:
            count=-19
        if(self.result_panel):
            self.result_panel.destroy()
        if(count==9 and self.chances>0):
            print("VERIFIED")
            self.result_panel = Label(self.root,text="ACCESS GRANTED!" ,fg="GREEN",font=('helvetica', 40, 'underline italic'))
            self.result_panel.pack()
        elif(self.chances>0):
            print("REJECTED")
            self.result_panel = Label(self.root, text="WRONG... "+str(self.chances)+" left", fg="ORANGE",
                                      font=('helvetica', 40, 'underline italic'))
            self.result_panel.pack()
        else:
            print("DENIED")
            self.result_panel = Label(self.root, text="ACCESS DENIED, TRY AGAIN", fg="RED", font=('helvetica', 40, 'underline italic'))
            self.result_panel.pack()
            
    def reset(self):
        if(self.result_panel):
            self.result_panel.destroy()
        self.frame.destroy()
        self.show_captcha()
        
    def next_captcha(self):
        if (self.result_panel):
            self.result_panel.destroy()
        self.frame.destroy()
        # SELECT THE DIFF ID OF GROUP FROM THE DATABASE
        conn = sqlite3.connect("database.db")
        c = conn.execute("SELECT ID FROM GROUPS ORDER BY RANDOM() LIMIT 1")
        for i in c:
            self.group_id = i[0]
        # now initialize the captcha again
        super().__init__(self.group_id)
        self.show_captcha()
