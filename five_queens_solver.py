"""
5-Queens Problem Solver using SimpleAI Library
Implements various CSP and Local Search algorithms:
1. Backtracking with heuristics (MRV, LCV)
2. Backtracking with AC3 constraint propagation
3. Hill-Climbing
4. Simulated Annealing
5. Genetic Algorithm
"""

import random
import time
from simpleai.search import CspProblem, backtrack
from simpleai.search.csp import MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE, min_conflicts
from simpleai.search.local import hill_climbing, simulated_annealing, genetic


class FiveQueensProblem:
    """Utility class for 5-Queens problem"""
    
    def __init__(self):
        self.board_size = 5
        self.variables = list(range(5))  # Queens 0, 1, 2, 3, 4
        self.domains = {i: list(range(5)) for i in range(5)}  # Each queen can be in any row
    
    def print_board(self, assignment):
        """Print the chess board with queens"""
        if not assignment or len(assignment) != 5:
            print("Invalid assignment")
            return
            
        board = [['.' for _ in range(5)] for _ in range(5)]
        for col, row in assignment.items():
            board[row][col] = 'Q'
        
        print("\nBoard:")
        for row in board:
            print(' '.join(row))
        print()
    
    def conflicts(self, assignment):
        """Count the number of conflicts (attacking pairs)"""
        conflicts = 0
        queens = list(assignment.items())
        
        for i in range(len(queens)):
            for j in range(i + 1, len(queens)):
                col1, row1 = queens[i]
                col2, row2 = queens[j]
                
                # Same row
                if row1 == row2:
                    conflicts += 1
                # Same diagonal
                if abs(row1 - row2) == abs(col1 - col2):
                    conflicts += 1
        
        return conflicts


# 1. BACKTRACKING WITH HEURISTICS
class FiveQueensCSP(CspProblem):
    """CSP formulation for 5-Queens problem"""
    
    def __init__(self):
        variables = list(range(5))  # Queens 0, 1, 2, 3, 4
        domains = {i: list(range(5)) for i in range(5)}  # Each queen can be in any row
        
        super().__init__(variables, domains, self.constraint_function)
    
    def constraint_function(self, variables, values):
        """Check if two queens don't attack each other"""
        if len(variables) != 2:
            return True
            
        col1, col2 = variables
        row1, row2 = values
        
        # Different rows and not on the same diagonal
        return row1 != row2 and abs(row1 - row2) != abs(col1 - col2)


# Use built-in heuristics from simpleai
# MOST_CONSTRAINED_VARIABLE and LEAST_CONSTRAINING_VALUE are already imported


# 2. LOCAL SEARCH IMPLEMENTATIONS
class QueensLocalSearch:
    """Local search implementation for 5-Queens"""
    
    def __init__(self):
        self.board_size = 5
    
    def random_state(self):
        """Generate a random state (one queen per column)"""
        return tuple(random.randint(0, 4) for _ in range(5))
    
    def evaluate(self, state):
        """Evaluate state - negative conflicts (higher is better)"""
        conflicts = 0
        for i in range(5):
            for j in range(i + 1, 5):
                # Same row
                if state[i] == state[j]:
                    conflicts += 1
                # Same diagonal
                if abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return -conflicts  # Negative because we want to minimize conflicts
    
    def get_neighbors(self, state):
        """Get all neighbors by moving one queen to a different row"""
        neighbors = []
        state_list = list(state)
        
        for col in range(5):
            for new_row in range(5):
                if new_row != state[col]:
                    neighbor = state_list.copy()
                    neighbor[col] = new_row
                    neighbors.append(tuple(neighbor))
        
        return neighbors
    
    def mutate(self, state):
        """Mutate state for genetic algorithm"""
        state_list = list(state)
        col = random.randint(0, 4)
        state_list[col] = random.randint(0, 4)
        return tuple(state_list)
    
    def crossover(self, state1, state2):
        """Crossover for genetic algorithm"""
        crossover_point = random.randint(1, 3)
        child1 = state1[:crossover_point] + state2[crossover_point:]
        child2 = state2[:crossover_point] + state1[crossover_point:]
        return child1, child2


def solve_backtracking_heuristics():
    """Solve using backtracking with MRV and LCV heuristics"""
    print("=== BACKTRACKING WITH HEURISTICS (MRV + LCV) ===")
    
    problem = FiveQueensCSP()
    start_time = time.time()
    
    result = backtrack(
        problem,
        variable_heuristic=MOST_CONSTRAINED_VARIABLE,
        value_heuristic=LEAST_CONSTRAINING_VALUE,
        inference=False
    )
    
    end_time = time.time()
    
    if result:
        print(f"Solution found in {end_time - start_time:.4f} seconds")
        FiveQueensProblem().print_board(result)
        conflicts = FiveQueensProblem().conflicts(result)
        print(f"Conflicts: {conflicts}")
    else:
        print("No solution found")
    
    return result


def solve_min_conflicts():
    """Solve using Min-Conflicts algorithm (CSP constraint propagation alternative)"""
    print("=== MIN-CONFLICTS (CSP CONSTRAINT PROPAGATION) ===")
    
    problem = FiveQueensCSP()
    start_time = time.time()
    
    result = min_conflicts(problem, iterations_limit=1000)
    
    end_time = time.time()
    
    if result:
        print(f"Solution found in {end_time - start_time:.4f} seconds")
        FiveQueensProblem().print_board(result)
        conflicts = FiveQueensProblem().conflicts(result)
        print(f"Conflicts: {conflicts}")
    else:
        print("No solution found")
    
    return result


