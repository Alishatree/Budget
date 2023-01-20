import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine
import pandas as pd
import pymysql
import sql_connector_key.key as key
matplotlib.use("TkAgg")
plt.style.use('seaborn-v0_8-darkgrid')

# connector Url to the MySQL database
k = key.Key()


# Connection to the SQL database
# Key is private data for security reason.
engine = create_engine(k.this_is_key())
conn = engine.connect()


# Using a SQL query and panda's ability to read sql to get data from my MySql database.
# Panda converts the SQL data into a dataframe, which is than used to select the data
# that I need for the graphs.
budget = pd.read_sql("SELECT * FROM budget", conn)
unique_query_budget_total = pd.read_sql("SELECT * FROM budget ORDER BY day_id DESC LIMIT 1", conn)
x_budget = budget.iloc[:, :1]
y_budget = budget.iloc[:, 1:]
budget_total = unique_query_budget_total.iloc[0]['money']

# Establishing the matlibplot before the program enters into the class
# At first it plots the data in the budget table of the database.
# After the data on the graph updates to another set of data, if you need to go back
# to the budget graph again the function will update the graph.
f = Figure(figsize=(12, 6), dpi=100)
a = f.add_subplot(111)
a.plot(x_budget, y_budget)
a.set_title("Checking Account\n Total: " + str(budget_total))


# Section of code that creates a window that allows you to add data to the database.

# This function is the template that I used to make the other functions in this section.
# The function itself creates a window that allows you to enter data in from the "Add to"
# Menu item.
def add_to_budget_form():

    # Function that allows the button to send the data in the entry widget to the SQL server
    def AddToBudget():
        # Converts the entry data into local variables
        day = day_entry.get()
        money = money_entry.get()

        # Creates a dataframe with Panda.
        d = {'day_id': [day], 'money': [money]}
        df = pd.DataFrame(data=d)

        # Sends the dataframe that was just created to the SQL server.
        df.to_sql('budget', con=conn, if_exists='append', index=False)

        # Resets the table after the button is pressed.
        # This is a design feature to indicate the data's been processed.
        day_entry.delete(0, len(day))
        money_entry.delete(0, len(money))



    popup = tk.Tk()
    popup.wm_title("Add to Budget")

    frame = tk.Frame(popup)
    frame.pack(side="top", fill="both")

    lb1 = tk.Label(frame, text="Date")
    lb1.pack(in_=frame, side='left')

    day_entry = tk.Entry(frame)
    day_entry.pack(in_=frame, side='left')

    lb2 = tk.Label(frame, text="Money")
    lb2.pack(in_=frame, side='left')

    money_entry = tk.Entry(frame,)
    money_entry.pack(in_=frame, side='left')

    # The button that sends the data in the Entry widgets over to the SQL server.
    submit = ttk.Button(frame, text="Submit", command = lambda: AddToBudget())
    submit.pack(in_=frame, side='left')

    popup.geometry('400x75')
    popup.mainloop()


def add_to_SPY_form():

    def add_to_SPY():
        day = day_entry.get()
        money = money_entry.get()

        d = {'month_id': [day], 'money': [money]}
        df = pd.DataFrame(data=d)

        df.to_sql('SPY', con=conn, if_exists='append', index=False)
        day_entry.delete(0, len(day))
        money_entry.delete(0, len(money))


    popup = tk.Tk()
    popup.wm_title("Add to SPY")

    frame = tk.Frame(popup)
    frame.pack(side="top", fill="both")

    lb1 = tk.Label(frame, text="Date")
    lb1.pack(in_=frame, side='left')

    day_var = tk.StringVar()
    day_entry = tk.Entry(frame, textvariable=day_var)
    day_entry.pack(in_=frame, side='left')

    lb2 = tk.Label(frame, text="Money")
    lb2.pack(in_=frame, side='left')

    money_entry = tk.Entry(frame, )
    money_entry.pack(in_=frame, side='left')

    submit = ttk.Button(frame, text="Submit", command=lambda: add_to_SPY())
    submit.pack(in_=frame, side='left')

    popup.geometry('400x75')
    popup.mainloop()


