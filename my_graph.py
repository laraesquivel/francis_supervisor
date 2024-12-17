import networkx as nx
import matplotlib.pylab as plt
from patterns import OBSTACULO, NAOBSTACULO

class MyGraph(nx.Graph):
    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)
        self.obstaculo = 1

    
    def add_obstacules_node(self,obstacules_node : list):
        for ponto_obstac in obstacules_node:
            self.add_node(ponto_obstac, type=OBSTACULO, value=self.obstaculo)
        self.obstaculo+=1
        '''
        self.add_edges_from([(obstacules_node[0], obstacules_node[1]),
                             (obstacules_node[0], obstacules_node[2]),
                             (obstacules_node[3], obstacules_node[1]),
                             (obstacules_node[3], obstacules_node[2])])
        '''
        for i in [0,3]:
            for j in [1,2]:
                x1, y1 = obstacules_node[i]
                x2, y2 = obstacules_node[j]
                self.add_edge(obstacules_node[i], obstacules_node[j], weight=((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (0.5))


        
    def add_non_obstacules_node(self, non_obstacules_node : list):
        for ponto_n_obstacules_node in non_obstacules_node:
            self.add_node(ponto_n_obstacules_node,type=NAOBSTACULO, value=0)
            self.add_edges_from([(non_obstacules_node[0], non_obstacules_node[1]),
                        (non_obstacules_node[0], non_obstacules_node[2]),
                        (non_obstacules_node[3], non_obstacules_node[1]),
                        (non_obstacules_node[3], non_obstacules_node[2])])
        
    def minimun_short_path(self):
        pass

    def generate_aresta(self):
        edgesObjects = list(self.edges())
        nodes = list(self.nodes(data=True))

        for nodeId in range(0, len(nodes)):
            for nextNodeId in range(nodeId+1,len(nodes)):
                #print(type(nodes))
                if (not(nodes[nodeId][1]['value'] == nodes[nextNodeId][1]['value'] or nodes[nodeId][1]['value'] == 0)):
                    #print(f"Analisando {nodes[nodeId]} e {nodes[nextNodeId]}")
                    newEdge = (nodes[nodeId][0],nodes[nextNodeId][0])
                    isNewEdge = True
                    for edge in edgesObjects:
                        #print(newEdge)
                        if(self.segmentos_se_intersectam(newEdge,edge)):
                            #print(f"colisão entre {newEdge} e {edge} é {self.segmentos_se_intersectam(newEdge,edge)}")
                            isNewEdge = False
                            break
                    if(isNewEdge):
                        #print("nova aresta")
                        x1, y1 = nodes[nodeId][0]
                        x2, y2 = nodes[nextNodeId][0]
                        self.add_edge(nodes[nodeId][0], nodes[nextNodeId][0], weight=((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (0.5))
        
        print(self.edges(data=True))
        print(nx.shortest_path(self, source=nodes[0][0], target=nodes[-1][0], weight='weight'))          
        return

    def segmentos_se_intersectam(self, seg1, seg2):
        """
        Verifica se dois segmentos de reta se intersectam.
        Não considera segmentos que compartilham apenas um ponto como cruzados.
        """
        def orientacao(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # Colineares
            return 1 if val > 0 else 2  # Anti-horário ou horário

        def esta_no_segmento(p, q, r):
            return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
                    min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))

        # Pontos dos segmentos
        (x1, y1), (x2, y2) = seg1
        (x3, y3), (x4, y4) = seg2

        p1, p2 = (x1, y1), (x2, y2)
        q1, q2 = (x3, y3), (x4, y4)

        #Tem um ponto em comum
        if(p1 == q1 or p1 == q2):
            return False
        if(p2 == q1 or p2 == q2):
            return False
        
        # Orientações
        o1 = orientacao(p1, p2, q1)
        o2 = orientacao(p1, p2, q2)
        o3 = orientacao(q1, q2, p1)
        o4 = orientacao(q1, q2, p2)

        # Caso geral
        if o1 != o2 and o3 != o4:
            return True

        # Casos especiais: verificar colinearidade e sobreposição
        if o1 == 0 and esta_no_segmento(p1, q1, p2):
            return p1 != q1 and p2 != q1  # Exclui interseção apenas no extremo
        if o2 == 0 and esta_no_segmento(p1, q2, p2):
            return p1 != q2 and p2 != q2  # Exclui interseção apenas no extremo
        if o3 == 0 and esta_no_segmento(q1, p1, q2):
            return q1 != p1 and q2 != p1  # Exclui interseção apenas no extremo
        if o4 == 0 and esta_no_segmento(q1, p2, q2):
            return q1 != p2 and q2 != p2  # Exclui interseção apenas no extremo

        return False

    def distanceNodes(self, node1, node2):
        x1, y1 = node1[0]
        x2, y2 = node2[0]
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (0.5)
        return distance

    def reconstructPath(self, node):
        path = []
        while not(node == None):
             path.insert(0,list(node))
             node = node[1]['parent']
             #print(node)
        return path
    
    def findPath(self, start, goal):
        openList = [start]
        closeList = []

        start[1]['g'] = 0
        start[1]['h'] = self.distanceNodes(start, goal)
        start[1]['f'] = start[1]['h'] + start[1]['g']
        start[1]['parent'] = None

        while(len(openList) > 0):
            #print(f"openList = {openList}\n")
            current = openList[0]
            for i in openList[1:]:
                if (current[1]['f'] > i[1]['f']):
                    current = i
            if (current == goal):
                return self.reconstructPath(current)
            openList.remove(current)
            closeList.append(current)
            print(f"current selecionado: {current}")
            for neighbor in self.neighbors(current[0]):
                neighbor = (neighbor, self.nodes[neighbor])
                if (neighbor in closeList):
                    continue
                tentative_g = current[1]['g'] + self.distanceNodes(current, neighbor)

                if not(neighbor in openList):
                    openList.append(neighbor)
                elif (tentative_g >= neighbor[1]['g']):
                    continue
                
                neighbor[1]['parent'] = current
                neighbor[1]['g'] = tentative_g
                neighbor[1]['h'] = self.distanceNodes(neighbor, goal)
                neighbor[1]['f'] = neighbor[1]['g'] + neighbor[1]['h']
                print(f"neighbor selecionado: {neighbor}")
            print("\n")
        return None
    
    

    '''
    def plot_graph(self):
        pos = {node: node for node in self.nodes(data=True)}
        nx.draw(self.graph, pos, with_labels=True, node_color="lightblue", font_size=8)
        plt.show()
    '''