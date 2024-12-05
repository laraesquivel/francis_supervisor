import tkinter as tk 
from supervisor_system import SupervisorSystem
from interface import RoboApp



root = tk.Tk()
supervisor = SupervisorSystem()
app = RoboApp(root, supervisor)
root.mainloop()