def add_to_401k_form():

    def add_to_401k():
        day = day_entry.get()
        money = money_entry.get()

        d = {'month_id': [day], 'money': [money]}
        df = pd.DataFrame(data=d)

        df.to_sql('retirement', con=conn, if_exists='append', index=False)
        day_entry.delete(0, len(day))
        money_entry.delete(0, len(money))

    popup = tk.Tk()
    popup.wm_title("Add to 401k")

    frame = tk.Frame(popup)
    frame.pack(side="top", fill="both")

    lb1 = tk.Label(frame, text="Date")
    lb1.pack(in_=frame, side='left')

    day_var = tk.StringVar()
    day_entry = tk.Entry(frame, textvariable=day_var)
    day_entry.pack(in_=frame, side='left')

    lb2 = tk.Label(frame, text="Money")
    lb2.pack(in_=frame, side='left')

    money_entry = tk.Entry(frame,)
    money_entry.pack(in_=frame, side='left')

    submit = ttk.Button(frame, text="Submit", command = lambda: add_to_401k())
    submit.pack(in_=frame, side='left')

    popup.geometry('400x75')
    popup.mainloop()


# The expense forms are different from the 3 other forms.
# In the SQL database the expenses are all in one table,
# but also the Primary key is different and less dynamic.
# The budget's table's Primary Key is the date itself, while the expense table
# is the number of the entry_id.
def food_add_to_database_form():
    def add_to_food():
        # This gets the last variable of the entry_id column, allowing it to be added
        # on to while creating the dataframe. Allowing the primary key to be updated more
        # dynamically
        expenses_general = pd.read_sql("SELECT * FROM expenses", conn)
        id_expenses = expenses_general.iloc[:, 0:1]
        current_id = int(id_expenses.iloc[len(id_expenses) - 1])

        day = day_entry.get()
        money = money_entry.get()

        # These dataframes also include the "type_id" So they can be queried to their assigned
        # graphs in the future.
        d = {'entry_id': [current_id + 1], 'day_id': [day], 'money': [money], 'type_id': 'Food'}
        df = pd.DataFrame(data=d)
        df.to_sql('Expenses', con=conn, if_exists='append', index=False)

        day_entry.delete(0, len(day))
        money_entry.delete(0, len(money))

    popup = tk.Tk()
    popup.wm_title("Add to Food")

    frame = tk.Frame(popup)
    frame.pack(side="top", fill="both")

    lb1 = tk.Label(frame, text="Date")
    lb1.pack(in_=frame, side='left')

    day_var = tk.StringVar()
    day_entry = tk.Entry(frame, textvariable=day_var)
    day_entry.pack(in_=frame, side='left')

    lb2 = tk.Label(frame, text="Money")
    lb2.pack(in_=frame, side='left')

    money_entry = tk.Entry(frame, )
    money_entry.pack(in_=frame, side='left')

    submit = ttk.Button(frame, text="Submit", command=lambda: add_to_food())
    submit.pack(in_=frame, side='left')

    popup.geometry('400x75')
    popup.mainloop()


def gas_add_to_database_form():

    def add_to_gas():
        expenses_general = pd.read_sql("SELECT * FROM expenses", conn)
        id_expenses = expenses_general.iloc[:, 0:1]
        current_id = int(id_expenses.iloc[len(id_expenses) - 1])

        day = day_entry.get()
        money = money_entry.get()

        d = {'entry_id': [current_id + 1], 'day_id': [day], 'money': [money], 'type_id': 'Gas'}
        df = pd.DataFrame(data=d)
        df.to_sql('Expenses', con=conn, if_exists='append', index=False)

        day_entry.delete(0, len(day))
        money_entry.delete(0, len(money))




    popup = tk.Tk()
    popup.wm_title("Add to Gas")

    frame = tk.Frame(popup)
    frame.pack(side="top", fill="both")

    lb1 = tk.Label(frame, text="Date")
    lb1.pack(in_=frame, side='left')

    day_var = tk.StringVar()
    day_entry = tk.Entry(frame, textvariable=day_var)
    day_entry.pack(in_=frame, side='left')

    lb2 = tk.Label(frame, text="Money")
    lb2.pack(in_=frame, side='left')

    money_entry = tk.Entry(frame,)
    money_entry.pack(in_=frame, side='left')

    submit = ttk.Button(frame, text="Submit", command = lambda: add_to_gas())
    submit.pack(in_=frame, side='left')

    popup.geometry('400x75')
    popup.mainloop()


