from typing import Tuple, List

import numpy as np

Point = Tuple[int, int]


def main() -> None:
    with open("i15.txt", "r") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)


def get_neighbor_nodes(p: Point, shape: Tuple[int, int]) -> List[Point]:
    y = p[0]
    x = p[1]
    lp: list[Point] = []
    for p in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        ny = y + p[0]
        nx = x + p[1]
        if nx < 0 or nx > shape[1] - 1 or ny < 0 or ny > shape[0] - 1:
            continue
        lp.append((ny, nx))
    return lp


def get_path(arr: np.ndarray, start: Point, end: Point) -> int:
    visited = np.full(arr.shape, False, dtype=bool)
    parents: dict[Point, Point] = {}
    max_value = np.iinfo(np.int32).max
    distance = np.full(arr.shape, max_value, dtype=np.int32)
    distance[start] = 0
    current = start
    max_x = 0
    while True:
        for neighbor in get_neighbor_nodes(current, arr.shape):
            if visited[neighbor]:
                continue
            dist = distance[current] + arr[neighbor]
            if distance[neighbor] == -1 or dist < distance[neighbor]:
                distance[neighbor] = dist
                parents[neighbor] = current
        visited[current] = True
        if current == end:
            break
        min_unvisited_val = max_value
        min_unvisited_index = (-1, -1)
        for y in range(arr.shape[1]):
            for x in range(arr.shape[0]):
                if visited[y, x]:
                    continue
                if distance[y, x] < min_unvisited_val:
                    min_unvisited_val = distance[y, x]
                    min_unvisited_index = (y, x)
        current = min_unvisited_index
        if current[1] > max_x:
            max_x = current[1]
            print(max_x)
    return distance[end]


def expand(arr: np.ndarray, times: int = 5) -> np.ndarray:
    arrays: dict[Point, np.ndarray] = {(0, 0): arr}
    last = np.copy(arr)
    for t in range(1, times):
        new_arr = np.copy(last)
        new_arr += 1
        new_arr %= 10
        new_arr[new_arr == 0] = 1
        for y in range(t, -1, -1):
            arrays[(y, t - y)] = new_arr
        last = new_arr
    for t in range(1, times):
        new_arr = np.copy(last)
        new_arr += 1
        new_arr %= 10
        new_arr[new_arr == 0] = 1
        i = 1
        for y in range(t, times):
            arrays[(y, times - i)] = new_arr
            i += 1
        last = new_arr
    rows: list[list[np.ndarray]] = []
    for i in range(times):
        rows.append([arrays[k] for k in arrays if k[0] == i])
    arr = np.block(rows)
    return arr


def run(lines: list[str]) -> int:
    size = len(lines[0].strip())
    arr = np.ndarray((size, size), dtype=np.int8)
    row = 0
    for line in lines:
        arr[row] = [int(i) for i in line.strip()]
        row += 1

    arr = expand(arr)
    dim = arr.shape
    best_path = get_path(arr, (0, 0), (dim[0] - 1, dim[1] - 1))
    return best_path


def test() -> None:
    txt = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
    assert run(txt.splitlines()) == 315


if __name__ == "__main__":
    test()
    main()
