from cell import Cell
import random, time

class Maze:
    def __init__(
            self,
            x1,    
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None
        ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
    
    def _create_cells(self):
        #establish maze cells
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)

        #draw cells to screen
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)



    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.005)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            to_visit_list = []

            #check adjacent cells of current for one(s) that have not been visited yet
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit_list.append((i-1, j, "left"))
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                to_visit_list.append((i+1, j, "right"))
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit_list.append((i, j-1, "top"))
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                to_visit_list.append((i, j+1, "bottom"))


            #break out if no valid options exist
            if len(to_visit_list) == 0:
                self._draw_cell(i, j)
                return
            
            #randomize next direction to move
            target_index = random.randrange(len(to_visit_list))
            to_visit = to_visit_list[target_index]
            target_i = to_visit[0]
            target_j = to_visit[1]
            direction = to_visit[2]
            
            #match and break current, and next cells shared walls
            match direction:
                case "left":
                    self._cells[target_i][target_j].has_right_wall = False
                    self._cells[i][j].has_left_wall = False
                case "right":
                    self._cells[target_i][target_j].has_left_wall = False
                    self._cells[i][j].has_right_wall = False
                case "top":
                    self._cells[target_i][target_j].has_bottom_wall = False
                    self._cells[i][j].has_top_wall = False
                case "bottom":
                    self._cells[target_i][target_j].has_top_wall = False
                    self._cells[i][j].has_bottom_wall = False

            #recurse to next(target) cell
            self._break_walls_r(target_i, target_j)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    #returns True if this is the end cell, OR if the current path hasn't been proven to be incorrect
    #returns False if current cell cannot be part of solution path
    def _solve_r(self, i, j):
        self._animate()

        #mark current as visited
        self._cells[i][j].visited = True

        #if current is end, the maze is solved
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        #try left
        if i > 0 and not self._cells[i-1][j].visited and not self._cells[i][j].has_left_wall:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        
        #check adjacent cell in all directions, visit if they haven't been visited, and no wall exists between current, and neighbor
        #try right
        if i < self._num_cols - 1 and not self._cells[i+1][j].visited and not self._cells[i][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)
        #try top
        if j > 0 and not self._cells[i][j-1].visited and not self._cells[i][j].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)
        #try bottom
        if j < self._num_rows - 1 and not self._cells[i][j+1].visited and not self._cells[i][j].has_bottom_wall:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)

        #wrong path traversed, go back to offending cell, and continue    
        return False
    
    #discover solution using depth first search
    def solve(self):
        return self._solve_r(0, 0)