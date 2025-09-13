"""
5-Queens Problem Solver using SimpleAI Library
Implements various CSP and Local Search algorithms:
1. Backtracking with heuristics (MRV, LCV)
2. Min-Conflicts constraint propagation
3. Hill-Climbing
4. Simulated Annealing
5. Genetic Algorithm
"""

import random
import time
from simpleai.search import CspProblem, backtrack, SearchProblem
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
        
        if isinstance(assignment, dict):
            for col, row in assignment.items():
                board[row][col] = 'Q'
        elif isinstance(assignment, (list, tuple)):
            for col, row in enumerate(assignment):
                board[row][col] = 'Q'
        
        print("\nBoard:")
        for row in board:
            print(' '.join(row))
        print()
    
    def conflicts(self, assignment):
        """Count the number of conflicts (attacking pairs)"""
        conflicts = 0
        
        if isinstance(assignment, dict):
            queens = list(assignment.items())
        elif isinstance(assignment, (list, tuple)):
            queens = list(enumerate(assignment))
        else:
            return 0
        
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
        
        # Create constraints for all pairs of variables
        constraints = []
        for i in range(5):
            for j in range(i + 1, 5):
                constraints.append(((i, j), self.constraint_function))
        
        super().__init__(variables, domains, constraints)
    
    def constraint_function(self, variables, values):
        """Check if two queens don't attack each other"""
        col1, col2 = variables
        row1, row2 = values
        
        # Different rows and not on the same diagonal
        return row1 != row2 and abs(row1 - row2) != abs(col1 - col2)


# 2. LOCAL SEARCH IMPLEMENTATIONS
class QueensSearchProblem(SearchProblem):
    """Search problem for local search algorithms"""
    
    def __init__(self):
        # Initial state: random placement of queens
        initial_state = tuple(random.randint(0, 4) for _ in range(5))
        super().__init__(initial_state)
    
    def actions(self, state):
        """Get all possible actions (moving one queen to a different row)"""
        actions = []
        for col in range(5):
            for new_row in range(5):
                if new_row != state[col]:
                    actions.append((col, new_row))
        return actions
    
    def result(self, state, action):
        """Apply action to state"""
        col, new_row = action
        new_state = list(state)
        new_state[col] = new_row
        return tuple(new_state)
    
    def value(self, state):
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
    
    def generate_random_state(self):
        """Generate a random state for genetic algorithm"""
        return tuple(random.randint(0, 4) for _ in range(5))
    
    def crossover(self, state1, state2):
        """Improved crossover for genetic algorithm"""
        # Use multiple crossover points for better mixing
        child = list(state1)
        
        # Randomly select positions to inherit from parent2
        for i in range(5):
            if random.random() < 0.5:  # 50% chance to take from parent2
                child[i] = state2[i]
        
        return tuple(child)
    
    def mutate(self, state):
        """Improved mutation for genetic algorithm"""
        state_list = list(state)
        
        # Higher chance of mutation with intelligent selection
        # Mutate 1-2 queens per mutation
        num_mutations = random.randint(1, 2)
        
        for _ in range(num_mutations):
            col = random.randint(0, 4)
            # Avoid placing in the same row (slight bias toward better moves)
            old_row = state_list[col]
            new_row = random.randint(0, 4)
            
            # Try to avoid same row with some probability
            if new_row == old_row and random.random() < 0.7:
                new_row = (new_row + random.randint(1, 4)) % 5
            
            state_list[col] = new_row
        
        return tuple(state_list)


