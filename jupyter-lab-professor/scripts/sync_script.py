import argparse
import requests
import json
import os
import shutil
import sys
import subprocess
from pathlib import Path
from datetime import datetime

from eduhelx_utils.custom_logger import CustomizeLogger

config_path=config_path=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'logging_config.json'))
logger = CustomizeLogger.make_logger(config_path)

gitea_url = os.environ.get('GITEA_URL')
grader_api_host = os.environ.get('GRADER_API_HOST')
grader_api_port = os.environ.get('GRADER_API_PORT')
grader_api_url  = f"{grader_api_host}:{grader_api_port}"

def checkout_commit_id(onyen, commit_id):

    logger.info(f"Checking out commit_id {commit_id} for {onyen}")

    try:
        stdout = subprocess.run(['git', 'checkout', commit_id], check=True, capture_output=True, text=True).stdout
        logger.info(f"Successfully checked out {commit_id} for {onyen}.\n Output:\n {stdout}")
    except subprocess.CalledProcessError as ex:
        logger.error(f"CalledProcessError:\n {ex}")
    except OSError as ex:
        logger.error(f"OSError:\n {ex}")
    except Exception as ex:
        logger.error(f"Unexpected exception:\n {ex}")



def get_last_commit_id_for_assignment(assignment, onyen):

    commit_id = ""
    try:
        url = f"http://{grader_api_url}/api/v1/latest_submission?onyen={onyen}&assignment_id={assignment}"

        logger.info(f"Getting last_commit_id for onyen={onyen} assignment={assignment}")

        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        commit_id = json_data['commit_id']

        logger.info(f"Successfully retrieved commit_id {commit_id} for onyen {onyen}")

    except requests.HTTPError:
        logger.error(f"API request received status code: {response.status_code}")
    except requests.Timeout:
        logger.error(f"API request timed out.")
    except Exception as ex:
        logger.error(f"Unexpected exception:\n {ex}")

    return commit_id


def get_course():

    course_name = ""
    try:
        url = f"http://{grader_api_url}/api/v1/course"

        logger.info(f"Getting course name with API url: {url}")

        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        course_name = json_data['name']

        logger.info(f"Successfully retrieved course name {course_name}")

    except requests.HTTPError:
        logger.error(f"Course API request received status code: {response.status_code}")
        sys.exit(1)
    except requests.Timeout:
        logger.error("Course API request timed out.")
        sys.exit(1)
    except Exception as ex:
        logger.error(f"Unexpected exception:\n {ex}")
        sys.exit(1)

    return course_name.lower()


def change_directory(new_directory):

    prev_dir = os.getcwd()
    logger.info(f"Changing working directory from {prev_dir} to {new_directory}")

    try:
        os.chdir(new_directory)
        logger.info(f"Successfully changed working directory to {os.getcwd()}.")
    except (FileNotFoundError, NotADirectoryError):
        logger.error(f"Directory {new_directory} does not exist or is not a directory.")
    except NotADirectoryError as ex:
        logger.error(f"{new_directory} is not a directory")
    except PermissionError as ex:
        logger.error(f"You do not have permissions to change to {new_directory}.")
    except Exception as ex:
        logger.error(f"Unexpected exception:\n {ex}")

    return prev_dir


def clone_repo(onyen, repo_name):

    logger.info(f"Cloning repo for student {onyen}")
    parent_dir = os.path.dirname(os.getcwd())
    student_repo_dir = Path(f"{parent_dir}/{onyen}")

    if os.path.exists(student_repo_dir.as_posix()) and os.path.isdir(student_repo_dir.as_posix()):
        logger.debug(f".git directory already exists for {onyen}/{repo_name}. Deleting existing directory.")
        try:
            shutil.rmtree(student_repo_dir.as_posix())
        except OSError as ex:
            logger.error(f"Failed to delete directory {student_repo_dir.as_posix}\n Error:\n {ex}")
    try:
        logger.debug(f"Creating directory {student_repo_dir.as_posix()}")
        student_repo_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created directory student_repo_dir: {student_repo_dir.as_posix()}")
    except OSError as ex:
        logger.error(f"Error creating repo dir {student_repo_dir.as_posix()}\n Error:\n {ex}")
    except Exception as ex:
        logger.error(f"Unexpected exception:\n {ex}")

    # Change to repo dir
    logger.debug(f"Changing directory to student_repo_dir: {student_repo_dir.as_posix()}")
    cur_dir = change_directory(student_repo_dir.as_posix())

    try:
        # Clone into directory named by student onyen
        git_url = f"{gitea_url}/{onyen}/{repo_name}.git"
        logger.info(f"Cloning git url {git_url}")
        stdout = subprocess.run(['git', 'clone', git_url, student_repo_dir.as_posix() + '/' + repo_name], check=True, capture_output=True, text=True).stdout
        logger.info(f"Successfully cloned {onyen}/{repo_name} repo.\n Output:\n {stdout}")
    except subprocess.CalledProcessError as ex:
        logger.error(f"CalledProcessError:\n {ex}")
    except OSError as ex:
        logger.error(f"OSError:\n {ex}")
    except Exception as ex:
        logger.error(f"Unexpected exception:\n {ex}")


def checkout_latest_commits_for_assignment(assignment, onyen_list):

    start_dir = os.getcwd()
    parent_dir = os.path.dirname(os.getcwd())
    logger.debug(f"Current working directory: {parent_dir}")

    repo_name = get_course().lower()
    for onyen in onyen_list:
        clone_repo(onyen, repo_name)
        logger.debug(f"Repo cloned, changing into repo directory: {parent_dir}/{onyen}/{repo_name}")
        prev_dir = change_directory(f"{parent_dir}/{onyen}/{repo_name}")
        commit_id = get_last_commit_id_for_assignment(assignment, onyen)
        checkout_commit_id(onyen, commit_id)
        rc = change_directory(start_dir)


def get_course_onyens():

    url = f"http://{grader_api_url}/api/v1/students"
    logger.info(f"Calling grader api url: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        onyens = [student['onyen'] for student in json_data]
    except requests.HTTPError as ex:
        logger.error(f"API request received status code: {response.status_code}\n Error:\n {ex}")
        sys.exit(1)
    except requests.Timeout:
        logger.error(f"API request timed out.")
        sys.exit(1)
    except Exception as ex:
        logger.error(f"Unexpected exception:\n {ex}")
        sys.exit(1)

    logger.info(f"Returning onyen list: {onyens}")
    return onyens


def main():

    parser = argparse.ArgumentParser(description="(Check out given assignment by commit id")
    parser.add_argument("assignment", type=int, help="Assignment number")
    parser.add_argument("-o", "--onyen", type=str, nargs='+', help="Optional Onyens (string). \
                        One or more onyens separated by spaces. To operate on  all onyens, \
                        omit this parameter.")
    parser.add_argument("--debug", help="Sets the log level to debug when running the script", action="store_true")

    args = parser.parse_args()

    if args.debug:
        CustomizeLogger.set_log_level(logger, "debug")

    if not args.onyen:
        onyen_list = get_course_onyens()
    else:
        onyen_list = args.onyen

    logger.info(f"Onyen list={onyen_list}")

    # Clone repo and checkout each onyen's latest commit id for assignment
    checkout_latest_commits_for_assignment(args.assignment, onyen_list)


if __name__ == "__main__":
    main()
