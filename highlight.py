import re
import COLORS

COLOR_PALETTE = COLORS.light

pattern_registers = r'\b(e[abcd]x|[abcd]x|r[abcd]x|[abcd]l|[abcd]h|si|di|sp|bp|ip|rsi|rdi|rbp|rsp|rip|r8|r9|r10|r11|r12|r13|r14|r15|esi|edi|ebp|esp|eip|xmm[0-9]|xmm1[0-5])\b'

def replace_URLs_with_fontcolors(content):
    return re.sub(r'URL="[^"]*",', f'fontcolor="{COLOR_PALETTE.DEFAULT}"', content)

def change_background(content):
    content = re.sub(r'bgcolor=azure', f'bgcolor="{COLOR_PALETTE.BACKGROUND}"', content)
    content = re.sub(r'fillcolor="#c19c00"','', content)
    content = re.sub(r'fillcolor=white', f'color="{COLOR_PALETTE.DEFAULT}", fillcolor="{COLOR_PALETTE.BOX_COLOR}"', content)
    return content

def remove_default_fontcolor(content):
    return re.sub(r'fontcolor="[^"]*",', "", content)

def syntax_highlight_asm(asm_code):
    replacements = [
        (r'\b(mov)\b', r'<font color="%s">\1</font>' % COLOR_PALETTE.MOV),
        (pattern_registers, r'<font color="%s">\1</font>' % COLOR_PALETTE.REGISTERS),
        (r'\b(0x[0-9a-fA-F]+)\b', r'<font color="%s">\1</font>' % COLOR_PALETTE.NUMBERS_AND_ADDRESSES),
        (r'\b(call)\b', r'<font color="%s"><b>\1</b></font>' % COLOR_PALETTE.CALL)
    ]
    asm_code = asm_code.replace('\l', '<BR ALIGN="LEFT"/>')

    for pattern, replacement in replacements:
        asm_code = re.sub(pattern, replacement, asm_code)
    return asm_code

def preprocess_dot_file(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    content = remove_default_fontcolor(content)
    content = replace_URLs_with_fontcolors(content)
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

