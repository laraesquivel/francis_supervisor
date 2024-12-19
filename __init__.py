import tkinter as tk

import nxt.backend 
from supervisor_system import SupervisorSystem
from interface import RoboApp
from blueNXT import BlueNXT
import nxt
import os



#############
#Diviir string e envia todo o grafo
graph_str = '"Em um dia claro e ensolarado, as aves cantam alegremente enquanto as árvores balançam suavemente com a brisa. As pessoas caminham pelas ruas, sorrindo e aproveitando cada momento da sua jornada. O mundo segue seu curso."'
bluenxt = BlueNXT(graph_str)
graph_str_list = bluenxt.gerate()
BlueNXT.send_message_list(graph_str_list)

#supervisor 1
root = tk.Tk()
supervisor = SupervisorSystem()
app = RoboApp(root, supervisor)
root.mainloop()