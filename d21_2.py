import itertools
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


def main() -> None:
    res = run(4, 6)
    print(res)


@dataclass
class State:
    field: int
    count: int
    points: int
    moves: int


def get_all_results(pos: int, size: int, end_score: int) -> dict[int, int]:
    in_progress: list[State] = [State(pos, 1, 0, 0)]
    won: list[State] = []

    while len(in_progress) > 0:
        new_in_progress: list[State] = []
        for ip in in_progress:
            for dist_val, dist_freq in dist_freqs.items():
                new_field = ((ip.field - 1 + dist_val) % size) + 1
                new_points = ip.points + new_field
                new_state = State(new_field, ip.count * dist_freq, new_points, ip.moves + 1)
                if new_state.points >= end_score:
                    won.append(new_state)
                else:
                    new_in_progress.append(new_state)
        in_progress = new_in_progress
    sorted(won, key=lambda w: w.moves)
    kl: dict[int, list[State]] = {k: list(v) for k, v in itertools.groupby(won, lambda w: w.moves)}
    res = {k: sum([s.count for s in v]) for k, v in kl.items()}
    return res


def run(p1_pos: int, p2_pos: int, size: int = 10, end_score: int = 21) -> int:
    p1_res = get_all_results(p1_pos, size, end_score)
    p2_res = get_all_results(p2_pos, size, end_score)

    won_by_p1 = 0
    for moves in p1_res:
        p2_worse = sum([s for k, s in p2_res.items() if k >= moves])
        won_by_p1 += p1_res[moves] * p2_worse

    won_by_p2 = 0
    for moves in p2_res:
        p1_worse = sum([s for k, s in p1_res.items() if k > moves])
        won_by_p2 += p2_res[moves] * p1_worse

    return max([won_by_p1, won_by_p2])


def test() -> None:
    res = run(4, 8)
    assert res == 444356092776315


if __name__ == "__main__":
    test()
    main()
