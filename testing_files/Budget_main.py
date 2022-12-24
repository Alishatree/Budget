import tkinter

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
from sqlalchemy import create_engine
import pandas as pd
import pymysql
import sql_connector_key.key as key

# connector Url to the MySQL database
k = key.Key()


# Connection to the SQL database
engine = create_engine(k.this_is_key())
conn = engine.connect()


# CSV data being converted into an object to work with and put into the graphs
dataset = pd.read_sql("SELECT * FROM budget", conn)

# Data from SQL, being converted into python variables
# x = Dates
# y = Money
x_budget = dataset.iloc[:, :1]
y_budget = dataset.iloc[:, 1:]

# Tkinter

tkwindow = tk.Tk()

buttonfood = tkinter.Button(text="Food",)
buttonfood.pack(side= tk.TOP)

plt.style.use('ggplot')
f = Figure(figsize=(12, 6), dpi= 100 )
a = f.add_subplot(111)
a.plot(x_budget, y_budget)


canvas = FigureCanvasTkAgg(f, tkwindow)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2Tk(canvas)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

tkwindow.mainloop()

######## SQL ##########




# Establishing the style of the graph and the size of the window.
# plt.style.use('ggplot')
# plt.figure(figsize=(12, 6))
#
# # Plots the data and activates the graph
# plt.plot(x_budget, y_budget)
# plt.show()
#

