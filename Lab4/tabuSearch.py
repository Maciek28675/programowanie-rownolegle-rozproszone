from flowShop import FlowShop
import random
from multiprocessing import Pool

class TabuSearch():
    def __init__(self, problem_instance: FlowShop):
        self.problem_instance = problem_instance

    def random_solution(self):
        jobs = self.problem_instance.jobs
        solution = random.sample(range(jobs), jobs)
        
        return solution
    
    def evaluate_move(self, args):
        current_solution, i, j = args

        neighbor = current_solution[:]
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

        cost = self.problem_instance.target_function(neighbor)

        return (i, j), neighbor, cost

    def tabu_search(self, initial_solution, max_iterations, tabu_list_size):
        best_solution = initial_solution[:]
        current_solution = initial_solution[:]
        best_cost = self.problem_instance.target_function(best_solution)
        tabu_list = []

        pool = Pool()

        for _ in range(max_iterations):
            best_neighbor, best_move = None, None
            best_neighbor_cost = float("inf")

            n = len(current_solution)

            moves = [(current_solution, i, j)
                     for i in range(n) for j in range(i+1, n)]
            
            # Search neighborhood
            results = pool.map(self.evaluate_move, moves)
            
            # Find best feasible move
            for move, neighbor, cost in results:
                if move not in tabu_list and cost < best_neighbor_cost:
                    best_neighbor = neighbor
                    best_neighbor_cost = cost
                    best_move = move

            if best_neighbor is None:
                break

            current_solution = best_neighbor

            # Update tabu list
            tabu_list.append(best_move)
            if len(tabu_list) > tabu_list_size:
                tabu_list.pop(0)

            # Update global best
            if best_neighbor_cost < best_cost:
                best_solution = best_neighbor[:]
                best_cost = best_neighbor_cost

        pool.close()
        pool.join()

        return best_solution



if __name__ == '__main__':
        problem = FlowShop(jobs=50, machines=5)
        problem.instance_from_file("50_5.txt")

        tabu = TabuSearch(problem)

        initial_solution = tabu.random_solution()
        best_solution = tabu.tabu_search(initial_solution, max_iterations=100, tabu_list_size=10)

        print("Best solution found:", best_solution)
        print("C_max:", problem.target_function(best_solution))