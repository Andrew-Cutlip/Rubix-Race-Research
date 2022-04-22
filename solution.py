import heapq as pq
from functools import reduce
import json
import operator

from board import Board


class Node:
    def __init__(self, board, previous, heuristic, depth):
        self.board = board
        self.previous = previous
        self.heuristic = heuristic
        self.depth = depth
        self.dimension = 5

    def __lt__(self, other):
        return True

    def generate_children(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0:
                    x, y = i, j
        val_list = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]
        children = []
        for child in val_list:
            if child[0] >= 0 and child[0] < len(self.board) and child[1] >= 0 and child[1] < len(self.board):
                child_board = [row[:] for row in self.board]
                child_board[x][y] = child_board[child[0]][child[1]]
                child_board[child[0]][child[1]] = 0
                child_node = Node(child_board, self, self.node_manhattan(
                    child_board), self.depth + 1)
                children.append(child_node)
        return children

    def node_manhattan(self, board):
        sum = 0
        n = len(board)
        for i in range(n):
            for j in range(n):
                x = int((board[i][j] - 1)/n)
                y = int((board[i][j] - 1) % n)
                if board[i][j] == 0:
                    continue
                sum += abs(x-i) + abs(y - j)
        return sum


class Solution:
    def __init__(self, board_colors, pattern_color) -> None:
        self.board_colors = board_colors
        self.pattern_color = pattern_color
        self.required_pattn_number = [7, 8, 9, 12, 13, 14, 15, 16, 17]
        self.mapper_coordinate = {}
        self.board = []
        for i in self.board_colors:
            self.board.append([-1] * len(i))

    def find_closest(self, current_row, current_col, color, number):
        sol = []
        for idx1, i in enumerate(self.board_colors):
            for idx2, j in enumerate(i):
                if j == color:
                    value = abs(current_row - idx1) + \
                        abs(current_col - idx2)
                    sol.append(((idx1, idx2), value))
        sol = sorted(sol, key=lambda x: x[1], reverse=True)
        while True:
            data = sol.pop()
            if self.board[data[0][0]][data[0][1]] == -1:
                self.board[data[0][0]][data[0][1]] = number
                break

    def generate_board(self):
        index = 0
        for idx1, i in enumerate(self.pattern_color):
            for idx2, j in enumerate(i):
                color = self.pattern_color[idx1][idx2]
                self.find_closest(idx1 + 1, idx2 + 1, color,
                                  self.required_pattn_number[index])
                index += 1

        for idx1, i in enumerate(self.board_colors):
            for idx2, j in enumerate(i):
                if j == 'X':
                    self.board[idx1][idx2] = 0
        remaining = list(set(range(1, 25)) - set(self.required_pattn_number))
        remaining.sort()
        counter = 1
        for idx1, i in enumerate(self.board):
            for idx2, j in enumerate(i):
                if self.board[idx1][idx2] == -1:
                    self.board[idx1][idx2] = remaining.pop(0)
                self.mapper_coordinate[self.board[idx1][idx2]] = counter
                counter += 1
        print(self.board)

    def row_col_goal_states(self, n):
        goal_states = []
        for layer in range(n-2):
            for i in range(n - layer):
                goal_states.append(set([n * layer + i + 1]))
                if len(goal_states) > 1:
                    goal_states[-1] = goal_states[-1].union(goal_states[-2])
            for i in range(n - layer - 1):
                goal_states.append(set([n+1 + i * (n)]))
                goal_states[-1] = goal_states[-1].union(goal_states[-2])
        goal_states.append(set(range(1, n*n)))
        return goal_states

    def isGoal(self, board, goal_nums):
        count = 0
        for i in range(len(board)):
            for j in range(len(board)):
                count += 1
                if count in goal_nums and board[i][j] != count:
                    return False
        return True

    def start_game(self):
        h = []
        visited = set()
        h_scale_factor = 3
        count = 1
        goal_states = self.row_col_goal_states(len(self.board_colors))
        self.generate_board()
        goal_states = self.row_col_goal_states(len(self.board_colors))
        curr_goal = 0
        root = Node(self.board, None, self.manhattan(self.board,
                                                     goal_states[curr_goal]), 0)
        pq.heappush(h, (root.depth + h_scale_factor * root.heuristic, root))
        with open("test.txt", 'w', encoding='utf-8') as f:
            while len(h) > 0:
                count += 1
                node = pq.heappop(h)[1]
                if self.isGoal(node.board, goal_states[curr_goal]):
                    print("reached goal", curr_goal, goal_states[curr_goal])
                    self.print_solution(node.board)
                    h = []
                    curr_goal += 1
                    if curr_goal == len(goal_states):
                        temp = node
                        boards = []
                        while temp != None:
                            boards.append(temp.board)
                            temp = temp.previous
                        boards.reverse()
                        for i in boards:
                            f.write(
                                " ".join(list(map(str, reduce(operator.concat, i)))))
                            f.write("\n")
                        f.write("\nMOVES FOR ROBOT \n\n")
                        list_data = []
                        for i in range(1, len(boards)):
                            initial = reduce(
                                operator.concat, boards[i-1]).index(0) + 1
                            final = reduce(operator.concat,
                                           boards[i]).index(0) + 1

                            f.write(str(initial) + " -> " + str(final))
                            f.write("\n")
                            list_data.append((initial, final))
                        Board().start(self.board_colors, self.board, list_data)
                        with open('data.json', 'w') as f:
                            json.dump(list_data, f)
                        break

                    root = Node(self.board, None, self.manhattan(
                        self.board, goal_states[curr_goal]), 0)
                    pq.heappush(
                        h, (root.depth + h_scale_factor * root.heuristic, root))

                t = tuple(reduce(operator.concat, node.board))
                visited.add(t)
                children = node.generate_children()
                for child in children:
                    t = tuple(reduce(operator.concat, child.board))
                    if t in visited:
                        continue
                    pq.heappush(h, (child.depth + h_scale_factor *
                                self.manhattan(child.board, goal_states[curr_goal]), child))

    def manhattan(self, board, goal_nums):
        sum = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] in goal_nums:
                    x = int((board[i][j] - 1)/len(board))
                    y = int((board[i][j] - 1) % len(board))
                    sum += abs(x-i) + abs(y - j)
        return sum

    def mapper(self):
        pass

    def print_solution(self, b):
        for i in b:
            for j in i:
                print(j, end=" ")
            print()


detected_color = [
    ['O', 'G', 'B', 'W', 'R'],
    ['B', 'R', 'Y', 'G', 'W'],
    ['Y', 'O', 'X', 'O', 'B'],
    ['R', 'G', 'W', 'Y', 'R'],
    ['Y', 'W', 'B', 'G', 'O']
]
solution_pattern = [
    ['B', 'G', 'W'],
    ['R', 'O', 'R'],
    ['B', 'W', 'W']
]

solution = Solution(detected_color, solution_pattern)
print(solution.start_game())
