import random
import math
import json

def softmax_clipped(scores):
		exp_scores = [math.exp(min(score, 100)) for score in scores]
		total_exp = sum(exp_scores)
		softmax_scores = [score / total_exp for score in exp_scores]
		return softmax_scores

class Q_graph:
    def __init__(self,q_graph_dict, alpha=1,gamma=1):
        self.q_graph = q_graph_dict
        self.current_node = random.choice(list(q_graph_dict.keys()))
        self.alpha = alpha
        self.gamma = gamma

    def optimize(self,iterations,supidity_rate=.1):
        current_path_num = 1
        current_path = []
        log = dict()
        
        for i in range(iterations):
            current_path.append(self.current_node)
            #print(self.current_node)

            ongoing = self.decide_neighbor(supidity_rate)
            if not ongoing:
                log[current_path_num] = current_path
                current_path_num += 1
                current_path = []

            #print(self.current_node)
            #print('***********************')
        current_path.append(self.current_node)
        log[current_path_num] = current_path
        with open('log.json', 'w') as fi:
            fi.write(json.dumps(log, indent = 4))
        print(self.q_graph)

    def update_q_values(self, current_node, new_node):
        old_q,reward = self.q_graph[current_node][new_node]
        neighbors = list(self.q_graph[new_node].keys())
        max_neighbor_q = max([self.q_graph[new_node][x][0] for x in neighbors], default=0)
        new_q = old_q + self.alpha*( reward +  self.gamma*max_neighbor_q - old_q)
        self.q_graph[current_node][new_node] = (new_q,reward)


    def decide_neighbor(self,stupidity_rate=.3):
        neighbors = list(self.q_graph[self.current_node].keys())
        if len(neighbors) == 0:
            self.current_node = random.choice(list(self.q_graph.keys()))
            return False
        else:
            logic = ['smart','stupid']
            logic_weights = [1-stupidity_rate, stupidity_rate]
            decision = random.choices(logic,logic_weights,k=1).pop()
            print(decision)
            if decision == 'stupid':
                new_neighbor = random.choice(neighbors)
            else:
                neighbor_qs = [self.q_graph[self.current_node][x][0] for x in neighbors]
                softmax_qs = softmax_clipped(neighbor_qs)
                new_neighbor = random.choices(neighbors,softmax_qs,k=1).pop()
            self.update_q_values(self.current_node,new_neighbor)
            self.current_node = new_neighbor
            return True

if __name__ == '__main__':
		q_graph_dict = dict()
		for i in range(11):
				if i == 0:
						q_graph_dict.update({i: {1: (1,0)}})
				elif i == 10:
						q_graph_dict.update({i: {}})
				elif i == 9:
						q_graph_dict[9] = {8:(1,0), 10: (1,1000000)}
				else:
						q_graph_dict.update({i: {i-1: (1,0), i+1: (1,0)}})


		q_graph = Q_graph(q_graph_dict, gamma = 0.1)
		q_graph.optimize(iterations=1000,supidity_rate=.1)
