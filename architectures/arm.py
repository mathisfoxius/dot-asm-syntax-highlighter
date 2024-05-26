REGISTERS = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]

CALL_INSTRUCTIONS = [
    "bl",   # Branch with Link
    "blx",  # Branch with Link and Exchange
    "bx",   # Branch and Exchange
    "bxj",  # Branch and Exchange Jazelle
    "blr",  # Branch with Link to Register (ARMv8)
    "br",   # Branch to Register (ARMv8)
    "ret"   # Return from Subroutine (ARMv8)
]
