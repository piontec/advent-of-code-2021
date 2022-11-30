from dataclasses import dataclass

dist_freqs = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


# points_p1: int, points_p2: int, pos_p1: int, pos_p2: int
State = tuple[int, int, int, int]


def run(pos1: int, pos2: int, size: int = 10, limit: int = 21) -> int:
    games_in_progress: dict[State, int] = {(0, 0, pos1, pos2): 1}
    games_won = {1: 0, 2: 0}

    while len(games_in_progress):
        state, freq = games_in_progress.popitem()
        for (p1, f1) in dist_freqs.items():
            pos_p1 = ((state[2] - 1 + p1) % size) + 1
            points_p1 = state[0] + pos_p1
            if points_p1 >= limit:
                games_won[1] += freq * f1
                break

            for (p2, f2) in dist_freqs.items():
                pos_p2 = ((state[3] - 1 + p2) % size) + 1
                points_p2 = state[1] + pos_p2
                if points_p2 >= limit:
                    games_won[2] += freq * f2
                    break

                new_state = (points_p1, points_p2, pos_p1, pos_p2)
                if new_state not in games_in_progress:
                    games_in_progress[new_state] = 1
                games_in_progress[new_state] += f1 * f2
    return max(games_won[1], games_won[2])


def main() -> None:
    res = run(4, 6)
    print(res)


def test() -> None:
    res = run(4, 8)
    assert res == 444356092776315


if __name__ == "__main__":
    test()
    main()
