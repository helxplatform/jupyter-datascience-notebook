import argparse
import os
import shutil
import sys
from eduhelx_utils.custom_logger import CustomizeLogger

config_path=config_path=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'logging_config.json'))
logger = CustomizeLogger.make_logger(config_path)

def validate_paths(src, dest):

    # Check if src directory exists
    if not os.path.exists(src):
        err_msg = f"Source directory {src} does not exist."
        logger.error(err_msg)
        sys.exit(1)

    # Check if dest directory exists
    if os.path.exists(dest):
        err_msg = "Destination directory already exists."
        logger.error(err_msg)
        sys.exit(1)

    # Check if dest directory's dirname is valid
    dest_dirname = os.path.dirname(dest)
    if not os.path.isdir(dest_dirname):
        err_msg = f"Destnation directory's dirname {dest_dirname} is not valid."
        logger.error(err_msg)
        sys.exit(1)

    logger.info("Path validation successful!")



def stage_student_repos(src, dest):

    # Create destination directory
    os.makedirs(dest)

    # Iterate through subdirectories in the source directory
    for subdir in os.scandir(src):
        if subdir.is_dir():
            # Get the name of the subdirectory
            subdir_name = subdir.name

            # Iterate through files in the subdirectory
            for file in os.scandir(subdir.path):
                if file.is_file() and file.name.endswith(".ipynb"):
                    # Get the filename without the extension
                    filename = os.path.splitext(file.name)[0]

                    # Create the new filename
                    new_filename = f"{subdir_name}_{filename}.ipynb"

                    # Copy the .ipynb file to the destination directory with the new filename
                    shutil.copy2(file.path, os.path.join(dest, new_filename))
                    shutil.chown(os.path.join(dest, new_filename), user=otter, group=otter)

    logger.info("Student repositories staged successfully!")

if __name__ == "__main__":

    # To run:  python script_name.py /path/to/source /path/to/destination

    # Create argparse parser
    parser = argparse.ArgumentParser(description="Path validation script")
    parser.add_argument("src", type=str, help="Source directory path")
    parser.add_argument("dest", type=str, help="Destination directory path for staging files to be graded")
    parser.add_argument("--debug", help="Sets the log level to debug when running the script", action="store_true")

    # Parse command-line arguments
    args = parser.parse_args()

    # Set log level to debug
    debug = args.debug
    if debug:
        CustomizeLogger.set_log_level(logger, "debug")

    # Validate paths
    validate_paths(args.src, args.dest)

    # Stage student repositories
    stage_student_repos(args.src, args.dest)