def fun_add_to_database_form():

    def add_to_fun():
        expenses_general = pd.read_sql("SELECT * FROM expenses", conn)
        id_expenses = expenses_general.iloc[:, 0:1]
        current_id = int(id_expenses.iloc[len(id_expenses) - 1])

        day = day_entry.get()
        money = money_entry.get()

        d = {'entry_id': [current_id + 1], 'day_id': [day], 'money': [money], 'type_id': 'Fun'}
        df = pd.DataFrame(data=d)
        df.to_sql('Expenses', con=conn, if_exists='append', index=False)

        day_entry.delete(0, len(day))
        money_entry.delete(0, len(money))


    popup = tk.Tk()
    popup.wm_title("Add to Fun")

    frame = tk.Frame(popup)
    frame.pack(side="top", fill="both")

    lb1 = tk.Label(frame, text="Date")
    lb1.pack(in_=frame, side='left')

    day_var = tk.StringVar()
    day_entry = tk.Entry(frame, textvariable=day_var)
    day_entry.pack(in_=frame, side='left')

    lb2 = tk.Label(frame, text="Money")
    lb2.pack(in_=frame, side='left')

    money_entry = tk.Entry(frame,)
    money_entry.pack(in_=frame, side='left')

    submit = ttk.Button(frame, text="Submit", command = lambda: add_to_fun())
    submit.pack(in_=frame, side='left')

    popup.geometry('400x75')
    popup.mainloop()


def health_add_to_database_form():

    def add_to_health():
        expenses_general = pd.read_sql("SELECT * FROM expenses", conn)
        id_expenses = expenses_general.iloc[:, 0:1]
        current_id = int(id_expenses.iloc[len(id_expenses) - 1])

        day = day_entry.get()
        money = money_entry.get()

        d = {'entry_id': [current_id + 1], 'day_id': [day], 'money': [money], 'type_id': 'Health'}
        df = pd.DataFrame(data=d)
        df.to_sql('Expenses', con=conn, if_exists='append', index=False)

        day_entry.delete(0, len(day))
        money_entry.delete(0, len(money))


    popup = tk.Tk()
    popup.wm_title("Add to Health")

    frame = tk.Frame(popup)
    frame.pack(side="top", fill="both")

    lb1 = tk.Label(frame, text="Date")
    lb1.pack(in_=frame, side='left')

    day_var = tk.StringVar()
    day_entry = tk.Entry(frame, textvariable=day_var)
    day_entry.pack(in_=frame, side='left')

    lb2 = tk.Label(frame, text="Money")
    lb2.pack(in_=frame, side='left')

    money_entry = tk.Entry(frame,)
    money_entry.pack(in_=frame, side='left')

    submit = ttk.Button(frame, text="Submit", command = lambda: add_to_health())
    submit.pack(in_=frame, side='left')

    popup.geometry('400x75')
    popup.mainloop()


def popup():
    popup = tk.Tk()
    popup.wm_title("Not added")

    label = tk.Label(text= "not added yet")
    label.pack()

    popup.geometry('200x150')
    popup.mainloop()


# Section of code that switches the data being shown on the Matplotlib graph
# All the functions follows the same general format.
# They each call the data again from the SQL server using queries.
# Then establishing the x and y axis with slices.
# The data is then cleared from the graph and re plotted using the new data.

