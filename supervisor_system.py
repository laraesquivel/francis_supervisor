import bluetooth
import time


class SupervisorSystem:
    def __init__(self, ADDRESS='00:16:53:08:2D:DC', PORT=1):
        self.ADDRESS = ADDRESS
        self.PORT = PORT
        self.RUN = True
        self.distance = 0
        self.passo_anterior = 0
        self.angulo_anterior = 0
        self.heading = 0.0
        self.wheel_diameter = 5.6
        self.axle_length = 16.5
        self.last_tacho_left = 0
        self.last_tacho_right = 0
        # Inicializa a conexão Bluetooth
        self.initialize_bluetooth()

    def initialize_bluetooth(self):
        """Inicializa a comunicação Bluetooth."""
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.connect((self.ADDRESS, self.PORT))
        print("Conexão Bluetooth estabelecida.")

    def receive_bluetooth_command(self):
        """Recebe um comando via Bluetooth."""
        try:
            data = self.socket.recv(1024)
            if data:
                #return data.decode('utf-8',errors='ignore').strip()
                command = ''.join(chr(b) for b in data if 32 <= b <= 126)
                #print(command)
                return command.strip()
        except bluetooth.btcommon.BluetoothError as e:
            print(e)
        return None
    
    def send_bluetooth_command(self, command):
        """Envia uma string via Bluetooth."""
        try:
            # Envia o comando via Bluetooth
            self.socket.send(command)
            print(f"Comando enviado: {command}")
        except bluetooth.BluetoothError as e:
            print(f"Erro ao enviar comando Bluetooth: {e}")

    def update_position(self,command):
        # Aqui você implementaria a lógica de atualização da posição
        if self.passo_anterior == float(command[0]):
            self.distance = 0
        else:
            self.distance = float(command[0]) - self.passo_anterior
        self.passo_anterior = float(command[0])
        # self.distance = self.distance - float(command[0])
        self.heading = float(command[1])
        print(f"Modulo e sentido direçao: {self.distance}\nAngulo Direçao: {self.heading}")
        self.notify_gui()

    def run(self):
  
        while self.RUN:
            #output = io.StringIO()
            #sys.stdout = output
            command = self.receive_bluetooth_command()
            if command:
                print(f"----------\nComando recebido: {command}")
                #print(f'{command}'.strip())
                #sys.stdout = sys.__stdout__
                #printed_value = output.getvalue()
                #output.close()
    
                self.update_position(command.split(';'))
            time.sleep(1)
    
    def notify_gui(self):
        """Notifica a interface gráfica sobre a atualização da posição."""
        # Aqui, você pode usar um método de callback ou um sistema de eventos.
        if self.gui_callback:
            self.gui_callback(self.distance*2, self.heading)
      
if __name__ == "__main__":
    supervisor = SupervisorSystem()
    supervisor.run()