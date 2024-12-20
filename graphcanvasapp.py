import tkinter as tk
from PIL import Image, ImageTk
import networkx as nx
import matplotlib.pyplot as plt

from my_graph import MyGraph
import os

class GraphCanvasApp:
    def __init__(self, root, image_path):
        self.root = root
        self.width = 180*2
       
        self.height = 270*2
        self.canvas = tk.Canvas(root, bg="white", width=self.width,height=self.height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Load and resize the image
        self.original_image = Image.open(image_path)
        self.resized_image = None
        self.tk_image = None

        # Graph structure
        self.graph = MyGraph()

        self.rect_start = None
        self.current_rect = None

        # Initial points (non-obstacles) and rectangles (obstacles)
        # self.initial_points = [(0, 85), (0, 86), (60, 85),(60,86)]  # Example predefined points
        '''
        self.initial_rectangles = [((0,152),(80,182)),
                                   ((0,247),(80,228)),
                                   ((0,289),(80,310)),
                                   ((0,384),(80,365)),
                                   ((280,150),(380,171)),
                                   ((280,230), (380,250)),
                                   ((280,286),(380,307)),
                                   ((280,384),(380,365))]
        '''
        self.initial_rectangles = [((0,2*(39+47-20)),(2*50,2*(39+47+10))),
                                   ((0,2*(39+47-10+30)),(2*50,2*(39+47+30+39+10))),
                                   ((0,2*(39+47+30+39+10+10)),(2*50,2*(39+47+30+39+10+10+30))),
                                   ((2*(130),2*(39+47-20)),(2*180,2*(39+47+10))),
                                   ((2*(130),2*(39+47-10+30)),(2*180,2*(39+47+30+39+10))),
                                   ((2*(130),2*(39+47+30+39+10+10)),(2*180,2*(39+47+30+39+10+10+30)))]

        # Storage for drawn elements
        self.rectangles = []  # To store obstacles
        self.points = []      # To store non-obstacles

        # Create a label to show the coordinates
        self.coord_label = tk.Label(root, text="Coordenadas: (0, 0)", bg="white", font=("Arial", 10))
        self.coord_label.pack(side=tk.BOTTOM, anchor=tk.W)

        # Bind events
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_click_left)
        self.canvas.bind("<B1-Motion>", self.on_drag_left)
        self.canvas.bind("<ButtonRelease-1>", self.on_release_left)
        self.canvas.bind("<Button-3>", self.on_click_right)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # Draw initial elements
        self.load_initial_elements()

    def load_initial_elements(self):
        # Draw predefined points (non-obstacles)
        # for x, y in self.initial_points:
        #     self.points.append((x, y))
        #     self.graph.add_non_obstacules_node([(x, y)])
        #     #self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="green")

        # Draw predefined rectangles (obstacles)
        for (x1, y1), (x2, y2) in self.initial_rectangles:
            self.rectangles.append(((x1, y1), (x2, y2)))
            self.graph.add_obstacules_node([(round(x1/2), round(y1/2)), (round(x1/2),round(y2/2)), (round(x2/2), round(y1/2)), (round(x2/2), round(y2/2))])
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue")

    def on_resize(self, event):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.resized_image = self.original_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.resized_image)
        self.canvas.delete("all")  # Clear the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        # Redraw existing rectangles
        for ((x1, y1), (x2, y2)) in self.rectangles:
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue")

        # Redraw points
        for (x, y) in self.points:
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="green")

    def on_click_left(self, event):
        self.rect_start = (event.x, event.y)

    def on_drag_left(self, event):
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = self.canvas.create_rectangle(
            self.rect_start[0], self.rect_start[1], event.x, event.y, outline="red"
        )

    def on_release_left(self, event):
        x1, y1 = self.rect_start
        x2, y2 = event.x, event.y
        self.rectangles.append(((x1, y1), (x2, y2)))
        self.graph.add_obstacules_node([(round(x1/2), round(y1/2)), (round(x1/2), round(y2/2)), (round(x2/2), round(y1/2)), (round(x2/2), round(y2/2))])
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue")
        self.rect_start = None
        self.current_rect = None

    def on_click_right(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.graph.add_non_obstacules_node([(round(x/2), round(y/2))])
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="green")

    def on_mouse_move(self, event):
        coord_text = f"Coordenadas: ({round(event.x/2)}, {round(event.y/2)})"
        self.coord_label.config(text=coord_text)

    def plot_graph(self):
        self.graph.generate_aresta()

        pos = {node: node for node in self.graph.nodes}
        nx.draw(self.graph, pos, with_labels=True, node_color="lightblue", font_size=8)
        plt.show()