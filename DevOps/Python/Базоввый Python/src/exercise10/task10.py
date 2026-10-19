def main():
    try:
        N, T = map(int, input().split())
        devices = []
        for _ in range(N):
            year, cost, time = map(int, input().split())
            devices.append((year, cost, time))

        min_cost = float('inf')
        found = False

        by_year = {}
        for year, cost, time in devices:
            if year not in by_year:
                by_year[year] = []
            by_year[year].append((cost, time))

        for year, devs in by_year.items():
            for i in range(len(devs)):
                for j in range(i + 1, len(devs)):
                    if devs[i][1] + devs[j][1] == T:
                        total_cost = devs[i][0] + devs[j][0]
                        if total_cost < min_cost:
                            min_cost = total_cost
                            found = True

        if found:
            print(min_cost)
        else:
            print("Invalid input")

    except:
        print("Invalid input")

if __name__ == "__main__":
    main()