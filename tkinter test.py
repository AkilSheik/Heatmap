import tkinter as tk
from tkinter import ttk  
from PIL import Image, ImageTk
from tkinter import *
import sys




small_font = ('Verdana',1)
root = tk.Tk()



root.title("GlobePoints")
root.geometry("800x600")
style = ttk.Style(root)
root.tk.call('source', 'azure.tcl')                 
ttk.Style().theme_use('azure')                                                  #azure light theme


Grid.rowconfigure(root, 0, weight=1)                                             #text box larger than submit button
Grid.columnconfigure(root, 0, weight=3)
Grid.columnconfigure(root, 1, weight=1)
Grid.rowconfigure(root, 1, weight=100)                                           #map greater importance/size

query = tk.StringVar()
query_entry = ttk.Entry(root,textvariable = query, font=('calibre',18,'normal')) #text box

enter = ttk.Button(root, text ="Submit")                                         #submit button
query_entry.insert(0, 'place')
query_entry.grid(row=0,column=0, padx=30,pady=30, sticky="nsew")
enter.grid(row=0,column=1, pady=30, padx=20, sticky="nsew")





root.mainloop()