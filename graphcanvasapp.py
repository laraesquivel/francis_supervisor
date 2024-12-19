import tkinter as tk
from PIL import Image, ImageTk
import networkx as nx
import matplotlib.pyplot as plt

from my_graph import MyGraph
import os

class GraphCanvasApp:
    def __init__(self, root, image_path):
        self.root = root
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Load and resize the image
        self.original_image = Image.open(image_path)
        self.resized_image = None
        self.tk_image = None

        # Graph structure
        # self.graph = nx.Graph()
        self.graph = MyGraph()

        self.rect_start = None
        self.current_rect = None
        self.rectangles = []

        # Create a label to show the coordinates
        self.coord_label = tk.Label(root, text="Coordenadas: (0, 0)", bg="white", font=("Arial", 10))
        self.coord_label.pack(side=tk.BOTTOM, anchor=tk.W)

        # Bind events
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<B3-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind('<ButtonRelease-3>', self.on_release_right)
        self.canvas.bind("<Motion>", self.on_mouse_move)  # Event to track mouse movement

    def on_resize(self, event):
        # Resize image to fit the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.resized_image = self.original_image.resize((canvas_width, canvas_height), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(self.resized_image)
        self.canvas.delete("all")  # Clear the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        # Redraw existing rectangles
        for ((x1, y1), (x2, y2)) in self.rectangles:
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue")

    def on_click(self, event):
        self.rect_start = (event.x, event.y)

    def on_right_click(self, event):
        self.rect_start = (event.x, event.y)

    def on_drag(self, event):
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = self.canvas.create_rectangle(
            self.rect_start[0], self.rect_start[1], event.x, event.y, outline="red"
        )

    def on_release_right(self, event):
        x1, y1 = self.rect_start
        x2, y2 = event.x, event.y
        self.rectangles.append(((x1, y1), (x2, y2)))
        self.graph.add_non_obstacules_node([(x1, y1), (x1, y2), (x2, y1), (x2, y2)])
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="green")
        self.rect_start = None
        self.current_rect = None

    def on_release(self, event):
        x1, y1 = self.rect_start
        x2, y2 = event.x, event.y
        self.rectangles.append(((x1, y1), (x2, y2)))
        self.graph.add_obstacules_node([(x1, y1), (x1, y2), (x2, y1), (x2, y2)])
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue")
        self.rect_start = None
        self.current_rect = None

    def on_mouse_move(self, event):
        # Update the label with the current mouse coordinates
        coord_text = f"Coordenadas: ({event.x}, {event.y})"
        self.coord_label.config(text=coord_text)

    def plot_graph(self):
        self.graph.generate_aresta()

        print('Ok nega!')
        
        pos = {node: node for node in self.graph.nodes}
        nx.draw(self.graph, pos, with_labels=True, node_color="lightblue", font_size=8)
        plt.show()
        # self.graph.plot_graph()
