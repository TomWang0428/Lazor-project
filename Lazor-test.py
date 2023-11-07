import sys
import copy
import itertools
sys.setrecursionlimit(100000)


def read_file(ftpr):
    # preprocess
    with open(ftpr, 'r') as f:
        lines = f.readlines()

    cleaned_list = [item.strip() for item in lines]

    # grid
    first_line_index = 0
    end_line_index = 0
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
    block_list = []
    laser_start = ()
    laser_direction = ()
    goal_p = []

    for line in lines:

        if not line or line.startswith('#'):
            continue

        else:
            if line.startswith('A'):
                A_block = int(line.split()[1])
            elif line.startswith('B'):
                B_block = int(line.split()[1])
            elif line.startswith('C'):
                C_block = int(line.split()[1])

        if line.startswith('L'):
            parts = line.split()
            laser_start = (int(parts[2]), int(parts[1]))
            laser_direction = (int(parts[4]), int(parts[3]))

        if line.startswith('P'):
            parts = line.split()
            if len(parts) == 3:
                goal_p.append((int(parts[2]), int(parts[1])))

    block_list = ['A'] * A_block + ['B'] * B_block + ['C'] * C_block
    return grid, block_list, laser_start, laser_direction, goal_p













def all_letter_permutations(letters):
    perms = itertools.permutations(letters)
    perms_list = [list(perm) for perm in set(perms)]
    perms_list.sort()
    return perms_list
