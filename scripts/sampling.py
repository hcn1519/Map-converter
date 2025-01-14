import os
import random
import argparse
import shutil
from pathlib import Path

def randomly_select_files(directory, num_files=1, extension="00000"):
    """Randomly select a specified number of files with a specific extension from a directory, including its subdirectories."""

    all_files = list(Path(directory).rglob(f"*.{extension}"))
    if len(all_files) == 0:
        return []
    selected_files = random.sample(all_files, min(len(all_files), num_files))
    return selected_files


def copy_files(files, target_directory):
    """Copy selected files to the target directory."""
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    print(f"Copy {len(files)}")
    
    for i, file in enumerate(files):
        file_name, file_extension = os.path.splitext(os.path.basename(file))
        new_file_name = f"{i}_{file_name}{file_extension}"
        target_path = os.path.join(target_directory, new_file_name)
        shutil.copy(file, target_path)
        print(f"Copied {file} to {target_path}")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=
        'Randomly select and copy files with a specific extension from a specified directory.'
    )
    parser.add_argument('directory',
                        type=str,
                        help='The directory to search for files.')
    parser.add_argument('num_files',
                        type=int,
                        help='The number of files to randomly select.')
    parser.add_argument('target_directory',
                        type=str,
                        help='The directory to copy the selected files to.')
    parser.add_argument('-e',
                        '--extension',
                        type=str,
                        default=".00000",
                        help='File extension to filter by (default is .00000)')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.num_files < 1:
        print("Please specify at least one file.")
    else:
        selected_files = randomly_select_files(args.directory, args.num_files,
                                               args.extension)
        if not selected_files:
            print("No files found with the specified extension.")
        else:
            print("Randomly selected files:")
            for file in selected_files:
                print(file)
            copy_files(selected_files, args.target_directory)
