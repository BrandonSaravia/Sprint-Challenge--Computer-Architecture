"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0b000000000
        self.sp = 244
        self.LDI = 130
        self.PRN = 71
        self.HLT = 1
        self.MUL = 162
        self.PUSH = 69
        self.POP = 70
        self.CALL = 80
        self.ADD = 160
        self.RET = 17
        

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if len(sys.argv) > 1:
            program = []
            file1 = open(sys.argv[1], 'r')
            for text in file1:
                x = text.split()
                instruction = x[0]
                if instruction != "#":
                    program.append(int(instruction, 2))
                    
        else:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

        self.ram *= len(program)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.reg[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""


        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')


    def run(self):
        """Run the CPU."""
        running = True
        # print(sys.argv)
        
        while running:
            IR = self.ram_read(self.pc)

            if (self.pc + 1) <= len(self.ram)-1:
                operand_a = self.ram_read(self.pc + 1)
            if (self.pc + 2) <= len(self.ram)-1:
                operand_b = self.ram_read(self.pc + 2) 

            if IR == self.LDI:
                self.ram_write(operand_b, operand_a)
                self.pc += 3
            elif IR == self.MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            elif IR == self.ADD:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3
            elif IR == self.CALL:
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2
                self.pc = self.reg[operand_a]
            elif IR == self.RET:
                value = self.ram[self.sp]
                self.sp += 1
                self.pc = value
            elif IR == self.PUSH:
                self.sp -= 1
                value = self.reg[operand_a]
                self.ram[self.sp] = value
                self.pc += 2
            elif IR == self.POP:
                pop_value = self.ram[self.sp]
                reg_address = self.ram[self.pc + 1]
                self.reg[reg_address] = pop_value
                self.sp += 1
                self.pc += 2
            elif IR == self.PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == self.HLT:
                running = False
            else:
                self.trace()
                sys.exit(1)