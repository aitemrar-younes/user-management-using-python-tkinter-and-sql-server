import tkinter
from tkinter import messagebox
from tkinter import ttk
import re
import pyodbc

selectedItemInTable = -1

def db_connection():
    connection = pyodbc.connect(  'Driver={SQL Server};'
                        'Server=.\SQLEXPRESS;'
                        'Database=app;'
                        'Trusted_Connection=yes;')
    return connection
    
def validation(firstname, lastname, age, phone):
    name_reg = re.compile("^[a-zA-Z ]{3,}$")
    age_reg = re.compile("^[0-9]+$")
    phone_reg = re.compile("^0[567][0-9]{8}$")

    if name_reg.match(firstname) is None :
        messagebox.showerror('Validation Error', 'Error: first name is short or contains non alpha chars')
        return False

    if name_reg.match(lastname) is None :
        messagebox.showerror('Validation Error', 'Error: last name is short or contains non alpha chars')
        return False
        
    if age_reg.match(age) is None :
        messagebox.showerror('Validation Error', 'Error: age must be numbers')
        return False
    if int(age)<18 or int(age)>79 :
        messagebox.showerror('Validation Error', 'Error: age must be > 18 and less < 79')
        return False
    
    if phone_reg.match(phone) is None :
        messagebox.showerror('Validation Error', 'Error: phone number incorrect')
        return False
    return True
    
def clear_table():
   for item in table.get_children():
      table.delete(item)

def update_table():
    clear_table()
    query = "select * from users"
    cursor = db.cursor()
    cursor.execute(query)
    for row in cursor:
        print(row)
        table.insert("","end",values=[row[0],row[1],row[2],row[3],row[4],row[5],"male" if not row[6] else "female"])


def delete_row():
    global selectedItemInTable
    indextable = selectedItemInTable
    
    if(selectedItemInTable in locals()):
        print("t7richa")
    print(indextable)
    if(indextable == None or indextable == -1):
        return
    id = table.item(indextable)['values'][0]
    query = f"delete users where id = {id}"
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    update_table()
    selectedItemInTable = -1
    button_delete.config(state="disable")
    
def selectItem(a):
    global selectedItemInTable
    print(selectedItemInTable)
    selectedItemInTable = table.focus()
    #print (type(table.item(curItem)))
    #print (table.item(curItem).keys())
    #print (table.item(curItem)['values'])
    print(selectedItemInTable)
    button_delete.config(state="normal")
    if(selectedItemInTable in globals()):
        print("t7richa")

def submit():
    firstname = firstname_entry.get()
    lastname = lastname_entry.get()
    age = age_entry.get()
    phone = phone_entry.get()
    gender = gender_entry.get()
    print(firstname, lastname, age, phone, gender)
    is_valid = validation(firstname,lastname,age,phone)
    if is_valid:
        cursor = db.cursor()
        gender_code = 0 if gender =="male"else 1
        query = f"insert into dbo.users (first_name, last_name, age, phone, gender) values ('{firstname}','{lastname}',{age},'{phone}',{gender_code})"
        try:
            cursor.execute(query)
            db.commit()
            clear_table()
            update_table()
        except:
            messagebox.showerror('Insertion Error', 'Error: Something went wrong with record insertion into a database')

window = tkinter.Tk()
window.title('cosider')
window.geometry('650x550')
window.resizable(False, False)

menu_bar = tkinter.Menu()

menu_file = tkinter.Menu(menu_bar, tearoff=0)
menu_file.add_command(label="New")
menu_file.add_command(label="Open")
menu_file.add_command(label="Save")
menu_file.add_separator()
menu_file.add_command(label="Exit",command=quit)
menu_bar.add_cascade(label="File", menu=menu_file)

menu_edit = tkinter.Menu(menu_bar, tearoff=0)
menu_edit.add_command(label="Undo")
menu_edit.add_separator()
menu_edit.add_command(label="Copy")
menu_edit.add_command(label="Cut")
menu_edit.add_command(label="Paste")
menu_bar.add_cascade(label="Edit", menu=menu_edit)

menu_help = tkinter.Menu(menu_bar, tearoff=0)
menu_help.add_command(label="About")
menu_bar.add_cascade(label="Help", menu=menu_help)

window.config(menu=menu_bar)

db = db_connection()

frame = tkinter.Frame(window)
frame.pack(padx=20, pady=20)

user_info_frame = tkinter.LabelFrame(frame, text="user information")
user_info_frame.grid(row=0, column=0)
#first name field
firstname_label = tkinter.Label(user_info_frame, text="First name")
firstname_label.grid(row=0, column=0,padx=15, pady=5)

firstname_entry = tkinter.Entry(user_info_frame)
firstname_entry.grid(row=0, column=1,padx=15, pady=5)

#last name field
lastname_label = tkinter.Label(user_info_frame, text="Last name")
lastname_label.grid(row=0, column=2,padx=15, pady=5)

lastname_entry = tkinter.Entry(user_info_frame)
lastname_entry.grid(row=0, column=3,padx=15, pady=5)

#age field
age_label = tkinter.Label(user_info_frame, text="Age")
age_label.grid(row=1, column=0,padx=15, pady=5)

age_entry = tkinter.Spinbox(user_info_frame, from_=18, to=79)
age_entry.grid(row=1, column=1,padx=15, pady=5)

#phone field
phone_label = tkinter.Label(user_info_frame, text="Phone")
phone_label.grid(row=1, column=2,padx=15, pady=5)

phone_entry = tkinter.Entry(user_info_frame)
phone_entry.grid(row=1, column=3,padx=15, pady=5)

#gender field
gender_label = tkinter.Label(user_info_frame, text="Gender")
gender_label.grid(row=2, column=0,padx=15, pady=5)

gender_entry = ttk.Combobox(user_info_frame, values=['male', 'female'])
gender_entry.current(0)
gender_entry.grid(row=2, column=1,padx=15, pady=5)

#submit button
submit_button = tkinter.Button(frame, text="Submit", command=submit, background="#24a0ed", border=0, foreground="white")
submit_button.grid(row=1, column=0,sticky="news",pady=10)


table = ttk.Treeview(frame, columns=(1,2,3,4,5,6,7), height=15, show="headings" )
table.grid(row=2, column=0, sticky="news")

table.heading(1, text="ID")
table.heading(2, text="first name")
table.heading(3, text="last name")
table.heading(4, text="age")
table.heading(5, text="phone")
table.heading(6, text="date join")
table.heading(7, text="gender")

table.column(1, width=20, anchor="center")
table.column(2, width=75, anchor="center")
table.column(3, width=75, anchor="center")
table.column(4, width=15, anchor="center")
table.column(5, width=75, anchor="center")
table.column(6, width=75, anchor="center")
table.column(7, width=35, anchor="center")

table.bind('<ButtonRelease-1>', selectItem)

update_table()

button_delete = tkinter.Button(frame, text="DELETE", bg="#d41d2d", border=0, foreground="white", state="disabled", command=lambda : delete_row())
button_delete.grid(row=3,column=0,sticky="ensw",pady=5)


window.mainloop()
