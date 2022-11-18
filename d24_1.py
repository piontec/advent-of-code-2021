from typing import List


class ALU:
    def __init__(self, code_lines: List[str], inputs: List[int]):
        self._ip: int = 0
        self._input_index = 0
        self._code_lines = code_lines
        self._inputs = inputs
        self._regs = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }

    def _run_instruction(self) -> None:
        instruction = self._code_lines[self._ip].strip('\n')
        self._ip += 1
        us = instruction.split(" ")
        op = us[0]
        args = us[1:]
        if op == "inp":
            self._regs[args[0]] = self._inputs[self._input_index]
            self._input_index += 1
        else:
            val = self._regs[args[1]] if args[1] in self._regs.keys() else int(args[1])
            if op == "add":
                self._regs[args[0]] += val
            elif op == "mul":
                self._regs[args[0]] *= val
            elif op == "div":
                if val == 0:
                    raise ZeroDivisionError()
                self._regs[args[0]] //= val
            elif op == "mod":
                if val <= 0:
                    raise ValueError(f"wrong b arg of mod: {val}")
                if self._regs[args[0]] < 0:
                    raise ValueError(f"wrong a arg of mod: {val}")
                self._regs[args[0]] %= val
            elif op == "eql":
                self._regs[args[0]] = int(self._regs[args[0]] == val)
            else:
                raise ValueError(f"Wrong op: {op}")

    def run(self) -> None:
        while self._ip < len(self._code_lines):
            self._run_instruction()


def main() -> None:
    with open("i24.txt") as f:
        lines = f.readlines()
    low = 11111111111111
    high = 99999999999999
    res = 0
    while True:
        mid = low + (high - low) // 2
        while "0" in str(mid):
            mid += 1
        if low >= mid:
            res = high
            break
        if mid >= high:
            res = low
            break
        inputs = [int(c) for c in str(mid)]
        alu = ALU(lines, inputs)
        alu.run()
        if alu._regs["z"] == 0:
            low = mid
        else:
            high = mid
    print(res)


def test() -> None:
    code = """inp z
inp x
mul z 3
eql z x""".splitlines()
    alu = ALU(code, [1, 3])
    alu.run()
    assert alu._regs["z"] == 1


if __name__ == "__main__":
    test()
    main()
