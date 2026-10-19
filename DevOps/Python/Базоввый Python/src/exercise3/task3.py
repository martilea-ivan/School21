def read_matrix(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    matrix = []
    for line in lines :
        if line.strip():
            row = list(map(int, line.split()))
            matrix.append(row)
    return matrix



def find_figures(matrix):
    n = len(matrix)
    figures = []
    visited = [ [False] * n for _ in range(n) ]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    def bfs(start_r, start_c):
        queue = [(start_r, start_c)]
        visited[start_r][start_c] = True
        cells = []
        while queue:
            r, c = queue.pop(0)
            cells.append((r, c))
            for dr, dc in directions:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and matrix[nr][nc] == 1:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
        return cells

    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1 and not visited[i][j]:
                component = bfs(i, j)
                figures.append(component)
    return figures


def classify_figure(cells):
    rows = [r for r, c in cells]
    cols = [c for r, c in cells]

    min_r = min(rows)
    max_r = max(rows)
    min_c = min(cols)
    max_c = max(cols)

    height = max_r - min_r + 1
    width = max_c - min_c + 1

    if height == width and len(cells) == height * width:
        return "square"
    else:
        return "circle"
def main():
    matrix = read_matrix("input.txt")

    figures = find_figures(matrix)

    squares = 0
    circles = 0

    for figure in figures:
        if len(figure) > 1:
            shape = classify_figure(figure)
            if shape == "square":
                squares += 1
            else:
                circles += 1

    print(squares, circles)



if __name__ == "__main__":
    main()