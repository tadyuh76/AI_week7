# 5-Queens Problem Solver

This project implements various Constraint Satisfaction Problem (CSP) and Local Search algorithms to solve the 5-Queens problem using the SimpleAI library.

## Problem Description

The 5-Queens problem is a variant of the famous N-Queens problem where you must place 5 queens on a 5×5 chessboard such that no two queens attack each other (same row, column, or diagonal).

## Implemented Algorithms

### CSP Algorithms
1. **Backtracking with Heuristics** - Uses MRV (Most Constrained Variable) and LCV (Least Constraining Value) heuristics
2. **Min-Conflicts** - CSP constraint propagation algorithm that efficiently resolves conflicts

### Local Search Algorithms
3. **Hill-Climbing** - Local search with multiple random restarts to avoid local optima
4. **Simulated Annealing** - Probabilistic optimization with temperature scheduling
5. **Genetic Algorithm (Hybrid)** - Enhanced evolutionary algorithm with genetic operators plus local search optimization for improved solution quality

## Requirements

```bash
pip install simpleai
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

## Usage

Run the interactive solver:
```bash
python five_queens_solver.py
```

### Menu Options

- **Option 1**: Run Backtracking with Heuristics
- **Option 2**: Run Min-Conflicts algorithm
- **Option 3**: Run Hill-Climbing search
- **Option 4**: Run Simulated Annealing
- **Option 5**: Run Genetic Algorithm
- **Option 6**: Run all algorithms and compare results
- **Option 0**: Exit

## Example Output

```
5-Queens Problem Solver
==================================================
Choose an algorithm:
1. Backtracking with Heuristics (MRV + LCV)
2. Min-Conflicts (CSP Constraint Propagation)
3. Hill-Climbing Local Search
4. Simulated Annealing
5. Genetic Algorithm
6. Run All Algorithms and Compare
0. Exit
--------------------------------------------------
Enter your choice (0-6): 1

Running Backtracking with Heuristics...
----------------------------------------
=== BACKTRACKING WITH HEURISTICS (MRV + LCV) ===
Solution found in 0.0008 seconds

Board:
Q . . . .
. . . Q .
. Q . . .
. . . . Q
. . Q . .

Conflicts: 0
```

## Algorithm Performance

- **Backtracking algorithms** (options 1-2) typically find optimal solutions very quickly (<0.001s)
- **Hill-Climbing** often finds good solutions and frequently achieves optimal results with multiple restarts
- **Simulated Annealing** can escape local optima and consistently finds optimal solutions
- **Genetic Algorithm (Hybrid)** combines evolutionary search with local optimization to consistently find perfect solutions, though it takes longer (0.1-0.5s)

## Implementation Details

### CSP Formulation
- **Variables**: Queen positions (columns 0-4)
- **Domain**: Possible rows for each queen (0-4)
- **Constraints**: No two queens on same row or diagonal

### Local Search Formulation
- **State**: Tuple representing row position of each queen
- **Actions**: Move one queen to a different row
- **Evaluation**: Negative number of conflicts (higher is better)

## Files

- `five_queens_solver.py` - Main solver with interactive menu
- `requirements.txt` - Python dependencies
- `README.md` - This documentation file

## Note

The 5-Queens problem has valid solutions, and the CSP algorithms (Backtracking and Min-Conflicts) will consistently find them. Local search algorithms may find partial solutions with some conflicts remaining, which is normal behavior for these heuristic approaches.