from tkinter import*
from PIL import Image,ImageTk     #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Made by Mann Soni ")
        self.root.resizable(False,False)
        self.root.config(bg="#F9F7F1")
        self.root.focus_force()
        #----------------------------------------------------------
		#------All Variables-----------------
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_supid=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
        
        
        #---------------Search Frame---------------------
        
        #-----------------option-------------------------
        lbl_search=Label(self.root,text="Invoice no.",bg="#F9F7F1",font=("Proxima Nova",15))
        lbl_search.place(x=700,y=80)
        

        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("Montserrat",15),bg="#DFDDC5").place(x=800,y=80,width=170)
        btn_search=Button(self.root,text="Search",command=self.search,font=("Montserrat",15),bg="#C0EB6A",cursor="hand2").place(x=980,y=79,width=100,height=28)


        #--------------------title------------------------ 
        title=Label(self.root,text="Supplier Details",font=("Montserrat",20,"bold"),bg="#6FC7E1").place(x=50,y=10,width=1000,height=40)


        #-------------Content--------------------
        #------row1----------
        lbl_supplier_invoice=Label(self.root,text="Invocie No.",font=("Montserrat",15),bg="#F9F7F1").place(x=50,y=80)     
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_supid,font=("Montserrat",15),bg="#DFDDC5").place(x=180,y=80,width=180)

        #-----row2-----
        lbl_name=Label(self.root,text="Name",font=("Montserrat",15),bg="#F9F7F1").place(x=50,y=120)
        
        txt_name=Entry(self.root,textvariable=self.var_name,font=("Montserrat",15),bg="#DFDDC5").place(x=180,y=120,width=180)

        #-----row3-----
        lbl_contact=Label(self.root,text="Contact",font=("Montserrat",15),bg="#F9F7F1").place(x=50,y=160)
        
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("Montserrat",15),bg="#DFDDC5").place(x=180,y=160,width=180)


        #--------row4-------------
        lbl_desc=Label(self.root,text="Description",font=("Montserrat",15),bg="#F9F7F1").place(x=50,y=200)
                
        self.txt_desc=Text(self.root,font=("Montserrat",15),bg="#DFDDC5")
        self.txt_desc.place(x=180,y=200,width=470,height=120)
        

        #-----------button------------
        btn_save=Button(self.root,text="Save",command=self.add,font=("Montserrat",15),bg="#FFA45B",cursor="hand2").place(x=180,y=370,width=110,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,font=("Montserrat",15),bg="#FFA45B",cursor="hand2").place(x=300,y=370,width=110,height=35)
        btn_delte=Button(self.root,text="Delete",command=self.delete,font=("Montserrat",15),bg="#FFA45B",cursor="hand2").place(x=420,y=370,width=110,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("Montserrat",15),bg="#FFA45B",cursor="hand2").place(x=540,y=370,width=110,height=35)

        #---------------------supplierdetails-------------
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=700,y=120,width=380,height=350)


        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(emp_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="INVOICE NO.")
        self.supplierTable.heading("name",text="NAME")
        self.supplierTable.heading("contact",text="CONTACT")
        self.supplierTable.heading("desc",text="DESCRIPTION")
        
        self.supplierTable["show"]="headings"

        self.supplierTable.column("invoice",width=70)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("desc",width=100)
        

        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)
         
        self.show()
#------------------------------------------------------------------------------------------
    def add(self):
        con=sqlite3.connect(database=r'CR.db')
        cur=con.cursor()
        try:
            if self.var_supid.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_supid.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Invoice No. already assigned, try different",parent=self.root)
                else:
                    cur.execute("Insert into supplier(invoice,name,contact,desc) values(?,?,?,?)",(
                                            self.var_supid.get(),
                                            self.var_name.get(),
                                            self.var_contact.get(),
                                            self.txt_desc.get('1.0',END),
                                            
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successflly",parent=self.root) 
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)


    def show(self):
        con=sqlite3.connect(database=r'CR.db')
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=row)



        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root )


    def get_data(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']
        # print(row)
        self.var_supid.set(row[0]),                                            
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END,row[3]),
        


    def update(self):
        con=sqlite3.connect(database=r'CR.db')
        cur=con.cursor()
        try:
            if self.var_supid.get()=="":
                messagebox.showerror("Error","Invoice no. must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where eid=?",(self.var_supid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice no.",parent=self.root)
                else:
                    cur.execute("Update employee set name=?,contact=?,desc=? where invoice=? ",(
                                            
                                            self.var_name.get(),
                                            self.var_contact.get(),
                                            self.txt_desc.get('1.0',END),
                                            self.var_supid.get(),

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier updated successflly",parent=self.root) 
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database=r'CR.db')
        cur=con.cursor()
        try:
            if self.var_supid.get()=="":
                messagebox.showerror("Error","Invocie no. must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_supid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice no.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("Delete from supplier where invoice=?",(self.var_supid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier deleted successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)



    def clear(self):
        self.var_supid.set("")                                            
        self.var_name.set("")
                                            
        
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
        self.var_searchtxt.set("")
        
        self.show()




    def search(self):
        con=sqlite3.connect(database=r'CR.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice no. should be required",parent=self.root)

            else:
                cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record found",parent=self.root)



        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root )




if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()