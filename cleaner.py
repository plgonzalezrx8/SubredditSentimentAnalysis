import glob
import os


def clean_empty_lines(filename):
    """Remove empty lines from a file."""
    print(f"Cleaning whitespace from {filename}")

    try:
        # Read file contents
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Filter out empty lines
        cleaned_lines = [line for line in lines if line.strip()]

        # Write cleaned contents back to file
        with open(filename, "w", encoding="utf-8") as file:
            file.writelines(cleaned_lines)

        print(f"Successfully cleaned {filename}")

    except IOError as e:
        print(f"Error processing {filename}: {e}")
    except Exception as e:
        print(f"Unexpected error processing {filename}: {e}")


def main():
    # Get all txt files in the parsed_comments directory
    parsed_comments_dir = "parsed_comments"
    txt_files = glob.glob(os.path.join(parsed_comments_dir, "*.txt"))

    if not txt_files:
        print(f"No text files found in {parsed_comments_dir}")
        return

    print(f"Found {len(txt_files)} text files to clean")

    # Clean each file
    for file in txt_files:
        clean_empty_lines(file)

    print("Cleaning process completed")


if __name__ == "__main__":
    main()
