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
