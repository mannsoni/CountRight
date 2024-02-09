from tkinter import*
from turtle import right
from PIL import Image,ImageTk     #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
import os
class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Made by Mann Soni ")
        self.root.resizable(False,False)
        self.root.config(bg="white")
        self.root.focus_force()

        self.bill_list=[]
        self.var_invoice=StringVar()
        #---------title----------
        lbl_title=Label(self.root,text="Bill Area",font=("Proxima Nova",30),bg="#7F886A",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=20,pady=2)

        lbl_invoice=Label(self.root,text="Invocie No.",font=("Montserrat",15),bg="white").place(x=50,y=90)
        txt_invoice=Entry(self.root,text=self.var_invoice,font=("Montserrat",15),bg="#F9F7F1").place(x=160,y=90,width=180,height=28)

        btn_search=Button(self.root,text="Search",command=self.search,font=("Montserrat",15,"bold"),bg="#38D7E7",fg="black",cursor="hand2").place(x=360,y=90,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("Montserrat",15,"bold"),bg="#FFA45B",fg="black",cursor="hand2").place(x=490,y=90,width=120,height=28)


#-------bill list--------------------
        sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=50,y=140,width=200,height=330)


        scrolly=Scrollbar(sales_Frame,orient=VERTICAL)
        self.Sales_List=Listbox(sales_Frame,font=("Montserrat",15),bg="#F9F7F1",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)
#-----------bill area------------------
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=280,y=140,width=565,height=330)

        lbl_title2=Label(bill_Frame,text="Customer Bill Area",font=("Proxima Nova",30),bg="#FFA883").pack(side=TOP,fill=X)


        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area=Text(bill_Frame,bg="#FCD783",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)

        self.show()

        #------------images---------------
        #self.bill_photo=Image.open("images/cat2.jpg")
        # self.bill_photo=self.bill_photo.resize((400,300),Image.ANTIALIAS)
        # self.bill_photo=ImageTk.PhotoImage(self.bill_photo)

        # lbl_image=Label(self.root,image=self.bill_photo,bd=0)
        # lbl_image.place(x=750,y=110)
        

        
#---------------------------------------------------------------------------------

    def show(self):
        del self.bill_list[:]
        self.Sales_List.delete(0,END)
        # print(os.listdir('bill'))  
        for i in os.listdir('bill'):
                if i.split('.')[-1]=='txt':
                        self.Sales_List.insert(END,i) 
                        self.bill_list.append(i.split('.')[0])
    
    def get_data(self,ev):
        index_=self.Sales_List.curselection()
        file_name=self.Sales_List.get(index_)
        print(file_name)
        self.bill_area.delete('1.0',END)
        fp=open(f'bill/{file_name}','r')
        for i in fp:
                self.bill_area.insert(END,i)
        fp.close()


    def search(self):
        if self.var_invoice.get()=="":
                messagebox.showerror("Error","Invoice no. should be required",parent=self.root)
        else:
                if self.var_invoice.get() in self.bill_list:
                        fp=open(f'bill/{self.var_invoice.get()}.txt','r')
                        self.bill_area.delete(1.0,END)
                        for i in fp:
                                self.bill_area.insert(END,i)
                        fp.close()
                else:
                        messagebox.showerror("Error","Invalid Invoice no.",parent=self.root)


    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)







if __name__=="__main__":
    root=Tk()
    obj=salesClass(root)
    root.mainloop()