def solve_hill_climbing():
    """Solve using Hill-Climbing"""
    print("=== HILL-CLIMBING ===")
    
    searcher = QueensLocalSearch()
    start_time = time.time()
    
    # Try multiple random starts
    best_result = None
    best_value = float('-inf')
    
    for _ in range(10):
        initial_state = searcher.random_state()
        result = hill_climbing(
            initial_state,
            searcher.get_neighbors,
            searcher.evaluate
        )
        
        value = searcher.evaluate(result.state)
        if value > best_value:
            best_value = value
            best_result = result
    
    end_time = time.time()
    
    if best_result:
        print(f"Best solution found in {end_time - start_time:.4f} seconds")
        assignment = {i: best_result.state[i] for i in range(5)}
        FiveQueensProblem().print_board(assignment)
        conflicts = FiveQueensProblem().conflicts(assignment)
        print(f"Conflicts: {conflicts}")
        print(f"Evaluation score: {best_value}")
    
    return best_result


def solve_simulated_annealing():
    """Solve using Simulated Annealing"""
    print("=== SIMULATED ANNEALING ===")
    
    searcher = QueensLocalSearch()
    start_time = time.time()
    
    initial_state = searcher.random_state()
    
    def temperature_function(time_step):
        return max(0.01, 100 * (0.95 ** time_step))
    
    result = simulated_annealing(
        initial_state,
        searcher.get_neighbors,
        searcher.evaluate,
        temperature_function,
        iterations_limit=1000
    )
    
    end_time = time.time()
    
    if result:
        print(f"Solution found in {end_time - start_time:.4f} seconds")
        assignment = {i: result.state[i] for i in range(5)}
        FiveQueensProblem().print_board(assignment)
        conflicts = FiveQueensProblem().conflicts(assignment)
        print(f"Conflicts: {conflicts}")
        print(f"Evaluation score: {searcher.evaluate(result.state)}")
    
    return result


def solve_genetic_algorithm():
    """Solve using Genetic Algorithm"""
    print("=== GENETIC ALGORITHM ===")
    
    searcher = QueensLocalSearch()
    start_time = time.time()
    
    # Generate initial population
    population_size = 50
    initial_population = [searcher.random_state() for _ in range(population_size)]
    
    def mutation_function(individual):
        return searcher.mutate(individual)
    
    def crossover_function(parent1, parent2):
        return searcher.crossover(parent1, parent2)
    
    result = genetic(
        initial_population,
        searcher.evaluate,
        mutation_function,
        crossover_function,
        population_size=population_size,
        iterations_limit=100
    )
    
    end_time = time.time()
    
    if result:
        print(f"Solution found in {end_time - start_time:.4f} seconds")
        assignment = {i: result.state[i] for i in range(5)}
        FiveQueensProblem().print_board(assignment)
        conflicts = FiveQueensProblem().conflicts(assignment)
        print(f"Conflicts: {conflicts}")
        print(f"Evaluation score: {searcher.evaluate(result.state)}")
    
    return result


def show_menu():
    """Display the menu and get user choice"""
    print("\n5-Queens Problem Solver")
    print("=" * 50)
    print("Choose an algorithm:")
    print("1. Backtracking with Heuristics (MRV + LCV)")
    print("2. Min-Conflicts (CSP Constraint Propagation)")
    print("3. Hill-Climbing Local Search")
    print("4. Simulated Annealing")
    print("5. Genetic Algorithm")
    print("6. Run All Algorithms and Compare")
    print("0. Exit")
    print("-" * 50)
    
    while True:
        try:
            choice = input("Enter your choice (0-6): ").strip()
            if choice in ['0', '1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print("Invalid choice. Please enter a number between 0 and 6.")
        except KeyboardInterrupt:
            print("\nExiting...")
            return '0'
        except Exception:
            print("Invalid input. Please enter a number between 0 and 6.")


def run_all_algorithms():
    """Run all algorithms and compare results"""
    print("\nRunning all algorithms...")
    print("=" * 50)
    
    algorithms = [
        ("Backtracking with Heuristics", solve_backtracking_heuristics),
        ("Min-Conflicts", solve_min_conflicts),
        ("Hill-Climbing", solve_hill_climbing),
        ("Simulated Annealing", solve_simulated_annealing),
        ("Genetic Algorithm", solve_genetic_algorithm)
    ]
    
    results = {}
    
    for name, solver in algorithms:
        print(f"\n{name}")
        print("-" * 30)
        try:
            result = solver()
            results[name] = result
        except Exception as e:
            print(f"Error in {name}: {e}")
            results[name] = None
        print()
    
    print("=" * 50)
    print("SUMMARY:")
    for name, result in results.items():
        if result:
            if hasattr(result, 'state'):
                assignment = {i: result.state[i] for i in range(5)}
            else:
                assignment = result
            conflicts = FiveQueensProblem().conflicts(assignment)
            print(f"{name}: {'SUCCESS' if conflicts == 0 else 'PARTIAL'} (conflicts: {conflicts})")
        else:
            print(f"{name}: FAILED")


def main():
    """Main function with interactive menu"""
    algorithms = {
        '1': ("Backtracking with Heuristics", solve_backtracking_heuristics),
        '2': ("Min-Conflicts", solve_min_conflicts),
        '3': ("Hill-Climbing", solve_hill_climbing),
        '4': ("Simulated Annealing", solve_simulated_annealing),
        '5': ("Genetic Algorithm", solve_genetic_algorithm),
        '6': ("Run All Algorithms", run_all_algorithms)
    }
    
    while True:
        choice = show_menu()
        
        if choice == '0':
            print("Thank you for using 5-Queens Problem Solver!")
            break
        elif choice == '6':
            run_all_algorithms()
        elif choice in algorithms:
            name, solver = algorithms[choice]
            print(f"\nRunning {name}...")
            print("-" * 40)
            try:
                solver()
            except Exception as e:
                print(f"Error: {e}")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()