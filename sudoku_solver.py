from typing import List
from itertools import product

class Sudoku:
    def __init__(self, puzzle: List[List[int]]):
        if len(puzzle) != 9:
            raise ValueError(f'\'puzzle\' must have 9 rows, got {len(puzzle)}')
        if not all([len(row) == 9 for row in puzzle]):
            raise ValueError(f'\'puzzle\' must have cols of 9 cells')
        self.puzzle = puzzle

    def _flatten(self, l: List[List]) -> List:
        return [item for sublist in l for item in sublist]

    def get_row(self, index: int) -> List[int]:
        return self.puzzle[index]

    def get_col(self, index: int) -> List[int]:
        cells = self._flatten(self.puzzle)
        return cells[index:9*9:9]

    def get_square(self, row_index: int, col_index: int) -> List[int]:
        row_index = row_index-row_index%3
        col_index = col_index-col_index%3
        square = self.puzzle[row_index][col_index:col_index+3]
        square += self.puzzle[row_index+1][col_index:col_index+3]
        square += self.puzzle[row_index+2][col_index:col_index+3]
        return square

    def is_complete(self) -> bool:
        return all([cell != 0 for cell in self._flatten(self.puzzle)])

    def is_solved(self) -> bool:
        solved = True
        digits = [1,2,3,4,5,6,7,8,9]
        for row in self.puzzle:
            solved &= sorted(row) == digits

        cells = self._flatten(self.puzzle)
        for i in range(0, len(digits)):
            col = cells[i:len(digits)*len(digits):len(digits)]
            solved &= sorted(col) == digits

        for i,j in product(range(3), repeat=2):
            sub_puzzle = self.puzzle[i*3][j*3:j*3+3]
            sub_puzzle += self.puzzle[i*3+1][j*3:j*3+3]
            sub_puzzle += self.puzzle[i*3+2][j*3:j*3+3]
            solved &= sorted(sub_puzzle) == digits

        return solved

    def solve(self) -> bool:
        for row, col in product(range(0,9), repeat=2):
            if self.puzzle[row][col] == 0:
                for num in range(1,10):
                    allowed = self.validate_num(num, row, col)
                    if allowed:
                        self.puzzle[row][col] = num
                        if attempt := self.solve():
                            return attempt
                        else:
                            self.puzzle[row][col] = 0
                return False
        return self

    def validate_num(self, num: int, row_index: int, col_index: int) -> bool:
        exists_in_row = num in self.get_row(row_index) 
        exists_in_col = num in self.get_col(col_index)
        exists_in_square = num in self.get_square(row_index, col_index)
        return not (exists_in_row or exists_in_col or exists_in_square)

    def __str__(self):
        string = ""
        for row in range(0,9):
            if row!=0 and row%3==0:
                string += '-'*6 + '+' + '-'*7 + '+' + '-'*6 + '\n'
            for col in range(0,9):
                if col!=0 and col%3==0:
                    string += '| '
                string += str(puzzle[row][col]) + ' '
                if col==8:
                    string += '\n'
        return string


if __name__ == "__main__":
    puzzle = [[5,3,0,0,7,0,0,0,0],
              [6,0,0,1,9,5,0,0,0],
              [0,9,8,0,0,0,0,6,0],
              [8,0,0,0,6,0,0,0,3],
              [4,0,0,8,0,3,0,0,1],
              [7,0,0,0,2,0,0,0,6],
              [0,6,0,0,0,0,2,8,0],
              [0,0,0,4,1,9,0,0,5],
              [0,0,0,0,8,0,0,7,9]]

    solution = [[5,3,4,6,7,8,9,1,2],
                [6,7,2,1,9,5,3,4,8],
                [1,9,8,3,4,2,5,6,7],
                [8,5,9,7,6,1,4,2,3],
                [4,2,6,8,5,3,7,9,1],
                [7,1,3,9,2,4,8,5,6],
                [9,6,1,5,3,7,2,8,4],
                [2,8,7,4,1,9,6,3,5],
                [3,4,5,2,8,6,1,7,9]]

    sudoku = Sudoku(puzzle)
    print(sudoku, sudoku.is_complete(), sudoku.is_solved())
    print(sudoku.solve(), sudoku.is_complete(), sudoku.is_solved())