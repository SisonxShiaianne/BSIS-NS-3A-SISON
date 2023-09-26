#Menu Billing System (Group 5)
#Members: Grace Nicole Arquiza, Shiaianne Sison and Mariecris Camasis
from tkinter import *
from tkinter import messagebox
import time
import csv

class Item():
    def __init__(self,item,price): # Constructor __init__
        self.item = item
        self.price = price

class Main():

    def __init__(self): # Constructor __init__
        self.window = Tk()      #Creating a window 
        self.window.title('FAST FOOD MENU BILLING SYSTEM') 
        self.window.geometry('1050x500') 

        self.total_sales_amount = 0 #Varible for total sales that has a value of zero 
        
        self.present_month = time.localtime().tm_mon #Variable for the month

        self.total_sales_read()  #Function to read the csv file

        self.customers = ["REGULAR","STUDENT","SENIOR","PWD"];

        self.pizza = [Item("HAWAIIAN", 250), Item("PEPPERONI", 220), Item("SPINACH", 270), Item("VEGGEI", 200)]
        self.pasta = [Item("SPAGHETTI", 100), Item("CARBONARA", 150), Item("PESTO_PENNE", 200)]
        self.burger = [Item("REGULAR", 75), Item("CHEESE", 100), Item("BBQ", 120), Item("BACON-&-CHEESE", 150)]
        self.fries = [Item("CHEESE", 75), Item("BBQ", 75), Item("SOUR_&_CREAM", 75)]
        self.drinks = [Item("COKE", 25), Item("ICED_TEA", 40), Item("TEA", 70), Item("HOT_COFFEE", 70)]
        self.dessert = [Item("HALO-HALO", 85), Item("ICE_CREAM", 70)]

        self.customer_index = 0; 
        self.quantity = 1 #default quantity for ordering
        self.selected = "" #for selecting an item
        self.price = 0 
        self.total_amount = 0 
        self.sub_total_amount = 0 
        #Receipt part
        self.receipt_text = "\t        ------ RECEIPT ------\n\n DATE : "+time.ctime()+"\n\n ITEM ---------------------- QTY ---- PRICE ---- TOTAL\n\n";

        self.title = Label(self.window, text="FAST FOOD MENU BILLING SYSTEM", font=('Arial', 30, 'bold'), bg="#ffccff")
        self.title.place(height=80, width=1050, x=0, y=0) #size and position

        self.menu_buttons() #function to declare buttons for the menu
        #listbox of the menu where the user can choose which items to order
        self.menu = Listbox(self.window, font=('Arial', 15, 'bold'), bg='#ccffff')
        self.menu.place(height=150, width=270, x=50, y=250) 

        self.pizza_button_cmd() 
        self.ordering_properties()
        self.receipt_properties() 
        self.payment_properties()

        self.window.mainloop() #function to display the window

    def menu_buttons(self): #function to declare all the buttons in our menu 
        pizza_button = Button(self.window, text="PIZZA", font=('Arial', 15, 'bold'), command=self.pizza_button_cmd) 
        pizza_button.place(height=35, width=130, x=50, y=120)

        pasta_button = Button(self.window, text="PASTA", font=('Arial', 15, 'bold'), command=self.pasta_button_cmd)
        pasta_button.place(height=35, width=130, x=190, y=120)

        burger_button = Button(self.window, text="BURGER", font=('Arial', 15, 'bold'), command=self.burger_button_cmd)
        burger_button.place(height=35, width=130, x=50, y=160)

        fries_button = Button(self.window, text="FRIES", font=('Arial', 15, 'bold'), command=self.fries_button_cmd)
        fries_button.place(height=35, width=130, x=190, y=160)

        drinks_button = Button(self.window, text="DRINKS", font=('Arial', 15, 'bold'), command=self.drinks_button_cmd)
        drinks_button.place(height=35, width=130, x=50, y=200)

        dessert_button = Button(self.window, text="DESSERT", font=('Arial', 15, 'bold'), command=self.dessert_button_cmd)
        dessert_button.place(height=35, width=130, x=190, y=200)

        select_button = Button(self.window, text="SELECT ITEM", font=('Arial', 14, 'bold'), command=self.select_button_cmd)
        select_button.place(height=35, width=270, x=50, y=410)

    def ordering_properties(self): #function that has its designs and the buttons for making an order

        item_selected_text = Label(self.window, font=('Arial', 10, 'bold'), text='ITEM')
        item_selected_text.place(height=30, width=100, x=380, y=313) 

        self.item_selected = Label(self.window, font=('Arial', 15), bg='#ffcccc')
        self.item_selected.place(height=30, width=200, x=410, y=337)

        self.item_quantity = Label(self.window, font=('Arial', 15), bg='#ffffcc', text='1')
        self.item_quantity.place(height=30, width=80, x=470, y=370)

        item_quantity_dec = Button(self.window, text="-", font=('Arial', 20, 'bold'), command=self.item_quantity_dec_cmd) 
        item_quantity_dec.place(height=30, width=50, x=410, y=370)

        item_quantity_inc = Button(self.window, text="+", font=('Arial', 15, 'bold'), command=self.item_quantity_inc_cmd)
        item_quantity_inc.place(height=30, width=50, x=560, y=370)

        add_order = Button(self.window, text="ADD ORDER", font=('Arial', 15, 'bold'), command=self.add_order_cmd)
        add_order.place(height=35, width=200, x=410, y=410)

    def payment_properties(self): #also a function for the design and buttons for the customer and others
        customer_text = Label(self.window, font=('Arial', 10, 'bold'), text='CUSTOMER')
        customer_text.place(height=20, width=120, x=390, y=100)

        self.customer_selected = Label(self.window, font=('Arial', 15), bg='#ccccff') #label for selected customer        self.customer_selected.place(height=30, width=150, x=410, y=120)
        self.customer_selected.place(height=30, width=150, x=410, y=120)
        self.customer_selected.config(text=self.customers[self.customer_index])
        
        customer_change = Button(self.window, text=">", font=('Arial', 15, 'bold'), command=self.customer_change_cmd)
        customer_change.place(height=30, width=40, x=570, y=120)
    
        total_amount_payment_text = Label(self.window, font=('Arial', 10, 'bold'), text='TOTAL AMOUNT')
        total_amount_payment_text.place(height=20, width=120, x=405, y=160)
        
        self.total_amount_payment = Label(self.window, font=('Arial', 15), bg='#ccffcc')
        self.total_amount_payment.place(height=30, width=150, x=410, y=180)
        self.total_amount_payment.config(text='P'+str(self.total_amount))
    
        cash_text = Label(self.window, font=('Arial', 10, 'bold'), text='CASH') 
        cash_text.place(height=15, width=80, x=390, y=220)
        
        self.cash = Entry(self.window, font=('Arial', 15), bg='#ffccff')  
        self.cash.place(height=30, width=90, x=410, y=237)
        
        change_text = Label(self.window, font=('Arial', 10, 'bold'), text='CHANGE')
        change_text.place(height=15, width=80, x=510, y=220)
    
        self.change = Label(self.window, font=('Arial', 15), bg='#ccffff')
        self.change.place(height=30, width=90, x=520, y=237)
        
        pay = Button(self.window, text="PAY", font=('Arial', 13, 'bold'), command=self.pay_cmd)
        pay.place(height=30, width=200, x=410, y=270)

    def receipt_properties(self): #function for the receipt and design of it
        self.receipt_text_area = Text(self.window, font=('Arial', 10))
        self.receipt_text_area.place(height=285, width=290, x=705, y=160)
        self.receipt_text_area.insert("1.0", self.receipt_text)
        
        clear = Button(self.window, text="CLEAR", font=('Arial', 13, 'bold'), command=self.clear_cmd)
        clear.place(height=30, width=100, x=705, y=120)

        total_sales = Button(self.window, text="TOTAL SALES", font=('Arial', 13, 'bold'), command=self.total_sales_cmd)
        total_sales.place(height=30, width=175, x=820, y=120)

    def total_sales_read(self): #function for reading csv file
        try:
            f = open("total_sales.csv", 'r', newline="")
            reader = csv.reader(f)

            for i in reader:
                self.total_sales_amount = int(i[0])
                self.month = int(i[1])
                break

            if self.present_month != self.month:
                self.total_sales_amount = 0
        except:
            self.total_sales_amount = 0
    
    def clear_menu_list(self): #function to clear our items in the menu 
        for i in range(self.menu.size()):
            self.menu.delete(0)

    def space_provider(self,string): #function for spacing in the menu items
        space = ""
        for i in range(5 - len(string)):
            space += "  "
        return space

    def add_menu_list(self,list): #function to clear and add item in the menu
        self.clear_menu_list()
        for i in range(len(list)):
            self.menu.insert(i,'P'+str(list[i].price) + self.space_provider(str(list[i].price)) + list[i].item)

    def pizza_button_cmd(self): #function for adding items in the pizza menu
        self.add_menu_list(self.pizza)

    def pasta_button_cmd(self): #function for adding items in the pasta menu
        self.add_menu_list(self.pasta)

    def burger_button_cmd(self): #function for adding items in the burger menu
        self.add_menu_list(self.burger)

    def fries_button_cmd(self): #function for adding items in the fries menu
        self.add_menu_list(self.fries)

    def drinks_button_cmd(self): #function for adding items in the drinks menu
        self.add_menu_list(self.drinks)

    def dessert_button_cmd(self): #function for adding items in the dessert menu
        self.add_menu_list(self.dessert)

    def remove_peso_sign(self,string): #function to remove peso sign in the price of the items
        s = string.split("P")
        return s[1]

    def select_button_cmd(self): #function for selecting items in the menu
        self.quantity = 1; 
        self.item_quantity.config(text=self.quantity) 

        if self.menu.curselection() == ():
            messagebox.showinfo(title='INFORMATION', message='PLEASE SELECT ITEM FIRST')
            self.selected = "";
            self.price = 0
        else:
            sel = str(self.menu.get(self.menu.curselection()))
            separate = sel.split(" ")
            self.price = int(self.remove_peso_sign(separate[0]))
            self.selected = separate[len(separate) - 1]

        self.item_selected.config(text=self.selected)

    def item_quantity_dec_cmd(self): #function for decreasing item quantity
        if self.quantity > 1:
            self.quantity -= 1
            self.item_quantity.config(text=self.quantity)

    def item_quantity_inc_cmd(self): #function for increasing item quantity
        self.quantity += 1
        self.item_quantity.config(text=self.quantity)

    def reset_selection(self): #function to set default value with the selected item
        self.selected = ""
        self.item_selected.config(text=self.selected)
        self.price = 0
        self.quantity = 1;
        self.item_quantity.config(text=self.quantity)

    def dot_provider(self,string,max): #function for the dot text in the receipt
        dot = ""
        for i in range(max - len(string)):
            dot += "."
        return dot

    def add_order_cmd(self): # FUNCTION FOR ADDING THE ORDER
        if self.selected.__eq__(""):
            messagebox.showinfo(title='INFORMATION', message='PLEASE SELECT ITEM FIRST')
            self.quantity = 1;
            self.item_quantity.config(text=self.quantity)
        else:
            self.total_amount += self.quantity * self.price
            self.sub_total_amount +=  self.quantity * self.price

            # ADDING THE CUSTOMER'S ORDER TO THE RECEIPT
            self.receipt_text += self.selected +"\n..................................."+\
                                 str(self.quantity) +self.dot_provider(str(self.quantity),10)+'P'+\
                                 str(self.price) +self.dot_provider(str(),8)+'P'+\
                                 str(self.quantity * self.price) + '\n'
            self.reset_selection()
            self.total_amount_payment.config(text='P'+str(self.total_amount)) 
            self.receipt_text_area.delete("1.0",END)
            self.receipt_text_area.insert("1.0",self.receipt_text)

            self.discount()

    def discount(self): # FUNCTION FOR CHECKING THE DISCOUNT OF THE CUSTOMER
        if self.customer_index == 0: # REGULAR CUSTOMER = SAME PRICE/NO DISCOUNT
            self.total_amount = self.sub_total_amount
        elif self.customer_index == 1: # STUDENT DISCOUNT
            self.total_amount = self.sub_total_amount - int(self.sub_total_amount / 10)
        else: # PWD AND SENIOR CITIZEN DISCOUNT
            self.total_amount = self.sub_total_amount - int(self.sub_total_amount / 5)

        self.total_amount_payment.config(text='P' + str(self.total_amount))

    def customer_change_cmd(self): # FUNCTION FOR THE DISCOUNTED CUSTOMER
        if self.customer_index == len(self.customers) - 1:
            self.customer_index = 0
        else:
            self.customer_index += 1
        self.customer_selected.config(text=self.customers[self.customer_index])

        self.discount()

    def pay_cmd(self): # FUNCTION FOR THE PAYMENT
        try:
            if self.total_amount == 0:
                messagebox.showinfo(title='INFORMATION', message="YOU DIDN'T ORDER ANYTHING")
            elif self.cash.get().__eq__(""):
                messagebox.showinfo(title='INFORMATION', message="PLEASE ENTER A CASH AMOUNT")
            else:
                cash_inputed = int(self.cash.get())

                if self.total_amount > cash_inputed:
                    messagebox.showinfo(title='INFORMATION', message='INSUFFICIENT CASH')
                else:
                    self.change.config(text=str(cash_inputed - self.total_amount))

                    self.receipt_text += "\nTOTAL AMOUNT ................................. P"+str(self.total_amount)+\
                                         "\nCASH ................................................. P"+str(cash_inputed)+\
                                         "\nCHANGE ............................................ P"+str(cash_inputed - self.total_amount)
                    self.receipt_text_area.delete("1.0", END) 
                    self.receipt_text_area.insert("1.0", self.receipt_text) 

                    # SAVING THE UPDATED TOTAL AMOUNT TO OUR TOTAL_SALE CSV FILE 
                    f = open("total_sales.csv", 'w', newline="")
                    writer = csv.writer(f)
                    writer.writerow([str(self.total_sales_amount+self.total_amount),self.present_month])

                    self.total_sales_amount += self.total_amount # FOR UPDATING THE TOTAL SALES AMOUNT TO OUR GUI
        except:
            messagebox.showinfo(title='INFORMATION',message='PLEASE ENTER A NUMBER ONLY')
            self.cash.delete(0,END)
    
    def clear_cmd(self): # FUNCTION FOR SETTING EVERYTHING TO DEFAULT
        self.customer_index = 0
        self.customer_selected.config(text=self.customers[self.customer_index])
        self.total_amount = 0
        self.sub_total_amount = 0
        self.total_amount_payment.config(text='P' + str(self.total_amount))
        self.cash.delete(0,END)
        self.change.config(text="")
        self.reset_selection()
        self.receipt_text = "\t        ------ RECEIPT ------\n\n DATE : " + time.ctime() + "\n\n ITEM ---------------------- QTY ---- PRICE ---- TOTAL\n\n";
        self.receipt_text_area.delete("1.0", END)
        self.receipt_text_area.insert("1.0", self.receipt_text)
    
    def total_sales_cmd(self): # FUNCTION FOR SHOWING THE TOTAL SALES OF THE MONTH
        messagebox.showinfo(title='INFORMATION',message="TOTAL MONTH SALES = "+str(self.total_sales_amount))

Main() # CALLING OUR MAIN CLASS