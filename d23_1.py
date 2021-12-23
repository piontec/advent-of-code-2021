from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Rooms:
    a: list[str]
    b: list[str]
    c: list[str]
    d: list[str]

    def __eq__(self, other):
        if type(other) is not Rooms:
            raise ValueError("wrong type")
        return self.a == other.a and self.b == other.b and self.c == other.c and self.d == other.d


rooms_to_corridor_index = {"a": 2, "b": 4, "c": 6, "d": 8}
step_cost = {"a": 1, "b": 10, "c": 100, "d": 1000}


@dataclass
class Burrow:
    corridor: list[str]
    rooms: Rooms
    # tuple of (room_name, room_index
    solved: list[Tuple[str, int]]
    cost: int
    history: list['Burrow']

    def __init__(self, corridor: Optional[list[str]], rooms: Rooms):
        if not corridor:
            self.corridor = ["." for _ in range(11)]
        else:
            self.corridor = corridor
        self.rooms = rooms
        self.solved = []
        self.update_solved()
        self.cost = 0
        self.history = []

    def __eq__(self, other):
        if type(other) is not Burrow:
            raise ValueError("wrong type")
        return self.corridor == other.corridor and self.rooms == other.rooms

    def __str__(self):
        print("#" * 13)
        print("#" + "".join(self.corridor) + "#")
        print(f"###{self.rooms.a[0]}#{self.rooms.b[0]}#{self.rooms.c[0]}#{self.rooms.d[0]}###")
        print(f"  #{self.rooms.a[1]}#{self.rooms.b[1]}#{self.rooms.c[1]}#{self.rooms.d[1]}#")
        print("  " + "#" * 9)

    def update_solved(self) -> None:
        for name in ["a", "b", "c", "d"]:
            if getattr(self.rooms, name)[1] == name:
                info = (name, 1)
                if info not in self.solved:
                    self.solved.append(info)
                if getattr(self.rooms, name)[0] == name:
                    info = (name, 0)
                    if info not in self.solved:
                        self.solved.append(info)

    @property
    def all_solved(self) -> bool:
        return len(self.solved) == 8

    def get_all_moves_from_corridor(self) -> list['Burrow']:
        res: dict[str, list[Burrow]] = {"a": [], "b": [], "c": [], "d": []}
        for i in range(len(self.corridor)):
            if self.corridor[i] == ".":
                continue
            amp = self.corridor[i]
            room = getattr(self.rooms, amp)
            # if we can't enter our room
            if not (room[1] == "." or (room[0] == "." and room[1] == amp)):
                continue
            room_index = 1 if room[1] == "." else 0
            steps = abs(rooms_to_corridor_index[amp] - i) + room_index + 1

            new_bur = deepcopy(self)
            new_bur.corridor[i] = "."
            getattr(new_bur.rooms, amp)[room_index] = amp
            new_bur.cost += steps * step_cost[amp]
            res[amp].append(new_bur)
        return res["d"] + res["c"] + res["b"] + res["a"]

    def get_all_moves_from_rooms(self) -> list['Burrow']:
        res: dict[str, list[Burrow]] = {"a": [], "b": [], "c": [], "d": []}
        for room_name in ["a", "b", "c", "d"]:
            for room_index in range(2):
                room = getattr(self.rooms, room_name)
                # already solved
                if (room_name, room_index) in self.solved:
                    continue
                # not an amp
                if room[room_index] == ".":
                    continue
                # blocked by amp at index 0 - can't leave
                if room_index == 1 and room[0] != ".":
                    continue
                amp = room[room_index]
                possible_corridor_indexes = []
                # go right
                for ci in range(rooms_to_corridor_index[room_name] + 1, len(self.corridor)):
                    if self.corridor[ci] != ".":
                        break
                    if ci in rooms_to_corridor_index.values():
                        continue
                    possible_corridor_indexes.append(ci)
                # go left
                for ci in range(rooms_to_corridor_index[room_name] - 1, -1, -1):
                    if self.corridor[ci] != ".":
                        break
                    if ci in rooms_to_corridor_index.values():
                        continue
                    possible_corridor_indexes.append(ci)
                for ci in possible_corridor_indexes:
                    new_bur = deepcopy(self)
                    new_bur.corridor[ci] = amp
                    getattr(new_bur.rooms, room_name)[room_index] = "."
                    steps = abs(rooms_to_corridor_index[room_name] - ci) + room_index + 1
                    new_bur.cost += steps * step_cost[amp]
                    res[amp].append(new_bur)
        return res["d"] + res["c"] + res["b"] + res["a"]


def main() -> None:
    with open("i23.txt", "r") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)


def run(lines: list[str]) -> int:
    row0 = lines[2].strip().split("#")
    row1 = lines[3].strip().split("#")
    rooms = Rooms([row0[3].lower(), row1[1].lower()], [row0[4].lower(), row1[2].lower()],
                  [row0[5].lower(), row1[3].lower()], [row0[6].lower(), row1[4].lower()])
    burrow = Burrow(None, rooms)

    best_solution: Optional[Burrow] = None
    best_solution_cost = -1
    to_check = deque([burrow])

    while len(to_check) > 0:
        burrow = to_check.pop()
        # check if we have new best solution
        if burrow.all_solved:
            if best_solution_cost == -1 or burrow.cost < best_solution_cost:
                best_solution_cost = burrow.cost
                best_solution = burrow
                print(f"new best: {best_solution_cost}")
            continue
        # check if we're already worse than the best solution so far
        if -1 < best_solution_cost < burrow.cost:
            continue
        from_corridor = burrow.get_all_moves_from_corridor()
        from_rooms = burrow.get_all_moves_from_rooms()
        for b in from_corridor + from_rooms:
            if b in b.history:
                continue
            b.update_solved()
            b.history.append(burrow)
            to_check.append(b)
    return best_solution_cost


def test() -> None:
    txt = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""
    assert run(txt.splitlines()) == 12521


if __name__ == "__main__":
    test()
    main()
