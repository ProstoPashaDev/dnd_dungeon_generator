def count_dist(i, j, state, n, m):
    up, left, right, down = 0, 0, 0, 0
    # up
    s = 0
    for i1 in range(0, i):
        if state[i1][j] == 1:
            s = i1
    up = max(i - s - 1, 0)

    # down
    s = n - 1
    for i1 in range(i + 1, n):
        if state[i1][j] == 1:
            s = i1
            break
    down = max(s - i - 1, 0)

    # left
    s = -1
    for j1 in range(j):
        if state[i][j1] == 1:
            s = j1
    left = max(j - s - 1, 0)

    # right
    s = m - 1
    for j1 in range(j + 1, m):
        if state[i][j1] == 1:
            s = j1
            break
    right = max(s - j - 1, 0)

    return left, up, right, down


def count_sum_around(i, j, state):
    su = 0
    try:
        su += state[i - 1][j]
    except:
        pass

    try:
        su += state[i + 1][j]
    except:
        pass

    try:
        su += state[i][j + 1]
    except:
        pass

    try:
        su += state[i][j - 1]
    except:
        pass

    return su


iterations = 0


def count_space(i, j, state, first=True):
    global iterations
    if first:
        iterations = 0

    iterations += 1
    n = len(state)
    m = len(state[0])

    state[i][j] = "*"

    if i - 1 >= 0 and state[i - 1][j] == 0:
        count_space(i - 1, j, state, False)

    if i + 1 < n and state[i + 1][j] == 0:
        count_space(i + 1, j, state, False)

    if j - 1 >= 0 and state[i][j - 1] == 0:
        count_space(i, j - 1, state, False)

    if j + 1 < m and state[i][j + 1] == 0:
        count_space(i, j + 1, state, False)
