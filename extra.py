import tkinter as tk
import math
import random
from PIL import Image, ImageTk
from supervisor_system import SupervisorSystem

class RoboApp:
    def __init__(self, root, supervisor):
        self.root = root
        self.root.title("Francis Supervisor System 0.1")

        self.supervisor = supervisor
        # Define as dimensões da arena
        self.width = 272
        self.height = 180

        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack(side=tk.LEFT)

        # Carrega a imagem de fundo
        self.bg_image = Image.open("07577e41656dd79.jpg")  # Altere para o caminho da sua imagem
        self.bg_image = self.bg_image.resize((self.width, self.height), Image.ANTIALIAS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        #self.move_button = tk.Button(root, text="Mover Robô Aleatoriamente", command=self.mover_robo_aleatorio)
        self.move_button.pack(side=tk.TOP)

        # Área para exibir informações
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(side=tk.RIGHT, padx=10)

        self.robo_pos = (self.width / 2, self.height / 2)  # Posição inicial do robô (centro da mesa)
        self.robo = self.canvas.create_oval(self.robo_pos[0]-5, self.robo_pos[1]-5,
                                             self.robo_pos[0]+5, self.robo_pos[1]+5,
                                             fill="blue")

        # Lista para armazenar a trajetória
        self.trajectory = []

        # Labels para exibir a posição
        self.pos_label = tk.Label(self.info_frame, text=f"Posição do Robô: {self.robo_pos}")
        self.pos_label.pack()

        self.trajectory_label = tk.Label(self.info_frame, text="Trajetória: Nenhuma")
        self.trajectory_label.pack()

        # Bind mouse events
        self.canvas.tag_bind(self.robo, "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind(self.robo, "<B1-Motion>", self.drag)


    def update_interface(self):
        with self.supervisor.lock:
            distancia = self.supervisor.distance
            angulo = self.supervisor.heading
            self.move(distancia, angulo)

    def start_drag(self, event):
        self.offset_x = event.x - self.robo_pos[0]
        self.offset_y = event.y - self.robo_pos[1]

    def drag(self, event):
        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y

        # Limita a posição do robô dentro da mesa
        new_x = max(5, min(new_x, self.width - 5))
        new_y = max(5, min(new_y, self.height - 5))

        self.robo_pos = (new_x, new_y)
        self.canvas.coords(self.robo, new_x-5, new_y-5, new_x+5, new_y+5)
        self.atualiza_posicao()

    def move(self,angle,distance):

        angle_rad = math.radians(angle)

        target_x = self.robo_pos[0] + distance * math.cos(angle_rad)
        target_y = self.robo_pos[1] - distance * math.sin(angle_rad)

        target_x = max(5, min(target_x, self.width - 5))
        target_y = max(5, min(target_y, self.height - 5))

        # Armazena a nova posição na trajetória
        self.trajectory.append((target_x, target_y))

        # Atualiza a trajetória no label
        self.atualiza_trajectory()

        # Inicia a animação de deslizar
        self.deslizar_robo(target_x, target_y)

    def deslizar_robo(self, target_x, target_y, steps=50):
        start_x, start_y = self.robo_pos
        delta_x = (target_x - start_x) / steps
        delta_y = (target_y - start_y) / steps

        def move_step(step):
            if step <= steps:
                new_x = start_x + delta_x * step
                new_y = start_y + delta_y * step
                self.robo_pos = (new_x, new_y)
                self.canvas.coords(self.robo, new_x-5, new_y-5, new_x+5, new_y+5)
                self.root.after(10, move_step, step + 1)
            else:
                # Atualiza a posição final
                self.robo_pos = (target_x, target_y)
                self.atualiza_posicao()

                # Desenha a linha tracejada da trajetória
                self.desenhar_trajectory()

        move_step(1)

    def atualiza_posicao(self):
        self.pos_label.config(text=f"Posição do Robô: {self.robo_pos}")

    def atualiza_trajectory(self):
        if self.trajectory:
            trajectory_text = ", ".join([f"{pos}" for pos in self.trajectory])
            self.trajectory_label.config(text=f"Trajetória: {trajectory_text}")

    def desenhar_trajectory(self):
        if len(self.trajectory) > 1:
            for i in range(len(self.trajectory) - 1):
                start = self.trajectory[i]
                end = self.trajectory[i + 1]
                self.canvas.create_line(start[0], start[1], end[0], end[1], fill="red", dash=(4, 2), tags="trajectory")
