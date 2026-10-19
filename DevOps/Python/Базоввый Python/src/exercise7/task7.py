def main():
    n, m = map(int, input().split())

    matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)

    dp = [[0] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if i == 0 and j == 0:
                dp[i][j] = matrix[i][j]
            elif i == 0:
                dp[i][j] = dp[i][j - 1] + matrix[i][j]
            elif j == 0:
                dp[i][j] = dp[i - 1][j] + matrix[i][j]
            else:
                dp[i][j] = matrix[i][j] + max(dp[i - 1][j], dp[i][j - 1])

    print(dp[n - 1][m - 1])


if __name__ == "__main__":
    main()