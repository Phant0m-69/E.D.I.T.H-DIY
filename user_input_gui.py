import tkinter as tk
from tkinter import simpledialog
ROOT = tk.Tk()
ROOT.withdraw()
num = int(simpledialog.askstring(title="Number of Objects",prompt="Enter the number of distict objects that will be trained"))
