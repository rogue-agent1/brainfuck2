#!/usr/bin/env python3
"""brainfuck2 - Brainfuck interpreter with optimizations and bounded tape."""
import sys

def interpret(code, input_str="", tape_size=30000, max_steps=1000000):
    code = [c for c in code if c in "+-<>.,[]"]
    tape = [0] * tape_size
    ptr = 0
    ip = 0
    inp_pos = 0
    output = []
    steps = 0
    # Precompute bracket pairs
    brackets = {}
    stack = []
    for i, c in enumerate(code):
        if c == "[": stack.append(i)
        elif c == "]":
            j = stack.pop()
            brackets[j] = i
            brackets[i] = j
    while ip < len(code) and steps < max_steps:
        c = code[ip]
        if c == "+": tape[ptr] = (tape[ptr] + 1) & 255
        elif c == "-": tape[ptr] = (tape[ptr] - 1) & 255
        elif c == ">": ptr = (ptr + 1) % tape_size
        elif c == "<": ptr = (ptr - 1) % tape_size
        elif c == ".": output.append(chr(tape[ptr]))
        elif c == ",":
            tape[ptr] = ord(input_str[inp_pos]) if inp_pos < len(input_str) else 0
            inp_pos += 1
        elif c == "[" and tape[ptr] == 0: ip = brackets[ip]
        elif c == "]" and tape[ptr] != 0: ip = brackets[ip]
        ip += 1
        steps += 1
    return "".join(output)

def test():
    # Hello World
    hw = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    assert interpret(hw).startswith("Hello World")
    # cat (echo input)
    assert interpret(",.,.", input_str="AB") == "AB"
    # Simple add: 2+3
    assert interpret("++>+++<[->+<]>.", input_str="") == chr(5)
    print("brainfuck2: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: brainfuck2.py --test")
