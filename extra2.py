import bluetooth
import time
import nxt
import io 
import sys
import threading

class SupervisorSystem:
    def __init__(self, ADDRESS='00:16:53:08:2D:DC', PORT=1):
        self.ADDRESS = ADDRESS
        self.PORT = PORT
        self.RUN = True
        self.distance = 0
        self.heading = 0.0
        self.wheel_diameter = 5.6
        self.axle_length = 16.5
        self.last_tacho_left = 0
        self.last_tacho_right = 0
        self.lock = threading.Lock()

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
                return command.strip()
        except bluetooth.btcommon.BluetoothError:
            return None
        return None

    def update_position(self,command):
        # Aqui você implementaria a lógica de atualização da posição
        self.distance = float(command[0])
        self.heading = float(command[1])
        print(self.distance, self.heading)

    def run(self):
  
        while self.RUN:
            #output = io.StringIO()
            #sys.stdout = output
            command = self.receive_bluetooth_command()
            if command:
                print(f"Comando recebido: {command}\n")
                #print(f'{command}'.strip())
                #sys.stdout = sys.__stdout__
                #printed_value = output.getvalue()
                #output.close()
    
                self.update_position(command.split(';'))
            time.sleep(1)
      
if __name__ == "__main__":
    supervisor = SupervisorSystem()
    supervisor.run()

