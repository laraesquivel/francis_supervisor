import nxt
import nxt.locator

class BlueNXT:
    brick = None
    HOST = '00:16:53:08:2D:DC'


    @classmethod
    def send_message_list(cls,msg):
        with nxt.locator.find(host=cls.HOST) as brick:
            for item in msg:
                brick.message_write(1,item)

    def __init__(self, graph_string) -> None:
        self.graph_string = graph_string

    def dividir_string(self, tamanho_maximo=50):
    # Cria uma lista de substrings, cada uma com no máximo 'tamanho_maximo' caracteres
        return [self.graph_string[i:i + tamanho_maximo].encode() for i in range(0, len(self.graph_string), tamanho_maximo)]
    
    def gerate(self):
        string_arr = self.dividir_string()
        return string_arr


