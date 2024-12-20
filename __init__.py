import tkinter as tk

import nxt.backend 
from supervisor_system import SupervisorSystem
from interface import RoboApp
from blueNXT import BlueNXT
import nxt
from graphcanvasapp import GraphCanvasApp

root = tk.Tk()
app_graph = GraphCanvasApp(root,'map.jpg')
plot_button = tk.Button(root, text='Plot Graph', command=app_graph.plot_graph)
plot_button.pack()

root.mainloop()


#############
#Diviir string e envia todo o grafo
node1 = ((round(app_graph.points[0][0]/2),round(app_graph.points[0][1]/2)) ,{'type': 'Nao-Obstaculo', 'value': 0})
node2 = ((round(app_graph.points[1][0]/2),round(app_graph.points[1][1]/2)) ,{'type': 'Nao-Obstaculo', 'value': 0})
print(f"path {node1[0]} to {node2[0]} {app_graph.graph.findPath(node1, node2)}")
graph_str = app_graph.graph.francisPath([i[0] for i in app_graph.graph.findPath(node1, node2)])

bluenxt = BlueNXT(graph_str)
graph_str_list = bluenxt.gerate()
BlueNXT.send_message_list(graph_str_list)

#supervisor 1
root = tk.Tk()
supervisor = SupervisorSystem()
app = RoboApp(root, supervisor,app_graph.points[0])
root.mainloop()
