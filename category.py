from ctypes import resize
from email.mime import image
from tkinter import*
from PIL import Image,ImageTk     #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Made by Mann Soni ")
        self.root.resizable(False,False)
        self.root.config(bg="#F3ECDB")
        self.root.focus_force()
        #---------variables----------------------
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        #-------------------title----------------------------------
        lbl_title=Label(self.root,text="Manage Product Category",font=("Proxima Nova",30),bg="#7F886A",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=20,pady=2)

        lbl_name=Label(self.root,text="Enter Category",font=("Montserrat",30),bg="#F3ECDB").place(x=50,y=60)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("Montserrat",18),bg="#B7AC9A").place(x=50,y=130,width=300)

        btn_add=Button(self.root,text="ADD",command=self.add,font=("Montserrat",15),bg="#FF6F3D",cursor="hand2").place(x=360,y=130,width=150,height=30)
        btn_delete=Button(self.root,text="DELETE",command=self.delete,font=("Montserrat",15),bg="#FF6F3D",cursor="hand2").place(x=520,y=130,width=150,height=30)

        #---------------------category-------------
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=60,width=380,height=100)


        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.categoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)

        self.categoryTable.heading("cid",text="C ID")
        self.categoryTable.heading("name",text="NAME")
        self.categoryTable["show"]="headings"
        self.categoryTable.column("cid",width=70)
        self.categoryTable.column("name",width=100)
        self.categoryTable.pack(fill=BOTH,expand=1)
        self.categoryTable.bind("<ButtonRelease-1>",self.get_data)

        #-------images-----------
        self.im1=Image.open("images/cat.jpg")
        self.im1=self.im1.resize((500,300),Image.ANTIALIAS)
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=180)


        self.im2=Image.open("images/cat2.jpg")
        self.im2=self.im2.resize((500,300),Image.ANTIALIAS)
        self.im2=ImageTk.PhotoImage(self.im2)
        
        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
        self.lbl_im2.place(x=580,y=180)
        self.show()
#---------------------Functions--------------------------------

    def add(self):
            con=sqlite3.connect(database=r'CR.db')
            cur=con.cursor()
            try:
                if self.var_name.get()=="":
                    messagebox.showerror("Error","Category name should be required",parent=self.root)
                else:
                    cur.execute("Select * from category where name=?",(self.var_name.get(),))
                    row=cur.fetchone()
                    if row!=None:
                        messagebox.showerror("Error","Category already assigned, try different",parent=self.root)
                    else:
                        cur.execute("Insert into category(name) values(?)",(
                                                    self.var_name.get(),
                                                        ))
                        con.commit()
                        messagebox.showinfo("Success","Category Added Successflly",parent=self.root) 
                        self.show()

            except Exception as ex:
                messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)


    def show(self):
        con=sqlite3.connect(database=r'CR.db')
        cur=con.cursor()
        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root )
    

    def get_data(self,ev):
        f=self.categoryTable.focus()
        content=(self.categoryTable.item(f))
        row=content['values']
        # print(row)
        self.var_cat_id.set(row[0]),                                            
        self.var_name.set(row[1]),


    def delete(self):
        con=sqlite3.connect(database=r'CR.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Please select category from the list",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error,please try again",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("Delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category deleted successfully",parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)









if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()