def solve_backtracking_heuristics():
    """Solve using backtracking with MRV and LCV heuristics"""
    print("=== BACKTRACKING WITH HEURISTICS (MRV + LCV) ===")
    
    problem = FiveQueensCSP()
    start_time = time.time()
    
    result = backtrack(
        problem,
        variable_heuristic=MOST_CONSTRAINED_VARIABLE,
        value_heuristic=LEAST_CONSTRAINING_VALUE
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
    """Solve using Min-Conflicts algorithm"""
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
    
    start_time = time.time()
    
    # Try multiple random starts
    best_result = None
    best_value = float('-inf')
    
    for _ in range(10):
        problem = QueensSearchProblem()
        result = hill_climbing(problem, iterations_limit=1000)
        
        if result and hasattr(result, 'state'):
            value = problem.value(result.state)
            if value > best_value:
                best_value = value
                best_result = result
    
    end_time = time.time()
    
    if best_result and hasattr(best_result, 'state'):
        print(f"Best solution found in {end_time - start_time:.4f} seconds")
        FiveQueensProblem().print_board(best_result.state)
        conflicts = FiveQueensProblem().conflicts(best_result.state)
        print(f"Conflicts: {conflicts}")
        print(f"Evaluation score: {best_value}")
    else:
        print("No solution found")
    
    return best_result


def solve_simulated_annealing():
    """Solve using Simulated Annealing"""
    print("=== SIMULATED ANNEALING ===")
    
    problem = QueensSearchProblem()
    start_time = time.time()
    
    def temperature_schedule(time_step):
        return max(0.01, 100 * (0.95 ** time_step))
    
    result = simulated_annealing(
        problem,
        schedule=temperature_schedule,
        iterations_limit=1000
    )
    
    end_time = time.time()
    
    if result and hasattr(result, 'state'):
        print(f"Solution found in {end_time - start_time:.4f} seconds")
        FiveQueensProblem().print_board(result.state)
        conflicts = FiveQueensProblem().conflicts(result.state)
        print(f"Conflicts: {conflicts}")
        print(f"Evaluation score: {problem.value(result.state)}")
    else:
        print("No solution found")
    
    return result


def local_improve_solution(state):
    """Apply local improvements to a genetic algorithm solution"""
    current_state = list(state)
    improved = True
    
    while improved:
        improved = False
        current_conflicts = FiveQueensProblem().conflicts(current_state)
        
        # Try moving each queen to a better position
        for col in range(5):
            original_row = current_state[col]
            best_row = original_row
            best_conflicts = current_conflicts
            
            # Try all possible rows for this column
            for new_row in range(5):
                if new_row != original_row:
                    current_state[col] = new_row
                    conflicts = FiveQueensProblem().conflicts(current_state)
                    
                    if conflicts < best_conflicts:
                        best_conflicts = conflicts
                        best_row = new_row
            
            # Keep the best position found
            current_state[col] = best_row
            if best_conflicts < current_conflicts:
                improved = True
                if best_conflicts == 0:  # Perfect solution found
                    break
    
    return tuple(current_state)


def solve_genetic_algorithm():
    """Solve using Hybrid Genetic Algorithm with Local Improvement"""
    print("=== GENETIC ALGORITHM (HYBRID WITH LOCAL SEARCH) ===")
    
    start_time = time.time()
    
    # Try multiple runs with different parameters
    best_result = None
    best_conflicts = float('inf')
    
    attempts = 3  # Reduced attempts since we're using local improvement
    for attempt in range(attempts):
        problem = QueensSearchProblem()
        
        # Vary parameters across attempts
        population_size = 80 + (attempt * 40)   # 80, 120, 160
        iterations = 150 + (attempt * 50)       # 150, 200, 250
        
        result = genetic(problem, population_size=population_size, iterations_limit=iterations)
        
        if result and hasattr(result, 'state'):
            # Apply local improvement to the genetic result
            improved_state = local_improve_solution(result.state)
            conflicts = FiveQueensProblem().conflicts(improved_state)
            
            if conflicts < best_conflicts:
                best_conflicts = conflicts
                # Create a result-like object with improved state
                class ImprovedResult:
                    def __init__(self, state):
                        self.state = state
                best_result = ImprovedResult(improved_state)
                
                # If we found a perfect solution, stop early
                if conflicts == 0:
                    print(f"Perfect solution found on attempt {attempt + 1}")
                    break
    
    end_time = time.time()
    
    if best_result and hasattr(best_result, 'state'):
        print(f"Best solution found in {end_time - start_time:.4f} seconds")
        FiveQueensProblem().print_board(best_result.state)
        print(f"Conflicts: {best_conflicts}")
        
        if best_conflicts == 0:
            print("✓ Perfect solution achieved!")
            print("Algorithm: Genetic Algorithm + Local Search optimization")
        else:
            print(f"⚠ Partial solution with {best_conflicts} conflicts")
    else:
        print("No solution found")
    
    return best_result


def show_menu():
    """Display the menu and get user choice"""
    print("\n5-Queens Problem Solver")
    print("=" * 50)
    print("Choose an algorithm:")
    print("1. Backtracking with Heuristics (MRV + LCV)")
    print("2. Min-Conflicts (CSP Constraint Propagation)")
    print("3. Hill-Climbing Local Search")
    print("4. Simulated Annealing")
    print("5. Genetic Algorithm (Hybrid with Local Search)")
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
                assignment = result.state
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