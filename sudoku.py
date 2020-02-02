SUDOKU_SQUARE_LENGTH = 3
SUDOKU_LENGHT = 9


class Cell(object):
    def __init__(self, row, col, static, number=None):
        self.row = row
        self.col = col
        self.position = row * SUDOKU_LENGHT + col
        self.static = static
        self.number = number if static else 0
        self.numbers = None if static else list(range(1, 10))
        self.numberidx = None
        self.square = (row // SUDOKU_SQUARE_LENGTH,
                       col // SUDOKU_SQUARE_LENGTH)

    def get_number(self):
        _number = 0
        if self.static:
            _number = self.number
        else:
            try:
                _number = self.numbers[self.numberidx] if (
                    self.numberidx is not None) else 0
            except:
                raise Exception(f'BT for Cell({self.row, self.col}')
        return _number

    def __repr__(self):
        return f'Cell({self.row, self.col, self.get_number()})'

    def reset(self):
        if self.static == False:
            self.numberidx = None

    def update_numbers(self, pcell):
        if pcell.static:
            if pcell.get_number() in self.numbers:
                self.numbers.remove(pcell.get_number())
        else:
            if self.numberidx is None:  # Initialisation
                self.numberidx = 0
            if pcell.numberidx is not None:
                if pcell.get_number() == self.get_number():
                    self.nextnumberidx()

    def nextnumberidx(self):
        self.numberidx += 1


class Sudoku(object):

    length = SUDOKU_LENGHT

    def __init__(self, cells=[]):
        self.cells = cells
        self.verbose = False

    def cell(self, row, col):
        return self.cells[row * SUDOKU_LENGHT + col]

    def unstatic_cells(self):
        for cell in self.cells:
            if not cell.static:
                yield cell

    def static_cells(self):
        for cell in self.cells:
            if cell.static:
                yield cell

    def append(self, cell):
        self.cells.append(cell)

    def __repr__(self):
        return '\n'.join(
            ' | '.join(
                str(self.cells[j + 9*i].get_number() if self.cells[j +
                                                                   9*i].get_number() != 0 else ' ')
                for j in range(Sudoku.length)
            )
            for i in range(Sudoku.length)
        )

    def cells_row(self, cell, static=False):
        for rcell in self.cells:
            if (not (rcell.static == static)) or (rcell.position == cell.position):
                continue
            if rcell.position // SUDOKU_LENGHT == cell.row:
                yield rcell

    def cells_col(self, cell, static=False):
        for ccell in self.cells:
            if (not (ccell.static == static)) or (ccell.position == cell.position):
                continue
            if ccell.position % SUDOKU_LENGHT == cell.col:
                yield ccell

    def cells_square(self, cell, static=False):
        for scell in self.cells:
            if (not (scell.static == static)) or (scell.position == cell.position):
                continue
            if scell.square == cell.square:
                yield scell

    def solve_row(self, cell, static=False):
        for pcell in self.cells_row(cell, static=static):
            cell.update_numbers(pcell)

    def solve_col(self, cell, static=False):
        for pcell in self.cells_col(cell, static=static):
            cell.update_numbers(pcell)

    def solve_square(self, cell, static=False):
        for pcell in self.cells_square(cell, static=static):
            cell.update_numbers(pcell)

    def solve_init(self):
        for cell in self.unstatic_cells():
            self.solve_row(cell, static=True)
            self.solve_col(cell, static=True)
            self.solve_square(cell, static=True)

    def solve_core(self):
        self.solve_init()
        # find potential for value for each cells
        unstatic_cells = list(self.unstatic_cells())
        cell_idx = 0
        while cell_idx <= len(unstatic_cells) - 1:
            cell = unstatic_cells[cell_idx]
            try:
                self.solve_row(cell)
                self.solve_col(cell)
                self.solve_square(cell)
                if self.verbose:
                    print(
                        f'Solved> Cell({cell.row, cell.col, cell.get_number()})')
                cell_idx += 1
            except:
                if self.verbose:
                    print(
                        f'Back Track Cell({cell.row, cell.col})')
                cell.reset()
                cell_idx -= 1
                cell = unstatic_cells[cell_idx]
                cell.nextnumberidx()

    def solve(self):
        print('INPUT:\n')
        print(self)
        self.solve_core()
        print('\n')
        print('OUTPUT:\n')
        print(self)

    @staticmethod
    def from_grid(grid):
        sudoku = Sudoku()
        nrows, ncols = len(grid), len(grid[0])
        msg = f'Expected {Sudoku.length} rows and cols, found {nrows} rows and {ncols} columns'
        assert(nrows == ncols == Sudoku.length), msg
        for i in range(nrows):
            for j in range(ncols):
                cell = Cell(
                    row=i, col=j,
                    static=True if grid[i][j] != 0 else False,
                    number=grid[i][j])
                sudoku.append(cell)
        return sudoku

    @staticmethod
    def from_csv(path):
        grid = []
        with open(path) as f:
            for line in f.readlines():
                grid.append([int(k) for k in line.split(',')])
        return Sudoku.from_grid(grid)


def test_1():
    print('TEST #1\n')
    path = 'grid/grid_1.csv'
    sdk = Sudoku.from_csv(path)
    sdk.solve()


def test_2():
    print('TEST #2\n')
    path = 'grid/grid_2.csv'
    sdk = Sudoku.from_csv(path)
    sdk.solve()


def test_3():
    print('TEST #3\n')
    path = 'grid/grid_3.csv'
    sdk = Sudoku.from_csv(path)
    sdk.solve()


if __name__ == "__main__":
    pass
    test_3()
