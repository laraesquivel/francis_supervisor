import tkinter as tk

import nxt.backend 
from supervisor_system import SupervisorSystem
from interface import RoboApp
from blueNXT import BlueNXT
import nxt
from graphcanvasapp import GraphCanvasApp

root = tk.Tk()
app = GraphCanvasApp(root,'map.jpg')

plot_button = tk.Button(root, text='Plot Graph', command=app.plot_graph)
plot_button.pack()

root.mainloop()


#############
#Diviir string e envia todo o grafo
graph_str = 'la'
bluenxt = BlueNXT(graph_str)
graph_str_list = bluenxt.gerate()
BlueNXT.send_message_list(graph_str_list)

#supervisor 1
root = tk.Tk()
supervisor = SupervisorSystem()
app = RoboApp(root, supervisor)
root.mainloop()
