from typing import List, Dict


class Interpreter:
    def __init__(self, brainfuck: str):
        self.stack: List[int] = []
        self.memory: List[int] = [0]
        self.memory_pointer: int = 0
        self.action_pointer: int = 0
        self.stdin_buffer = []
        self.brainfuck = brainfuck
        self.actions: Dict = {
            ">": self.advance_in_memory,
            "<": self.return_in_memory,
            "+": self.increase_memory_value,
            "-": self.decrease_memory_value,
            ".": self.print_memory_value,
            ',': self.insert_memory_value,
            "[": self.start_loop,
            "]": self.end_loop
        }

    def advance_in_memory(self) -> None:
        self.memory_pointer += 1
        if self.memory_pointer == len(self.memory):
            self.memory.append(0)

    def return_in_memory(self) -> None:
        self.memory_pointer -= 1
        if self.memory_pointer < 0:
            raise ValueError("Can't jump to memory address -1")

    def increase_memory_value(self) -> None:
        self.memory[self.memory_pointer] += 1

    def decrease_memory_value(self) -> None:
        self.memory[self.memory_pointer] -= 1

    def print_memory_value(self) -> None:
        print(chr(self.memory[self.memory_pointer]), end='')

    def insert_memory_value(self) -> None:
        if len(self.stdin_buffer) == 0:
            std_in: str = input()
            if std_in == "":
                self.stdin_buffer += "\n"
            else:
                self.stdin_buffer += std_in
        self.memory[self.memory_pointer] = ord(self.stdin_buffer.pop(0))

    def start_loop(self) -> None:
        if self.memory[self.memory_pointer] == 0:
            i = 0
            while self.action_pointer < len(self.brainfuck) and self.brainfuck[self.action_pointer] != ']':
                self.action_pointer += 1
                if self.brainfuck[self.action_pointer] == '[':
                    i += 1
                elif i > 0 and self.brainfuck[self.action_pointer] == ']':
                    i -= 1
                    self.action_pointer += 1

            if self.action_pointer == len(self.brainfuck):
                raise RuntimeError('Closing ] not found')
        else:
            self.stack.append(self.action_pointer)

    def end_loop(self) -> None:
        if self.memory[self.memory_pointer] != 0:
            if len(self.stack) > 0:
                self.action_pointer = self.stack.pop(-1) - 1
            else:
                raise RuntimeError('Opening [ not found')
        else:
            self.stack.pop(-1)

    def interpret(self) -> None:
        while self.action_pointer < len(self.brainfuck):
            if self.brainfuck[self.action_pointer] in self.actions:
                self.actions[self.brainfuck[self.action_pointer]]()
            else:
                raise ValueError(f"{self.brainfuck[self.action_pointer]} is not a brainfuck character")
            self.action_pointer += 1
