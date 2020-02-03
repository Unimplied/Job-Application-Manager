from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from data import Database
import matplotlib.pyplot as plt
import numpy as np

db = Database('applications.db')

# Defines global variable for buttons
global application_status
application_status = ''

# Creates style object
# style = ttk.Style()

def populate_list():
    applications_list.delete(0, END)
    for row in db.fetch():
        applications_list.insert(END, row)
    
def add_active():
    global application_status
    application_status = "Active"
    
def add_reject():
    global application_status
    application_status = "Rejected"

def add_accepted():
    global application_status
    application_status = "Offer Accepted"
    
def clear_input():
    company_entry.delete(0, END)
    title_entry.delete(0, END)
    application_entry.delete(0, END)
    application_status = ''

def add_item():
    if company_name.get() == '' or title_name.get() == '' or application_date.get() == '' or application_status == '':
        messagebox.showerror('Error', 'Required field missing. Please include all fields.')
        return
    db.insert(company_name.get(), title_name.get(), application_date.get(), application_status)
    applications_list.delete(0, END)
    applications_list.insert(END, (company_name.get(), title_name.get(), application_date.get(), application_status))
    clear_input()
    populate_list()
    
def select_item(event):
    global selected_item
    index = applications_list.curselection()[0]
    selected_item = applications_list.get(index)
    
    company_entry.delete(0, END)
    company_entry.insert(END, selected_item[1])
    
    title_entry.delete(0, END)
    title_entry.insert(END, selected_item[2])
    
    application_entry.delete(0, END)
    application_entry.insert(END, selected_item[3])
    
    application_status = ''
    
def update_selection():
    db.update(selected_item[0], company_name.get(), title_name.get(), application_date.get(), application_status)
    populate_list()

def remove_selection():
    db.remove(selected_item[0])
    clear_input()
    populate_list()
    
# Create window object
app = Tk()

# Company applied to
company_name = StringVar()
company_label = Label(app, text='Company Name:', font=('bold', 14), pady=10, padx=20)
company_label.grid(row=0, column=0, sticky=W)
company_entry = Entry(app, textvariable=company_name)
company_entry.grid(row=0, column=1)

# Job title
title_name = StringVar()
title_label = Label(app, text='Title:', font=('bold', 14), pady=10, padx=20)
title_label.grid(row=1, column=0, sticky=W)
title_entry = Entry(app, textvariable=title_name)
title_entry.grid(row=1, column=1)

# job application Date
application_date = StringVar()
application_date_label = Label(app, text='Application Date:', font=('bold', 14), pady=10, padx=20)
application_date_label.grid(row=2, column=0, sticky=W)
application_entry = Entry(app, textvariable=application_date)
application_entry.grid(row=2, column=1)

# Status buttons
ttk.active_application_btn = Button(app, text='Active', width = 12, command=add_active)
ttk.active_application_btn.grid(row=3, column=0, pady=10)

ttk.reject_btn = Button(app, text='Rejected', width = 12, command=add_reject)
ttk.reject_btn.grid(row=3, column=1, pady=10)

ttk.accepted_btn = Button(app, text='Offer Accepted', width = 12, command=add_accepted)
ttk.accepted_btn.grid(row=3, column=2, pady=10)

ttk.add_btn = Button(app, text='Add Selection', width = 12, command=add_item)
ttk.add_btn.grid(row=4, column=0)

ttk.update_btn = Button(app, text='Update Selection', width = 12, command=update_selection)
ttk.update_btn.grid(row=4, column=1)

ttk.remove_btn = Button(app, text='Remove Selection', width = 14, command=remove_selection)
ttk.remove_btn.grid(row=4, column=2)

ttk.clear_btn = Button(app, text='Clear Input', width = 12, command=clear_input)
ttk.clear_btn.grid(row=4, column=3)

# List box of active job applications
applications_list=Listbox(app, height=8, width=75)
applications_list.grid(row=5, column=0, columnspan=3, rowspan=6, pady=20, padx=20)


# Create scrollbar and connect to listbox
scrollbar=Scrollbar(app)
#scrollbar.grid(row=5, column=2)
applications_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=applications_list.yview)

# Bind select to Listbox
applications_list.bind('<<ListboxSelect>>', select_item)

# Bar chart box
def graph():
    # Imports counted values from Database
    total = Database.count_total(db)
    active = Database.count_active(db)
    rejected = Database.count_rejected(db)
    accepted = Database.count_accepted(db)
    
    # X-Axis Labels
    x_labels = np.array(['Total','Active', 'Rejected', 'Accepted'])
    # Y-Axis Values
    y_axis = np.array([total, active, rejected, accepted])
    
    w = 4
    nitems = len(y_axis)
    x_axis = np.arange(0, nitems*w, w) # Sets an array of x-coordinates
    fig, ax = plt.subplots(1)
    ax.bar(x_axis, y_axis, width = w, align='center')
    ax.set_xticks(x_axis);
    ax.set_xticklabels(x_labels, rotation=90);
    plt.show()

# Create button to plot Histogram
ttk.plot_chart = Button(app, text='Plot Chart', command=graph)
ttk.plot_chart.grid(row=11, column=0)

# Application title and window size declaration
app.title('Application Manager')
app.geometry('800x450')

# Populate data
populate_list()

# Start program
app.mainloop()
