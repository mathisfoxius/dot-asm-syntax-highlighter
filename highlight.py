#!/usr/bin/env python3

import re
import COLORS
import architectures.arm as arm
import architectures.x64 as x64


COLOR_PALETTE = COLORS.light
ARCH = "x64"


def replace_URLs_with_fontcolors(content):
    return re.sub(r'URL="[^"]*",', f'fontcolor="{COLOR_PALETTE.DEFAULT}"', content)


def change_background(content):
    content = re.sub(r"bgcolor=azure", f'bgcolor="{COLOR_PALETTE.BACKGROUND}"', content)
    content = re.sub(r'fillcolor="#c19c00"', "", content)
    content = re.sub(
        r"fillcolor=white",
        f'color="{COLOR_PALETTE.DEFAULT}", fillcolor="{COLOR_PALETTE.BOX_COLOR}"',
        content,
    )
    return content


def remove_default_fontcolor(content):
    return re.sub(r'fontcolor="[^"]*",', "", content)


def syntax_highlight_asm(asm_code):
    if ARCH == "x64":
        pattern_registers = r"\b(" + "|".join(x64.REGISTERS) + r")\b"
        pattern_call = r"\b(" + "|".join(x64.CALL_INSTRUCTIONS) + r")\b"
    elif ARCH == "arm":
        pattern_registers = r"\b(" + "|".join(arm.REGISTERS) + r")\b"
        pattern_call = r"\b(" + "|".join(arm.CALL_INSTRUCTIONS) + r")\b"

    replacements = [
        (r"\b(mov)\b", r'<font color="%s">\1</font>' % COLOR_PALETTE.MOV),
        (
            pattern_registers,
            r'<font color="%s">\1</font>' % COLOR_PALETTE.REGISTERS,
        ),
        (
            r"\b(0x[0-9a-fA-F]+)\b",
            r'<font color="%s">\1</font>' % COLOR_PALETTE.NUMBERS_AND_ADDRESSES,
        ),
        (pattern_call, r'<font color="%s"><b>\1</b></font>' % COLOR_PALETTE.CALL),
    ]

    asm_code = asm_code.replace("\l", '<BR ALIGN="LEFT"/>')

    for pattern, replacement in replacements:
        asm_code = re.sub(pattern, replacement, asm_code)
    return asm_code


def preprocess_dot_file(input_file, output_file):
    with open(input_file, "r") as file:
        content = file.read()

    content = remove_default_fontcolor(content)
    content = replace_URLs_with_fontcolors(content)
    content = change_background(content)

    asm_pattern = re.compile(r'label="(.*?)"\](?:\\n|\x0a|\Z)')

    highlighted_content = asm_pattern.sub(
        lambda x: f"label=<{syntax_highlight_asm(x.group(1))}>];\n", content
    )

    with open(output_file, "w") as file:
        file.write(highlighted_content)


def main(input_file, arm=False):
    if arm:
        global ARCH
        ARCH = "arm"
    preprocess_dot_file(input_file, output_file="output.dot")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Process an input file with an optional architecture."
    )

    # Positional argument for the input file
    parser.add_argument("input_file", type=str, help="The input file to be processed")

    # Optional argument for the architecture
    parser.add_argument(
        "--arm", action="store_true", help="Specify if ARM architecture is to be used"
    )

    args = parser.parse_args()

    main(args.input_file, args.arm)
