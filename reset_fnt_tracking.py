import argparse


def modify_fnt_file(input_path, output_path, old_tracking=None, new_tracking=None):
    with open(input_path, "r") as input_file:
        lines = input_file.readlines()

    modified_lines = []

    if new_tracking is not None:
        modified_lines.append(f"tracking={new_tracking}\n")

    for line in lines:
        stripped_line = line.strip()

        # Ignore comments and blank lines
        if stripped_line.startswith("--") or stripped_line == "":
            continue

        # Check for tracking value line
        if line.strip().startswith("tracking"):
            old_tracking = int(stripped_line.split("=")[1])
            continue

        # Modify glyph widths
        parts = stripped_line.split()
        if len(parts) == 2:
            if old_tracking is None:
                raise ValueError("--old-tracking must be specified if the tracking value is missing from the file.")

            glyph, width = parts
            modified_lines.append(f"{glyph}\t{int(width) + old_tracking}\n")
            continue

        # Copy verbatim if nothing matched
        modified_lines.append(line)

    with open(output_path, "w") as output_file:
        output_file.writelines(modified_lines)


def main():
    parser = argparse.ArgumentParser(description="Applies the tracking value to the width of characters in a Playdate "
                                                 ".fnt file.")

    parser.add_argument("input_path", help="Path to the input .fnt file.")
    parser.add_argument("output_path", help="Path to the output .fnt file.")
    parser.add_argument("--old-tracking", type=int, help="Override the old tracking value.")
    parser.add_argument("--new-tracking", type=int, help="Set the new tracking value.")

    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    old_tracking = args.old_tracking
    new_tracking = args.new_tracking

    modify_fnt_file(input_path, output_path, old_tracking, new_tracking)
    print(f"Modified .fnt file saved to {output_path}")


if __name__ == "__main__":
    main()