# This updates the graph if it was changed through the "Add to" menu,
# and it also allows the graph to change what section of data is being displayed.
# Without having to change the frames of the program, which caused lag when the window
# was scaled.
def Budget(canvas):
    budget = pd.read_sql("SELECT * FROM budget", conn)
    # Queries the last day_id and puts the data frame row into a variable
    unique_query_budget_total = pd.read_sql("SELECT * FROM budget ORDER BY day_id DESC LIMIT 1", conn)
    x_budget = budget.iloc[:, :1]
    y_budget = budget.iloc[:, 1:]
    # Making a variable with the dataframe unique_query_budget_total and selecting the data in the "money" column.
    budget_total = unique_query_budget_total.iloc[0]['money']


    a.clear()
    a.plot(x_budget, y_budget)
    a.set_title("Checking Account\n Total: " + str(budget_total))
    canvas.draw()


def SPY(canvas):
    SPY = pd.read_sql("SELECT * FROM SPY", conn)
    SPY_total_db = pd.read_sql("SELECT * FROM SPY ORDER BY money DESC LIMIT 1", conn)
    x_SPY = SPY.iloc[:, :1]
    y_SPY = SPY.iloc[:, 1:]
    total_SPY = SPY_total_db.iloc[0]['money']

    a.clear()
    a.plot(x_SPY, y_SPY)
    a.set_title("SPY\n Total: " + str(total_SPY))
    canvas.draw()


def f_401k(canvas):
    d_401k = pd.read_sql("SELECT * FROM retirement", conn)
    d_401k_total = pd.read_sql("SELECT * FROM retirement ORDER BY money DESC LIMIT 1", conn)
    x_d_401k = d_401k.iloc[:, :1]
    y_d_401k = d_401k.iloc[:, 1:]
    total_401k = d_401k_total.iloc[0]['money']

    a.clear()
    a.plot(x_d_401k, y_d_401k)
    a.set_title("401k\n Total: " + str(total_401k))
    canvas.draw()


def FoodGraph(canvas):
    # These queries only select rows based on the type_id variable
    food = pd.read_sql("SELECT * FROM expenses as t WHERE t.type_id LIKE 'Food'", conn)
    food_money = []
    output = 0

    for x in range(len(food)):
        output += float(food.iloc[x]['money'])
        food_money.append(output)

    food_x = food.iloc[:, 1:2]

    a.clear()
    a.plot(food_x, food_money)
    # Formatting the data so that it only shows a month of the data at a time.
    month_locator = mdates.MonthLocator(interval= 2)
    month_formatter = mdates.DateFormatter("%m-%d")
    a.xaxis.set_major_locator(month_locator)
    a.xaxis.set_major_formatter(month_formatter)

    a.set_title("Food\n Total: " + str(food_money[len(food_money) - 1]))
    canvas.draw()


def Gas(canvas):
    gas = pd.read_sql("SELECT * FROM expenses as t WHERE t.type_id LIKE 'Gas'", conn)
    gas_money = []
    output1 = 0

    for x in range(len(gas)):
        output1 += float(gas.iloc[x]['money'])
        gas_money.append(output1)

    gas_x = gas.iloc[:, 1:2]

    a.clear()
    a.plot(gas_x, gas_money)

    month_locator = mdates.MonthLocator(interval= 2)
    month_formatter = mdates.DateFormatter("%m-%d")
    a.xaxis.set_major_locator(month_locator)
    a.xaxis.set_major_formatter(month_formatter)

    a.set_title("Gas \n Total: " + str(gas_money[len(gas_money) - 1]))
    canvas.draw()


def Fun(canvas):
    fun = pd.read_sql("SELECT * FROM expenses as t WHERE t.type_id LIKE 'Fun'", conn)
    fun_money = []
    output2 = 0

    for x in range(len(fun)):
        output2 += float(fun.iloc[x]['money'])
        fun_money.append(output2)

    fun_x = fun.iloc[:, 1:2]

    a.clear()
    a.plot(fun_x, fun_money)
    month_locator = mdates.MonthLocator(interval=2)
    month_formatter = mdates.DateFormatter("%m-%d")
    a.xaxis.set_major_locator(month_locator)
    a.xaxis.set_major_formatter(month_formatter)

    a.set_title("Entertainment \n Total: " + str(fun_money[len(fun_money) - 1]))
    canvas.draw()


