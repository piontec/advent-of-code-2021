from typing import TypedDict


class Regs(TypedDict):
    w: int
    x: int
    y: int
    z: int


class Alu:
    def __init__(self, inp: list[int]):
        self.inp = inp
        self.regs: Regs = {"w": 0, "x": 0, "y": 0, "z": 0}
        self._inp_pointer = 0

    def _arg_val(self, arg: str) -> int:
        if arg in ["w", "x", "y", "z"]:
            return self.regs[arg]
        return int(arg)

    def run_instr(self, instr: str) -> bool:
        op, args = instr.split(" ", maxsplit=1)
        r1 = args[0]
        if r1 not in ["w", "x", "y", "z"]:
            raise Exception("bad arg[0]")
        match op:
            case "inp":
                self.regs[r1] = self.inp[self._inp_pointer]
                self._inp_pointer += 1
            case "add":
                r2 = args.split(" ")[1]
                self.regs[r1] = self.regs[r1] + self._arg_val(r2)
            case "mul":
                r2 = args.split(" ")[1]
                self.regs[r1] = self.regs[r1] * self._arg_val(r2)
            case "div":
                r2 = args.split(" ")[1]
                av = self._arg_val(r2)
                if av == 0:
                    self.regs["z"] = 1
                    return False
                self.regs[r1] = self.regs[r1] // av
            case "mod":
                r2 = args.split(" ")[1]
                if self.regs[r1] < 0:
                    self.regs["z"] = 2
                    return False
                av = self._arg_val(r2)
                if av <= 0:
                    self.regs["z"] = 3
                    return False
                self.regs[r1] = self.regs[r1] % av
            case "eql":
                r2 = args.split(" ")[1]
                self.regs[r1] = 1 if self.regs[r1] == self._arg_val(r2) else 0
            case _:
                raise Exception("unknown op")
        return True


def run(lines: list[str], inp: list[int]) -> int:
    alu = Alu(inp)
    for line in lines:
        if not alu.run_instr(line.strip()):
            break
    return alu.regs["z"]


def main() -> None:
    with open("i24.txt", "r") as i:
        lines = i.readlines()
    # inp = [1, 3, 5, 7, 9, 2, 4, 6, 8, 9, 9, 9, 9, 9]
    inp = [1, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    res = run(lines, inp)
    print(res)


def test() -> None:
    txt = ""
    assert run(txt.splitlines()) == 590784


if __name__ == "__main__":
    # test()
    main()
