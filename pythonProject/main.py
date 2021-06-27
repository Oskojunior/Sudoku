board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def find_loc(sud):
    for i in range(len(sud)):
        for j in range(len(sud[0])):
            if sud[i][j] == 0:
                return i, j

    return None


def valid(sud, num, location):
    for i in range(0, len(sud[0])):
        if sud[location[0]][i] == num and location[1] != i:
            return False

    for i in range(0, len(board)):
        if sud[i][location[1]] == num and location[1] != i:
            return False

    box = location[0] // 3, location[1] // 3

    for i in range(box[0] * 3, box[0] * 3 + 3):
        for j in range(box[1] * 3, box[1] * 3 + 3):
            if sud[i][j] == num and location != (i, j):
                return False

    return True


def solve(sud):
    location = find_loc(sud)

    if location:
        row, col = location
    else:
        return True

    for num in range(1, 10):
        if valid(sud, num, location):
            sud[row][col] = num

            if solve(sud):
                return True

            sud[row][col] = 0

    return False


def show_board(sud):
    for i in range(9):
        for j in range(9):
            print(sud[i][j], end="")
        print('\n')


if solve(board):
    show_board(board)
else:
    print("Solution not found")
