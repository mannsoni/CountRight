from cProfile import label
from os import access
from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
import time
import os
import tempfile

from PIL import Image, ImageTk  # pip install pillow


class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1520x790+0+0")
        self.root.title("Inventory Management System | Made by Mann Soni ")
        
        self.root.config(bg="#F9F7F1")
        self.cart_list=[]
        self.chk_print=0

        #-----title--------
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)


        #----btn_logout------
        btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1350,y=10,height=50,width=150)

        #-----clock-------
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)


        #-----------product frame----------
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="#F9F7F1")
        ProductFrame1.place(x=10,y=110,width=410,height=590)

        pTtitle=Label(ProductFrame1,text="All Products",font=("Montserrat",20,"bold"),bg="#373234",fg="white").pack(side=TOP,fill=X)

        #-----------product search frame------------------
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="#F9F7F1")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("Montserrat",15,"bold"),bg="#F9F7F1",fg="BLACK").place(x=2,y=5)

        lbl_name=Label(ProductFrame2,text="Product Name",font=("Montserrat",15,"bold"),bg="#F9F7F1").place(x=2,y=45)
        txt_name=Entry(ProductFrame2,textvariable=self.var_search,font=("Montserrat",15,"bold"),bg="#F3ECDB").place(x=140,y=48,width=149,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("Montserrat",15,),bg="#FF7FAE",fg="white",cursor="hand2").place(x=290,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("Montserrat",15,),bg="#8333E9",fg="white",cursor="hand2").place(x=290,y=10,width=100,height=25)

        #---------------------product details frame-------------
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=425)


        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)  

        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid",text="PID")
        self.product_Table.heading("name",text="NAME")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="QTY")
        self.product_Table.heading("status",text="Status") 
        
        self.product_Table["show"]="headings"

        self.product_Table.column("pid",width=40)
        self.product_Table.column("name",width=100)
        self.product_Table.column("price",width=60)
        self.product_Table.column("qty",width=60)
        self.product_Table.column("status",width=80)
        

        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        lbl_note=Label(ProductFrame3,text="Note: Enter 0 quantity to remove product from the cart",font=("Montserrat",10),bg="#F9F7F1",fg="red").pack(side=BOTTOM,fill=X)

        #---------------Customer frame------------------------
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="#F9F7F1")
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTtitle=Label(CustomerFrame,text="Customer Details",font=("Montserrat",15),bg="#373234",fg="white").pack(side=TOP,fill=X)
        
        lbl_name=Label(CustomerFrame,text="Name",font=("Montserrat",15),bg="#F9F7F1").place(x=5,y=30)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("Montserrat",13),bg="#F3ECDB").place(x=80,y=35,width=180)
        
        lbl_contact=Label(CustomerFrame,text="Contact",font=("Montserrat",15),bg="#F9F7F1").place(x=270,y=30)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("Montserrat",13),bg="#F3ECDB").place(x=360,y=35,width=160)
        
        #-----------cal cart frame------------------
        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="#F9F7F1")
        Cal_Cart_Frame.place(x=420,y=180,width=530,height=368)

        #-----------calculator frame------------------
        self.var_cal_input=StringVar()


        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="#F9F7F1")
        Cal_Frame.place(x=5,y=10,width=268,height=346)


        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('Dank Mono',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly')
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(Cal_Frame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='c',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=3)


        #-----------cart frame------------------
        cartFrame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        cartFrame.place(x=280,y=8,width=245,height=348)
        self.cTtitle=Label(cartFrame,text="Cart\tTotal Product: [0]",font=("Montserrat",10),bg="#373234",fg="white")
        self.cTtitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(cartFrame,orient=VERTICAL)
        scrollx=Scrollbar(cartFrame,orient=HORIZONTAL)  

        self.cartTable=ttk.Treeview(cartFrame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)

        self.cartTable.heading("pid",text="PID")
        self.cartTable.heading("name",text="NAME")
        self.cartTable.heading("price",text="Price")
        self.cartTable.heading("qty",text="QTY")
        
        self.cartTable["show"]="headings"

        self.cartTable.column("pid",width=30)
        self.cartTable.column("name",width=90)
        self.cartTable.column("price",width=80)
        self.cartTable.column("qty",width=30)
        

        self.cartTable.pack(fill=BOTH,expand=1)
        self.cartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #-----------add cart widgets buttons------------------
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        self.var_disc=StringVar()
        


        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="#F9F7F1")
        Add_CartWidgetsFrame.place(x=420,y=550,width=530,height=150)

        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product name",font=("Montserrat",15),bg="#F9F7F1").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("Montserrat",15),bg="#F9F7F1",state='readonly').place(x=5,y=35,width=190,height=35)

        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price Per Qty",font=("Montserrat",15),bg="#F9F7F1").place(x=210,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("Montserrat",15),bg="#F9F7F1",state='readonly').place(x=210,y=35,width=150,height=35)

        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("Montserrat",15),bg="#F9F7F1").place(x=370,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("Montserrat",15),bg="#F3ECDB").place(x=370,y=35,width=120,height=35)

        self.lbl_instock=Label(Add_CartWidgetsFrame,text="In Stock",font=("Montserrat",15),bg="#F9F7F1")
        self.lbl_instock.place(x=5,y=110)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("Montserrat",15,"bold"),bg="#FF7FAE",cursor="hand2").place(x=180,y=110,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update",command=self.add_update_cart,font=("Montserrat",15,"bold"),bg="#FF7FAE",cursor="hand2").place(x=340,y=110,width=180,height=30)

        #-----------------------------billing area-------------------------------------
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=953,y=110,width=565,height=438)

        BTtitle=Label(billFrame,text="Customer Bill",font=("Montserrat",20,"bold"),bg="#373234",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #---------------------------billing buttons-----------------------
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billMenuFrame.place(x=953,y=520,width=565,height=179)

        self.lbl_amnt=Label(billMenuFrame,text='Bill Amount\n[0]',font=("Montserrat",15,"bold"),bg="#33bbf9",fg="white")
        self.lbl_amnt.place(x=6,y=10,width=180,height=70)
        
        self.lbl_discount=Label(billMenuFrame,text='Discount\n',font=("Montserrat",15,"bold"),bg="#ff5722",fg="white").place(x=190,y=10,width=180,height=70)
        self.txt_discount=Entry(billMenuFrame,textvariable=self.var_disc,font=("Montserrat",15),bg="#F3ECDB").place(x=230,y=45,width=100,height=30)
        
        self.lbl_net_pay=Label(billMenuFrame,text='Net Pay\n[0]',font=("Montserrat",15,"bold"),bg="#009688",fg="white")
        self.lbl_net_pay.place(x=374,y=10,width=180,height=70)


        btn_print=Button(billMenuFrame,text='Print',command=self.print_bill,cursor='hand2',font=("Montserrat",15,"bold"),bg="#33bbf9",fg="white")
        btn_print.place(x=6,y=90,width=180,height=70)
        
        btn_clear_all=Button(billMenuFrame,text='Clear All',command=self.clear_all,cursor='hand2',font=("Montserrat",15,"bold"),bg="#ff5722",fg="white")
        btn_clear_all.place(x=190,y=90,width=180,height=70)
        
        btn_generate=Button(billMenuFrame,text='Generate/Save Bill',command=self.generate_bill,cursor='hand2',font=("Montserrat",15,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=374,y=90,width=180,height=70)


        #------------------fotter-------------
        lbl_footer=Label(self.root,text="IMS-Inventory Management System | Made By Mann Soni\n For any Technical Issue Contact: 7575074341",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        self.show()
        #self.bill_top()
        self.update_date_time()


    #-------------------ALL FUNCTION----------------------
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))


    def show(self):
        con=sqlite3.connect(database=r'CR.db')
        cur=con.cursor()
        try:
            
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def search(self):
        con=sqlite3.connect(database=r'CR.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input required",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+ self.var_search.get()+"%' and status='Active'" )
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record found",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root )


    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

#pid,name,price,qty,stock
    def get_data_cart(self,ev):
        f=self.cartTable.focus()
        content=(self.cartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    



    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Please select product from the list",parent=self.root)

        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantity is required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Invalid Quantity",parent=self.root)

        else:
            #price_cal=int(self.var_qty.get())*float(self.var_price.get())
            #price_cal=float(price_cal)
            price_cal=self.var_price.get()

            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]

            #-----------------update_cart---------------
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product already present\nDo you want to Update or Remove from the cart list",parent=self.root)   
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #pid,name,price,qty,status
                        #self.cart_list[index_][2]=price_cal
                        self.cart_list[index_][3]=self.var_qty.get()

            else:
                self.cart_list.append(cart_data)
                
            self.show_cart()
            self.bill_updates()



    def bill_updates(self):
        self.bill_amt=0
        self.net_pay=0
        
        for row in self.cart_list:
            #pid,name,price,qty,status     indexing
            self.bill_amt=self.bill_amt+(float(row[2])*int(row[3]))

        if self.var_disc.get()=='':
            messagebox.showerror('Error',"Discount is required",parent=self.root)
        else:
            self.discount=(self.bill_amt*float(self.var_disc.get()))/100
            self.net_pay=float(self.bill_amt-self.discount)

            
        self.lbl_amnt.config(text=f'Bill Amount\n{str(self.bill_amt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')

        self.cTtitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")



    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_list:
                self.cartTable.insert('',END,values=row)            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root )

    def generate_bill(self):
        if self.var_cname.get=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add product to the Cart!!!",parent=self.root)
            
        else:
            #-----------bill Top---------
            self.bill_top()
            #-----------bill middle---------
            self.bill_middle()
            #-----------bill bottom---------
            self.bill_bottom()

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been generated/Save in backend",parent=self.root)
            
            self.chk_print=1



    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\t\t\tMann-store
\t\tPhone No. 7575074341 , Ahmedadbad-380054
{str("-"*67)}
 Customer Name : {self.var_cname.get()}
 Ph No. : {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate : {str(time.strftime("%d/%m/%Y"))}
{str('-'*67)}
 Product Name\t\t\tQTY\tPrice
{str('-'*67)}
        '''
        
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)
            
    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("-"*67)}
 Bill Amount\t\t\t\tRs.{self.bill_amt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.bill_amt-self.discount}
{str("-"*67)}\n
    '''
        
        self.txt_bill_area.insert(END,bill_bottom_temp)


    def bill_middle(self):
        con=sqlite3.connect(database=r'CR.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                #pid,name,price,qty,status
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                
                if int(row[3])!=int(row[4]):
                    status='Active'
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                #-----------------update quantity in product table--------------------
                cur.execute('Update product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid
                    
                ))
                con.commit()

            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root )

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock [{str('')}]")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.var_disc.set('')
        self.txt_bill_area.delete('1.0',END)
        self.chk_print=0
        self.cTtitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print',"Please generate bill, to print the recipt",parent=self.root)




if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()