def flatten_list(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list
def remake_grid(grid):
    width = len(grid)
    height = len(grid[0])
    re_grid = [[None] * (height * 2 + 1) for _ in range(width * 2 + 1)]
    for i in range(width):
        for j in range(height):
            for k in range(3):
                for h in range(3):
                    if re_grid[i * 2 + k][j * 2 + h] == None or re_grid[i * 2 + k][j * 2 + h] == "o" or re_grid[i * 2 + k][j * 2 + h] == "x":
                        re_grid[i * 2 + k][j * 2 + h] = grid[i][j]
                    else:
                        re_grid[i * 2 + k][j * 2 + h] = re_grid[i * 2 + k][j * 2 + h] + grid[i][j]
                        re_grid[i * 2 + k][j * 2 + h] = re_grid[i * 2 + k][j * 2 + h].replace("o","")
    return re_grid


def lazor_path(re_grid, laser_start, laser_direction):
    width = len(re_grid)
    height = len(re_grid[0])
    x = laser_start[0]
    y = laser_start[1]
    path = [(x,y)]
    refract_n = 0
    pt_dir = []
    if x <= width and y <= height and len(path) <= 100:
        c_dir = laser_direction

        while x in range(width) and y in range(height) and len(path) <= 100:
            a = vis_path(re_grid, path)
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
                    if refract_n % 2 == 0:
                        if re_grid[x + laser_direction[0]][y + laser_direction[1]] == "C" or re_grid[x + laser_direction[0]][y + laser_direction[1]] == "CC":
                            c_dir = laser_direction
                            if x % 2 == 0:
                                add_path = lazor_path(re_grid, (x, y), (-laser_direction[0], laser_direction[1]))
                            if y % 2 == 0:
                                add_path = lazor_path(re_grid, (x,y), (laser_direction[0], - laser_direction[1]))
                            path.append(add_path)
                    else:
                        c_dir = laser_direction
                    refract_n += 1
            elif "A" in re_grid[x][y] and "A" in re_grid[x + laser_direction[0]][y + laser_direction[1]]:
                if x % 2 == 0:
                    c_dir = (-laser_direction[0], laser_direction[1])
                if y % 2 == 0:
                    c_dir = (laser_direction[0], -laser_direction[1])
                if "A" in re_grid[x + c_dir[0]][y + c_dir[1]]:
                    c_dir = laser_direction
                else:
                    laser_direction = c_dir

            elif "B" in re_grid[x][y] and "B" in re_grid[x + laser_direction[0]][y + laser_direction[1]]:
                break
            elif re_grid[x][y] == "C" or re_grid[x][y] == "CC":
                if re_grid[x + laser_direction[0]][y + laser_direction[1]] == "C" or re_grid[x + laser_direction[0]][y + laser_direction[1]] == "CC":
                    if refract_n % 2 == 0:
                        c_dir = laser_direction
                        if x % 2 == 0:
                            add_path = lazor_path(re_grid, (x, y), (-laser_direction[0], laser_direction[1]))
                        if y % 2 == 0:
                            add_path = lazor_path(re_grid, (x, y), (laser_direction[0], - laser_direction[1]))
                        path.append(add_path)
                    else:

                        c_dir = laser_direction
                refract_n += 1
            pt_dir.append(c_dir)
            x = x + c_dir[0]
            y = y + c_dir[1]
            if x < width and y < height and x >=0 and y >= 0:
                path.append((x,y))
                list(set(flatten_list(path)))
            elif (x,y) in path and pt_dir[path.index((x,y))] == c_dir:
                break
    else:
        return
    return list(set(flatten_list(path)))

def find_possible(path, grid):
    width = len(grid)
    height = len(grid[0])
    possible_placement = []
    for i in range(len(path)):
        x = path[i][0]
        y = path[i][1]
        if x % 2 == 0:
            if x//2 <= width - 1:
                possible_placement.append((x // 2, y // 2))
            if x // 2 - 1 >= 0:
                possible_placement.append((x // 2 - 1, y // 2))
        if y % 2 == 0:
            if y // 2 <= height - 1:
             possible_placement.append((x // 2, y // 2))
            if y // 2 - 1 >= 0:
                possible_placement.append((x // 2, y // 2 - 1))
    return list(set(possible_placement))

def vis_path(re_grid,path):
    path = list(set(flatten_list(path)))
    t_regrid = copy.deepcopy(re_grid)
    for i in range(len(path)):
        t_regrid[path[i][0]][path[i][1]] = "1"
    return t_regrid



def lazor_solve(grid, laser_start, laser_direction, goal_p, block_list, finish_flag, f_grid=None):
    if f_grid is None:
        f_grid = []

    re_grid = remake_grid(grid)
    path = lazor_path(re_grid, laser_start, laser_direction)

    if set(goal_p).issubset(path):
        finish_flag = 1
        f_grid = copy.deepcopy(grid)  # update f_grid with the current grid as the solution
        return f_grid, finish_flag

    possible_placement = find_possible(path, grid)

    for pos in possible_placement:
        if finish_flag == 0 and grid[pos[0]][pos[1]] == 'o':
            for block in block_list:
                t_grid = copy.deepcopy(grid)
                t_grid[pos[0]][pos[1]] = block
                t_block_list = block_list.copy()
                t_block_list.remove(block)
                # Recursively solve with the updated grid and block list
                f_grid, finish_flag = lazor_solve(t_grid, laser_start, laser_direction, goal_p, t_block_list, finish_flag, f_grid)
                if finish_flag:
                    return f_grid, finish_flag

    return f_grid, finish_flag



if __name__ == "__main__":
    """
    grid = [["o"] * 4 for _ in range(4)]
    laser_start = (7, 2)
    laser_direction = (-1, 1)
    goal_p = (0, 3), (3, 4), (5, 2), (7, 4)
    test_grid = [['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'], ['o', 'A', 'o', 'o'], ['o', 'C', 'A', 'o']]
    block_list = ["A", "C", "A"]
    finish_flag = 0
    re_grid = remake_grid(test_grid)
    path = lazor_path(re_grid, laser_start, laser_direction)
    """
    ftpr = 'mad_4.bff'
    grid, block_list, laser_start, laser_direction, goal_p = read_file(ftpr)
    finish_flag = 0
    print(lazor_solve(grid, laser_start, laser_direction, goal_p, block_list, finish_flag))
