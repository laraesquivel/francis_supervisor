import tkinter as tk
import math
import random
from PIL import Image, ImageTk
from supervisor_system import SupervisorSystem
import threading


class RoboApp:
    def __init__(self, root, supervisor,initial_position):
        self.root = root
        self.root.title("Francis Supervisor System 0.1")

        self.supervisor = supervisor
        # Define as dimensões da arena
        #self.width = 816 #O
        self.width = 180*2
        #self.width = 544
        #self.height = 540
        self.height = 270*2
        #self.height = 360
        self.supervisor.gui_callback = self.update_position_from_supervisor  # Set the callback

        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack(side=tk.LEFT)

        # Carrega a imagem de fundo
        self.bg_image = Image.open("map.jpg")  # Altere para o caminho da sua imagem
        self.bg_image = self.bg_image.resize((self.width, self.height), Image.ANTIALIAS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        #self.move_button = tk.Button(root, text="Mover Robô Aleatoriamente", command=self.mover_robo_aleatorio)

        # Área para exibir informações
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(side=tk.RIGHT, padx=10)

        #self.robo_pos = (self.width / 2, self.height / 2)  # Posição inicial do robô (centro da mesa)
        self.robo_pos = (53*2,31*2)
        self.robo_ang = 0
        self.robo = self.canvas.create_oval(initial_position[0]-5, initial_position[1]-5,
                                             initial_position[0]+5, initial_position[1]+5,
                                             fill="blue")

        # Lista para armazenar a trajetória
        self.trajectory = []

        # Labels para exibir a posição
        self.pos_label = tk.Label(self.info_frame, text=f"Posição do Robô: ({self.robo_pos[0]/2},{self.robo_pos[1]/2})")
        self.pos_label.pack()
        self.ang_label = tk.Label(self.info_frame, text=f"Angulo do Robo: {self.robo_ang}°")
        self.ang_label.pack()
        def onButtonInit():
            self.supervisor.send_bluetooth_command("i")
            print("comando enviado")
        self.buttonInit = tk.Button(self.info_frame, text="Iniciar", command=onButtonInit)
        #self.buttonInit.pack()

        #self.trajectory_label = tk.Label(self.info_frame, text="Trajetória: Nenhuma")
        #self.trajectory_label.pack()
        


        self.supervisor_thread = threading.Thread(target=self.supervisor.run)
        self.supervisor_thread.daemon = True  # Ensure thread exits when the program does
        self.supervisor_thread.start()

        # Start the update loop for the interface
        self.root.after(100, self.update_loop)

    

    def update_position_from_supervisor(self, distance, heading):
        """Atualiza a posição do robô na interface a partir dos dados do supervisor."""
        self.move(heading, distance)  # Mova o robô na interface

    def update_interface(self):
        distancia = self.supervisor.distance
        angulo = self.supervisor.heading
        self.move(distancia, angulo)

    def update_loop(self):
        # Update the interface based on supervisor data
        self.update_interface()
        self.root.after(100, self.update_loop)  # Repeat every 100ms
        
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

        moveDistance = distance
        #print(f"Comparaçao ({self.robo_ang} - {angle})>10) = {(self.robo_ang - angle)>10}")
        if (abs(self.robo_ang - angle)>10):
            self.robo_ang = angle
            moveDistance = 0
        angle_rad = math.radians(self.robo_ang)
        print(f"moveDistance: {moveDistance}\nangle: {self.robo_ang}")
        target_x = self.robo_pos[0] + moveDistance * math.sin(angle_rad)
        target_y = self.robo_pos[1] + moveDistance * math.cos(angle_rad)
        print(f"(x,y): ({target_x},{target_y})")
        
        target_x = max(5, min(target_x, self.width - 5))
        target_y = max(5, min(target_y, self.height - 5))

        # Armazena a nova posição na trajetória
        self.trajectory.append((target_x, target_y))

        # Atualiza a trajetória no label
        #self.atualiza_trajectory()

        # Inicia a animação de deslizar
        self.deslizar_robo(target_x, target_y)

    def deslizar_robo(self, target_x, target_y, steps=10):
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
        self.ang_label.config(text=f"Angulo do Robo: {self.robo_ang}°")

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

    def normalize_distance(self, distance, old_min=0, old_max=10000):
        normalized_x = (distance / old_max) * self.new_width
        
        # Normaliza a distância para a altura
        normalized_y = (distance / old_max) * self.new_height

        return normalized_x, normalized_y
    
    '''
    def onButtonInit():
        print("but")
        return
    '''