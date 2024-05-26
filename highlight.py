import re
import COLORS

pattern_registers = r'\b(e[abcd]x|[abcd]x|r[abcd]x|[abcd]l|[abcd]h|si|di|sp|bp|ip|rsi|rdi|rbp|rsp|rip|r8|r9|r10|r11|r12|r13|r14|r15|esi|edi|ebp|esp|eip|xmm[0-9]|xmm1[0-5])\b'

def remove_URLs(content):
    return re.sub(r'URL="[^"]*",', "", content)

def change_background(content):
    content = re.sub(r'bgcolor=azure', "", content)
    content = re.sub(r'fillcolor="#c19c00"', f'fillcolor="{COLORS.BACKGROUND}"', content)
    return content

def syntax_highlight_asm(asm_code):
    replacements = [
        (r'\b(mov)\b', r'<font color="%s">\1</font>' % COLORS.MOV),
        (pattern_registers, r'<font color="%s">\1</font>' % COLORS.REGISTERS),
        (r'\b(0x[0-9a-fA-F]+)\b', r'<font color="%s">\1</font>' % COLORS.NUMBERS_AND_ADDRESSES),
        (r'\b(call)\b', r'<font color="%s"><b>\1</b></font>' % COLORS.CALL)
    ]
    asm_code = asm_code.replace('\l', '<BR ALIGN="LEFT"/>')

    for pattern, replacement in replacements:
        asm_code = re.sub(pattern, replacement, asm_code)
    return asm_code

def preprocess_dot_file(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    content = remove_URLs(content)
    content = change_background(content)

    asm_pattern = re.compile(r'label="(.*?)"\](?:\\n|\x0a|\Z)')

    highlighted_content = asm_pattern.sub(lambda x: f'label=<{syntax_highlight_asm(x.group(1))}>];\n', content)

    with open(output_file, 'w') as file:
        file.write(highlighted_content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python highlight.py input.dot output.dot")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    preprocess_dot_file(input_file, output_file)