def Health(canvas):
    health = pd.read_sql("SELECT * FROM expenses as t WHERE t.type_id LIKE 'Health'", conn)
    health_money = []
    output3 = 0

    for x in range(len(health)):
        output3 += float(health.iloc[x]['money'])
        health_money.append(output3)
    health_x = health.iloc[:, 1:2]

    a.clear()
    a.plot(health_x, health_money)
    month_locator = mdates.MonthLocator(interval=2)
    month_formatter = mdates.DateFormatter("%m-%d")
    a.xaxis.set_major_locator(month_locator)
    a.xaxis.set_major_formatter(month_formatter)

    a.set_title("Health \n Total: " + str(health_money[len(health_money) - 1]))
    canvas.draw()


# This is the class that allows the whole Tkinter program to use more of an
# Object-Oriented design. Was originally designed so that the frames could be changed
# so that the graph would change. But that made the program to but still liked how the
# code ended up being organized.
class BudgetStart(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        # Bitmap for the program.
        tk.Tk.iconbitmap(self, default="icon_for_budget_project.ico")
        tk.Tk.wm_title(self, "Budget and Investment Tracker")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # The menu section, which main functionality is to access the "Add to" windows.
        menubar = tk.Menu(container)

        # This is the first section which is mainly just for show
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command = lambda: popup())

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # This section is where the "Add To" entry windows are established and made.
        # Each button calls the form associated to their name.
        add_data_menu= tk.Menu(menubar, tearoff=0)
        add_data_menu.add_command(label="Budget", command= lambda: add_to_budget_form())

        add_data_menu.add_separator()

        add_data_menu.add_command(label="SPY", command= lambda: add_to_SPY_form())
        add_data_menu.add_command(label="401k", command= lambda: add_to_401k_form())

        add_data_menu.add_separator()

        add_data_menu.add_command(label="Food", command= lambda: food_add_to_database_form())
        add_data_menu.add_command(label="Gas", command= lambda: gas_add_to_database_form())
        add_data_menu.add_command(label="Fun", command= lambda: fun_add_to_database_form())
        add_data_menu.add_command(label="Health", command= lambda: health_add_to_database_form())

        menubar.add_cascade(label="Add Data", menu=add_data_menu)

        tk.Tk.config(self, menu=menubar)

        self.frame = {}
        F = StartPage
        page_name = F.__name__
        frame = F(parent=container, controller=self)
        self.frame[page_name] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frame[page_name]
        frame.tkraise()


# The main Frame of the program, most of the interactive buttons are established here.
# It's also were the graph for the program is established and plotted.
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        top = tk.Frame(self)
        top.pack(side="top", fill='both')

        # These are buttons that change what data is being shown, each of the functions
        # clears the data being displayed and updates it with the data in the function.
        buttonBudget = ttk.Button(text="Checking", command=lambda: Budget(canvas))

        # Packs the widget into the top framework with the parameter in_=top
        buttonBudget.pack(in_=top, side='left')

        buttonSPY = ttk.Button(text="SPY", command=lambda: SPY(canvas))
        buttonSPY.pack(in_=top, side= 'left')

        button401k = ttk.Button(text="401k", command= lambda: f_401k(canvas))
        button401k.pack(in_=top, side= 'left')

        buttonfood = ttk.Button( text="Food", command=lambda: FoodGraph(canvas))
        buttonfood.pack(in_=top, side='left')

        buttongas = ttk.Button( text="Gas", command=lambda: Gas(canvas))
        buttongas.pack(in_=top, side='left')

        buttonfun = ttk.Button(text="Fun", command=lambda: Fun(canvas))
        buttonfun.pack(in_=top, side='left')

        buttonAdd = ttk.Button(text="Health", command=lambda: Health(canvas))
        buttonAdd.pack(in_=top, side='left')


        # This makes the bitmap show on the icon, on the taskbar.
        # Don't really know why.
        plt.title("Checking Account")

        # This establishes the matplotlib graph and puts it into the program
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = BudgetStart()
app.geometry("1280x720")
app.mainloop()

