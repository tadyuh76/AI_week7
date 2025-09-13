"""
Bài toán 5 Hậu sử dụng thư viện SimpleAI
Triển khai các thuật toán CSP và Tìm kiếm Cục bộ:
1. Backtracking với heuristics (MRV, LCV)
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
    """Lớp tiện ích cho bài toán 5 Hậu"""
    
    def __init__(self):
        self.board_size = 5
        self.variables = list(range(5))  # Các hậu 0, 1, 2, 3, 4
        self.domains = {i: list(range(5)) for i in range(5)}  # Mỗi hậu có thể ở bất kỳ hàng nào
    
    def print_board(self, assignment):
        """In bàn cờ với các quân hậu"""
        if not assignment or len(assignment) != 5:
            print("Phân bổ không hợp lệ")
            return
            
        board = [['.' for _ in range(5)] for _ in range(5)]
        
        if isinstance(assignment, dict):
            for col, row in assignment.items():
                board[row][col] = 'Q'
        elif isinstance(assignment, (list, tuple)):
            for col, row in enumerate(assignment):
                board[row][col] = 'Q'
        
        print("\nBàn cờ:")
        for row in board:
            print(' '.join(row))
        print()
    
    def conflicts(self, assignment):
        """Đếm số lượng xung đột (cặp hậu tấn công nhau)"""
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
                
                # Cùng hàng
                if row1 == row2:
                    conflicts += 1
                # Cùng đường chéo
                if abs(row1 - row2) == abs(col1 - col2):
                    conflicts += 1
        
        return conflicts


# 1. BACKTRACKING VỚI HEURISTICS
class FiveQueensCSP(CspProblem):
    """Công thức CSP cho bài toán 5 Hậu"""
    
    def __init__(self):
        variables = list(range(5))  # Các hậu 0, 1, 2, 3, 4
        domains = {i: list(range(5)) for i in range(5)}  # Mỗi hậu có thể ở bất kỳ hàng nào
        
        # Tạo ràng buộc cho tất cả cặp biến
        constraints = []
        for i in range(5):
            for j in range(i + 1, 5):
                constraints.append(((i, j), self.constraint_function))
        
        super().__init__(variables, domains, constraints)
    
    def constraint_function(self, variables, values):
        """Kiểm tra nếu hai quân hậu không tấn công nhau"""
        col1, col2 = variables
        row1, row2 = values
        
        # Khác hàng và không cùng đường chéo
        return row1 != row2 and abs(row1 - row2) != abs(col1 - col2)


# 2. TRIỂN KHAI TÌM KIẾM CỤC BỘ
class QueensSearchProblem(SearchProblem):
    """Bài toán tìm kiếm cho các thuật toán tìm kiếm cục bộ"""
    
    def __init__(self):
        # Trạng thái ban đầu: đặt hậu ngẫu nhiên
        initial_state = tuple(random.randint(0, 4) for _ in range(5))
        super().__init__(initial_state)
    
    def actions(self, state):
        """Lấy tất cả hành động có thể (di chuyển một hậu đến hàng khác)"""
        actions = []
        for col in range(5):
            for new_row in range(5):
                if new_row != state[col]:
                    actions.append((col, new_row))
        return actions
    
    def result(self, state, action):
        """Thực hiện hành động lên trạng thái"""
        col, new_row = action
        new_state = list(state)
        new_state[col] = new_row
        return tuple(new_state)
    
    def value(self, state):
        """Đánh giá trạng thái - xung đột âm (cao hơn là tốt hơn)"""
        conflicts = 0
        for i in range(5):
            for j in range(i + 1, 5):
                # Cùng hàng
                if state[i] == state[j]:
                    conflicts += 1
                # Cùng đường chéo
                if abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return -conflicts  # Âm vì chúng ta muốn giảm thiểu xung đột
    
    def generate_random_state(self):
        """Tạo trạng thái ngẫu nhiên cho thuật toán di truyền"""
        return tuple(random.randint(0, 4) for _ in range(5))
    
    def crossover(self, state1, state2):
        """Lai ghép cải tiến cho thuật toán di truyền"""
        # Sử dụng nhiều điểm lai ghép để trộn tốt hơn
        child = list(state1)
        
        # Chọn ngẫu nhiên vị trí kế thừa từ cha mẹ 2
        for i in range(5):
            if random.random() < 0.5:  # 50% cơ hội lấy từ cha mẹ 2
                child[i] = state2[i]
        
        return tuple(child)
    
    def mutate(self, state):
        """Biến đổi cải tiến cho thuật toán di truyền"""
        state_list = list(state)
        
        # Cơ hội biến đổi cao hơn với lựa chọn thông minh
        # Biến đổi 1-2 hậu mỗi lần
        num_mutations = random.randint(1, 2)
        
        for _ in range(num_mutations):
            col = random.randint(0, 4)
            # Tránh đặt ở cùng hàng (thiên vị hơi về nước đi tốt hơn)
            old_row = state_list[col]
            new_row = random.randint(0, 4)
            
            # Thử tránh cùng hàng với một xác suất nào đó
            if new_row == old_row and random.random() < 0.7:
                new_row = (new_row + random.randint(1, 4)) % 5
            
            state_list[col] = new_row
        
        return tuple(state_list)


def solve_backtracking_heuristics():
    """Giải bằng backtracking với heuristics MRV và LCV"""
    print("=== BACKTRACKING VỚI HEURISTICS (MRV + LCV) ===")
    
    problem = FiveQueensCSP()
    start_time = time.time()
    
    result = backtrack(
        problem,
        variable_heuristic=MOST_CONSTRAINED_VARIABLE,
        value_heuristic=LEAST_CONSTRAINING_VALUE
    )
    
    end_time = time.time()
    
    if result:
        print(f"Tìm được nghiệm trong {end_time - start_time:.4f} giây")
        FiveQueensProblem().print_board(result)
        conflicts = FiveQueensProblem().conflicts(result)
        print(f"Xung đột: {conflicts}")
    else:
        print("Không tìm được nghiệm")
    
    return result


def solve_min_conflicts():
    """Giải bằng thuật toán Min-Conflicts"""
    print("=== MIN-CONFLICTS (CSP CONSTRAINT PROPAGATION) ===")
    
    problem = FiveQueensCSP()
    start_time = time.time()
    
    result = min_conflicts(problem, iterations_limit=1000)
    
    end_time = time.time()
    
    if result:
        print(f"Tìm được nghiệm trong {end_time - start_time:.4f} giây")
        FiveQueensProblem().print_board(result)
        conflicts = FiveQueensProblem().conflicts(result)
        print(f"Xung đột: {conflicts}")
    else:
        print("Không tìm được nghiệm")
    
    return result


def solve_hill_climbing():
    """Giải bằng thuật toán Hill-Climbing"""
    print("=== LEO ĐỒI (HILL-CLIMBING) ===")
    
    start_time = time.time()
    
    # Thử nhiều khởi đầu ngẫu nhiên
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
        print(f"Nghiệm tốt nhất tìm được trong {end_time - start_time:.4f} giây")
        FiveQueensProblem().print_board(best_result.state)
        conflicts = FiveQueensProblem().conflicts(best_result.state)
        print(f"Xung đột: {conflicts}")
        print(f"Điểm đánh giá: {best_value}")
    else:
        print("Không tìm được nghiệm")
    
    return best_result


def solve_simulated_annealing():
    """Giải bằng thuật toán Simulated Annealing"""
    print("=== MÔ PHỎNG LUYỆN KIM (SIMULATED ANNEALING) ===")
    
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
        print(f"Tìm được nghiệm trong {end_time - start_time:.4f} giây")
        FiveQueensProblem().print_board(result.state)
        conflicts = FiveQueensProblem().conflicts(result.state)
        print(f"Xung đột: {conflicts}")
        print(f"Điểm đánh giá: {problem.value(result.state)}")
    else:
        print("Không tìm được nghiệm")
    
    return result


def local_improve_solution(state):
    """Thực hiện cải tiến cục bộ cho nghiệm thuật toán di truyền"""
    current_state = list(state)
    improved = True
    
    while improved:
        improved = False
        current_conflicts = FiveQueensProblem().conflicts(current_state)
        
        # Thử di chuyển mỗi quân hậu đến vị trí tốt hơn
        for col in range(5):
            original_row = current_state[col]
            best_row = original_row
            best_conflicts = current_conflicts
            
            # Thử tất cả hàng có thể cho cột này
            for new_row in range(5):
                if new_row != original_row:
                    current_state[col] = new_row
                    conflicts = FiveQueensProblem().conflicts(current_state)
                    
                    if conflicts < best_conflicts:
                        best_conflicts = conflicts
                        best_row = new_row
            
            # Giữ vị trí tốt nhất tìm được
            current_state[col] = best_row
            if best_conflicts < current_conflicts:
                improved = True
                if best_conflicts == 0:  # Tìm được nghiệm hoàn hảo
                    break
    
    return tuple(current_state)


def solve_genetic_algorithm():
    """Giải bằng Thuật toán Di truyền Lai ghép với Cải tiến Cục bộ"""
    print("=== THUẬT TOÁN DI TRUYỀN (LAI GHÉP VỚI TÌM KIẾM CỤC BỘ) ===")
    
    start_time = time.time()
    
    # Thử nhiều lần chạy với tham số khác nhau
    best_result = None
    best_conflicts = float('inf')
    
    attempts = 3  # Giảm số lần thử vì đang sử dụng cải tiến cục bộ
    for attempt in range(attempts):
        problem = QueensSearchProblem()
        
        # Thay đổi tham số qua các lần thử
        population_size = 80 + (attempt * 40)   # 80, 120, 160
        iterations = 150 + (attempt * 50)       # 150, 200, 250
        
        result = genetic(problem, population_size=population_size, iterations_limit=iterations)
        
        if result and hasattr(result, 'state'):
            # Áp dụng cải tiến cục bộ cho kết quả di truyền
            improved_state = local_improve_solution(result.state)
            conflicts = FiveQueensProblem().conflicts(improved_state)
            
            if conflicts < best_conflicts:
                best_conflicts = conflicts
                # Tạo đối tượng kết quả với trạng thái cải tiến
                class ImprovedResult:
                    def __init__(self, state):
                        self.state = state
                best_result = ImprovedResult(improved_state)
                
                # Nếu tìm được nghiệm hoàn hảo, dừng sớm
                if conflicts == 0:
                    print(f"Tìm được nghiệm hoàn hảo ở lần thử {attempt + 1}")
                    break
    
    end_time = time.time()
    
    if best_result and hasattr(best_result, 'state'):
        print(f"Nghiệm tốt nhất tìm được trong {end_time - start_time:.4f} giây")
        FiveQueensProblem().print_board(best_result.state)
        print(f"Xung đột: {best_conflicts}")
        
        if best_conflicts == 0:
            print("✓ Đạt được nghiệm hoàn hảo!")
            print("Thuật toán: Thuật toán Di truyền + Tối ưu hóa Tìm kiếm Cục bộ")
        else:
            print(f"⚠ Nghiệm không hoàn hảo với {best_conflicts} xung đột")
    else:
        print("Không tìm được nghiệm")
    
    return best_result


def show_menu():
    """Hiển thị menu và lấy lựa chọn của người dùng"""
    print("\nCông cụ Giải bài toán 5 Hậu")
    print("=" * 50)
    print("Chọn thuật toán:")
    print("1. Backtracking với Heuristics (MRV + LCV)")
    print("2. Min-Conflicts (CSP Constraint Propagation)")
    print("3. Tìm kiếm Cục bộ Leo đồi")
    print("4. Mô phỏng Luyện kim")
    print("5. Thuật toán Di truyền (Lai ghép với Tìm kiếm Cục bộ)")
    print("6. Chạy Tất cả Thuật toán và So sánh")
    print("0. Thoát")
    print("-" * 50)
    
    while True:
        try:
            choice = input("Nhập lựa chọn của bạn (0-6): ").strip()
            if choice in ['0', '1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print("Lựa chọn không hợp lệ. Vui lòng nhập số từ 0 đến 6.")
        except KeyboardInterrupt:
            print("\nĐang thoát...")
            return '0'
        except Exception:
            print("Dữ liệu đầu vào không hợp lệ. Vui lòng nhập số từ 0 đến 6.")


def run_all_algorithms():
    """Chạy tất cả thuật toán và so sánh kết quả"""
    print("\nĐang chạy tất cả thuật toán...")
    print("=" * 50)
    
    algorithms = [
        ("Backtracking với Heuristics", solve_backtracking_heuristics),
        ("Min-Conflicts", solve_min_conflicts),
        ("Leo đồi", solve_hill_climbing),
        ("Mô phỏng Luyện kim", solve_simulated_annealing),
        ("Thuật toán Di truyền", solve_genetic_algorithm)
    ]
    
    results = {}
    
    for name, solver in algorithms:
        print(f"\n{name}")
        print("-" * 30)
        try:
            result = solver()
            results[name] = result
        except Exception as e:
            print(f"Lỗi trong {name}: {e}")
            results[name] = None
        print()
    
    print("=" * 50)
    print("TÓM TẮT:")
    for name, result in results.items():
        if result:
            if hasattr(result, 'state'):
                assignment = result.state
            else:
                assignment = result
            conflicts = FiveQueensProblem().conflicts(assignment)
            print(f"{name}: {'THÀNH CÔNG' if conflicts == 0 else 'KHÔNG HOÀN HẢO'} (xung đột: {conflicts})")
        else:
            print(f"{name}: THẤT BẠI")


def main():
    """Hàm chính với menu tương tác"""
    algorithms = {
        '1': ("Backtracking với Heuristics", solve_backtracking_heuristics),
        '2': ("Min-Conflicts", solve_min_conflicts),
        '3': ("Leo đồi", solve_hill_climbing),
        '4': ("Mô phỏng Luyện kim", solve_simulated_annealing),
        '5': ("Thuật toán Di truyền", solve_genetic_algorithm),
        '6': ("Chạy Tất cả Thuật toán", run_all_algorithms)
    }
    
    while True:
        choice = show_menu()
        
        if choice == '0':
            print("Cảm ơn bạn đã sử dụng Công cụ Giải bài toán 5 Hậu!")
            break
        elif choice == '6':
            run_all_algorithms()
        elif choice in algorithms:
            name, solver = algorithms[choice]
            print(f"\nĐang chạy {name}...")
            print("-" * 40)
            try:
                solver()
            except Exception as e:
                print(f"Lỗi: {e}")
        
        input("\nNhấn Enter để tiếp tục...")


if __name__ == "__main__":
    main()