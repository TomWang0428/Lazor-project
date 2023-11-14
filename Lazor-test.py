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
    block_list_AC = []
    block_list_B = []
    lasers = []
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
            lasers.append(Lazor(laser_start, laser_direction))

        if line.startswith('P'):
            parts = line.split()
            if len(parts) == 3:
                goal_p.append((int(parts[2]), int(parts[1])))

    block_list_AC = ['A'] * A_block + ['C'] * C_block
    block_list_B = ['B'] * B_block
    return grid, block_list_AC, block_list_B, lasers, goal_p


def use_unused(grid, unused_bl, lasers, goal_p, t2_grid=None):
    re_grid= remake_grid(grid)
    impossible = []
    for lasor in lasers:
        laser_start = lasor.laser_start
        laser_direction = lasor.laser_direction
        path, p_dir = lazor_path(re_grid, lasor)
        impossible = impossible + find_possible(path, grid)
    rows = len(grid)
    cols = len(grid[1])
    all_cor = [(x, y) for x in range(cols) for y in range(rows)]
    diff = [item for item in all_cor if item not in impossible]

    t_grid = copy.deepcopy(grid)
    finish_flag = 0
    for pos in diff:
        for block in unused_bl:
            t_block_list = unused_bl.copy()
            if t_grid[pos[0]][pos[1]] == "o":
                t_grid[pos[0]][pos[1]] = block
                t_block_list.remove(block)
            if t_block_list == []:
                break
    unused_block = t_block_list.copy()
    t2_grid = copy.deepcopy(t_grid)
    for i in range(len(unused_block)):
        t2_grid, finish_flag, ub = lazor_solve(t2_grid, laser_start, laser_direction, goal_p, [unused_block[i]], finish_flag)
    return t2_grid, unused_bl


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


def lazor_path(re_grid, laser):
    width = len(re_grid)
    height = len(re_grid[0])
    x = laser.laser_start[0]
    y = laser.laser_start[1]
    laser_direction = laser.laser_direction
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
                    if refract_n % 2 == 0 or re_grid[x][y] == "CC":
                        if re_grid[x + laser_direction[0]][y + laser_direction[1]] == "C" or re_grid[x + laser_direction[0]][y + laser_direction[1]] == "CC":
                            c_dir = laser_direction
                            if x % 2 == 0:
                                lasor = Lazor((x, y),(-laser_direction[0], laser_direction[1]))
                                add_path, add_pt = lazor_path(re_grid, lasor)
                            if y % 2 == 0:
                                lasor = Lazor((x, y),(laser_direction[0], - laser_direction[1]))
                                add_path, add_pt = lazor_path(re_grid, lasor)
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
                            lasor = Lazor((x, y), (-laser_direction[0], laser_direction[1]))
                            add_path, add_pt = lazor_path(re_grid, lasor)
                        if y % 2 == 0:
                            lasor = Lazor((x, y), (laser_direction[0], - laser_direction[1]))
                            add_path, add_pt = lazor_path(re_grid, lasor)
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
            if x < width and y < height and x >=0 and y >= 0:
                flatten_list(path)
                flatten_list(pt_dir)
                if (x,y) in path and pt_dir[path.index((x,y))] == c_dir:
                    break
                else:
                    path.append((x, y))
            else:
                break
    else:
        return
    return flatten_list(path), flatten_list(pt_dir)


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



def lazor_solve(grid, lasers, goal_p, block_list, finish_flag, f_grid = None, u_block_list = None):
    if f_grid is None:
        f_grid = []
    path = []
    re_grid = remake_grid(grid)
    for laser in lasers:
        pathh, p_dir = lazor_path(re_grid, laser)
        path = path + pathh
    list(set(flatten_list(path)))
    possible_placement = find_possible(path, grid)
    for pos in possible_placement:
        if finish_flag == 0 and grid[pos[0]][pos[1]] == 'o':
            for block in block_list:
                t_grid = copy.deepcopy(grid)
                t_grid[pos[0]][pos[1]] = block
                t_block_list = block_list.copy()
                t_block_list.remove(block)
                # Recursively solve with the updated grid and block list
                f_grid, finish_flag, u_block_list = lazor_solve(t_grid, lasers, goal_p, t_block_list, finish_flag, f_grid)
                if finish_flag:
                    return f_grid, finish_flag, u_block_list
    if set(goal_p).issubset(set(path)):
        finish_flag = 1
        f_grid = copy.deepcopy(grid)  # update f_grid with the current grid as the solution
        u_block_list = copy.deepcopy(t_block_list)
        return f_grid, finish_flag, u_block_list
    return f_grid, finish_flag, u_block_list


class Lazor:
    def __init__(self, laser_start, laser_direction):
        self.laser_start = laser_start
        self.laser_direction = laser_direction



if __name__ == "__main__":
    test_grid = [['o', 'B', 'A'], ['o', 'o', 'o'], ['A', 'C', 'o']]
    """
    grid = [["o"] * 4 for _ in range(4)]
    laser_start = (7, 2)
    laser_direction = (-1, 1)
    goal_p = (0, 3), (3, 4), (5, 2), (7, 4)
    
    block_list = ["A", "C", "A"]
    finish_flag = 0
    re_grid = remake_grid(test_grid)
    path, dir = lazor_path(re_grid, laser_start, laser_direction)
    """
    ftpr = 'tiny_5.bff'
    grid, block_list_AC, block_list_B, lasers, goal_p = read_file(ftpr)
    finish_flag = 0
    f_grid, finish_flag, unused_bl = lazor_solve(grid, lasers, goal_p, block_list_AC, finish_flag)
    unused_bl.append(block_list_B)
    unused_bl = flatten_list(unused_bl)
    if len(unused_bl) >= 1:
        f_grid, unused_bl = use_unused(f_grid, unused_bl, lasers, goal_p)
    print(f_grid)