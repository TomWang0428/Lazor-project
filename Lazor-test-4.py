import copy
import multiprocessing
from sympy.utilities.iterables import multiset_permutations
from PIL import Image


def count_o_in_2d_list(matrix):
    count = 0
    for row in matrix:
        for element in row:
            if element == 'o':
                count += 1
    return count

def vis_path(path,re_grid):
    path = list(set(flatten_list(path)))
    t_regrid = copy.deepcopy(re_grid)
    for i in range(len(path)):
        t_regrid[path[i][0]][path[i][1]] = "1"
    return t_regrid

def flatten_list(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list

class Grid:
    def __init__(self, grid_data):
        self.grid = [list(row) for row in grid_data]

    def update_grid(self, position, block):
        self.grid[position[0]][position[1]] = block.block_type

    @staticmethod
    def remake_grid(grid):
        width = len(grid)
        height = len(grid[0])
        re_grid = [[None] * (height * 2 + 1) for _ in range(width * 2 + 1)]
        for i in range(width):
            for j in range(height):
                for k in range(3):
                    for h in range(3):
                        if re_grid[i * 2 + k][j * 2 + h] == None or re_grid[i * 2 + k][j * 2 + h] == "o" or \
                                re_grid[i * 2 + k][j * 2 + h] == "x":
                            re_grid[i * 2 + k][j * 2 + h] = grid[i][j]
                        else:
                            re_grid[i * 2 + k][j * 2 + h] = re_grid[i * 2 + k][j * 2 + h] + grid[i][j]
                            re_grid[i * 2 + k][j * 2 + h] = re_grid[i * 2 + k][j * 2 + h].replace("o", "")
        return re_grid

    def placement(self, block_list):
        h = len(self.grid)
        w = len(self.grid[0])
        c = 0
        t_grid = Grid(copy.deepcopy(self.grid))
        for y in range(w):
            for x in range(h):
                if t_grid.grid[x][y] == 'o':
                    t_grid.update_grid((x,y),Block(block_list[c]))
                    c += 1
        return t_grid.grid

    def Count(self, letter):
        n = self.grid.count(letter)
        return n


class Block:
    def __init__(self, block_type):
        self.block_type = block_type

class Laser:
    def __init__(self, start, direction):
        self.start = start
        self.direction = direction

    def get_path(self, re_grid):
        width = len(re_grid)
        height = len(re_grid[0])
        x = self.start[0]
        y = self.start[1]
        laser_direction = self.direction
        path = [(x, y)]
        refract_n = 0
        pt_dir = []
        if x <= width and y <= height and len(path) <= 100:
            c_dir = laser_direction

            while x in range(width) and y in range(height) and len(path) <= 100:
                if len(path) != 1:
                    if re_grid[x][y] == "o" or re_grid[x][y] == "x":
                        c_dir = laser_direction
                    elif "A" in re_grid[x][y]:
                        if x % 2 == 0:
                            c_dir = (-laser_direction[0], laser_direction[1])
                            laser_direction = c_dir
                        if y % 2 == 0:
                            c_dir = (laser_direction[0], -laser_direction[1])
                            laser_direction = c_dir
                    elif "B" in re_grid[x][y]:
                        break
                    if re_grid[x][y] == "C" or re_grid[x][y] == "CC":
                        if refract_n % 2 == 0 or re_grid[x][y] == "CC":
                            if re_grid[x + laser_direction[0]][y + laser_direction[1]] == "C" or \
                                    re_grid[x + laser_direction[0]][y + laser_direction[1]] == "CC":
                                c_dir = laser_direction
                                if x % 2 == 0:
                                    las_2 = Laser((x, y),(-laser_direction[0], laser_direction[1]))
                                    add_path, add_pt = las_2.get_path(re_grid)

                                if y % 2 == 0:
                                    las_2 = Laser((x, y), (laser_direction[0], -laser_direction[1]))
                                    add_path, add_pt = las_2.get_path(re_grid)
                                path.extend(add_path)
                                pt_dir.extend(add_pt)
                        else:
                            c_dir = laser_direction
                        refract_n += 1
                elif "A" in re_grid[x][y] and "A" in re_grid[x + laser_direction[0]][y + laser_direction[1]]:
                    if x % 2 == 0:
                        c_dir = (-laser_direction[0], laser_direction[1])
                    if y % 2 == 0:
                        c_dir = (laser_direction[0], -laser_direction[1])
                    if x + c_dir[0] < width and y + c_dir[1] < height and x + c_dir[0] > 0 and y + c_dir[1] > 0:
                        if "A" in re_grid[x + c_dir[0]][y + c_dir[1]]:
                            c_dir = laser_direction
                    else:
                        laser_direction = c_dir

                elif "B" in re_grid[x][y] and "B" in re_grid[x + laser_direction[0]][y + laser_direction[1]]:
                    break
                elif re_grid[x][y] == "C" or re_grid[x][y] == "CC":
                    if re_grid[x + laser_direction[0]][y + laser_direction[1]] == "C" or \
                            re_grid[x + laser_direction[0]][y + laser_direction[1]] == "CC":
                        if refract_n % 2 == 0:
                            c_dir = laser_direction
                            if x % 2 == 0:
                                las_2 = Laser((x, y), (-laser_direction[0], laser_direction[1]))
                                add_path, add_pt = las_2.get_path(re_grid)
                            if y % 2 == 0:
                                las_2 = Laser((x, y), (laser_direction[0], -laser_direction[1]))
                                add_path, add_pt = las_2.get_path(re_grid)
                            path.extend(add_path)
                            pt_dir.extend(add_pt)
                        else:
                            c_dir = laser_direction
                    refract_n += 1
                else:
                    c_dir = laser_direction
                pt_dir.append(c_dir)
                x = x + c_dir[0]
                y = y + c_dir[1]
                if x < width and y < height and x >= 0 and y >= 0:
                    flatten_list(path)
                    flatten_list(pt_dir)
                    if (x, y) in path and pt_dir[path.index((x, y))] == c_dir:
                        break
                    else:
                        path.append((x, y))
                else:
                    break
        else:
            return
        return flatten_list(path), flatten_list(pt_dir)

class Solver:
    def __init__(self, grid, blocks, lasers, goals):
        self.grid = grid
        self.blocks = blocks
        self.lasers = lasers
        self.goals = goals
        self.finish_flag = False

    def solver(self, per):
        grid = Grid(self.grid.grid)

        t_grid = Solver(grid.placement(per), per, self.lasers, self.goals)

        if t_grid._is_goal_reached():
            return grid.placement(per)

    def _is_goal_reached(self, path=None):
        # Check if all goals are reached by lasers
        if path is None:
            path = []
        for laser in self.lasers:
            p = self.grid
            pathh, _ = laser.get_path(Grid.remake_grid(self.grid))
            path.append(pathh)

        if set(self.goals).issubset(set(flatten_list(path))):
            vis_path(path, Grid.remake_grid(self.grid))
            return True
        else:
            return False

def read_file(ftpr):
    with open(ftpr, 'r') as f:
        lines = f.readlines()

    cleaned_list = [item.strip() for item in lines]

    # grid
    first_line_index = cleaned_list.index("GRID START") + 1
    end_line_index = cleaned_list.index("GRID STOP") - 1

    grid_data = []
    for i in range(first_line_index, end_line_index + 1):
        grid_data.append(cleaned_list[i])
    grid = [s.split() for s in grid_data]

    # block ABC & Lazor
    A_block = 0
    B_block = 0
    C_block = 0
    lasers = []
    goal_p = []
    i = 0
    n = 10000

    for line in lines:
        i += 1
        if line == 'GRID STOP\n':
            n = i
        if not line or line.startswith('#'):
            continue

        else:
            if line.startswith('A') and n < i:
                A_block = int(line.split()[1])
            elif line.startswith('B') and n < i:
                B_block = int(line.split()[1])
            elif line.startswith('C') and n < i:
                C_block = int(line.split()[1])

        if line.startswith('L'):
            parts = line.split()
            laser_start = (int(parts[2]), int(parts[1]))
            laser_direction = (int(parts[4]), int(parts[3]))
            lasers.append(Laser(laser_start, laser_direction))

        if line.startswith('P'):
            parts = line.split()
            if len(parts) == 3:
                goal_p.append((int(parts[2]), int(parts[1])))

    block_list_AC = ['A'] * A_block + ['C'] * C_block
    block_list_B = ['B'] * B_block
    return grid, block_list_AC, block_list_B, lasers, goal_p


def main(filepath):
    #filepath = 'yarn_5.bff'
    grid_data, block_list_AC, block_list_B, lasers_data, goals = read_file(filepath)

    grid = Grid(grid_data)
    blocks = [Block(block_type) for block_type in block_list_AC + ['B'] * len(block_list_B)]

    solver = Solver(grid, blocks, lasers_data, goals)

    n = count_o_in_2d_list(grid_data)
    all_blocks = flatten_list([['o'] * n, flatten_list([block_list_AC, block_list_B])])
    all_per = list(multiset_permutations(all_blocks))
    with multiprocessing.Pool() as pool:
        # Distribute the work among the processes
        results = pool.map(solver.solver, all_per)

    # Process the results
    for solved_grid in results:
        if solved_grid:
            for row in solved_grid:
                print(' '.join(row))
            return solved_grid
            # break


def get_colors():
    '''
    Colors map that the solution output will use:
        'o' - White - place that can put blocks
        'x' - Grey - place that must be left empty
        'A' - Green - type A block
        'B' - Black - type B block
        'C' - Blue - type C block

    **Returns**

        color_map: *dict, int, tuple*
            A dictionary that will correlate the key to a color.
    '''
    return {
        'x': (128, 128, 128),
        'o': (255, 255, 255),
        'A': (0, 255, 0),
        'B': (0, 0, 0),
        'C': (0, 0, 255),
    }


def print_solution(solution_list, blockSize=100, name="solution"):
    # nBlocks = len(solution_list)
    sol = [[row[i] for row in solution_list] for i in range(len(solution_list[0]))]
    height = len(sol)
    width = len(sol[0])

    dims_height = height * blockSize
    dims_width = width * blockSize

    colors = get_colors()

    # Verify that all values in the maze are valid colors.
    ERR_MSG = "Error, invalid maze value found!"
    assert all([x in colors.keys() for row in sol for x in row]), ERR_MSG

    img = Image.new("RGB", (dims_width, dims_height), color=(128, 128, 128))

    # Parse "maze" into pixels
    for jx in range(width):
        for jy in range(height):
            x = jx * blockSize
            y = jy * blockSize
            for i in range(blockSize):
                for j in range(blockSize):
                    img.putpixel((x + i, y + j), colors[sol[jx][jy]])

    if not name.endswith(".png"):
        name += ".png"
    img.save("%s" % name)


if __name__ == "__main__":
    fp = 'yarn_5.bff'
    my_solved_grid = main(fp)
    print_solution(my_solved_grid, blockSize=100, name=f"{fp}_solution")
