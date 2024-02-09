import csv
import os
import sys
from eduhelx_utils.api import APIException
from eduhelx_utils.custom_logger import CustomizeLogger
from api import get_api_client

config_path=config_path=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'logging_config.json'))
logger = CustomizeLogger.make_logger(config_path)
    
async def main(roster_file: str, pid_column: str):
    api_client = get_api_client()

    with open(roster_file, "r") as f:
        reader = csv.DictReader(f, delimiter=",")
        rows = [row for row in reader]
    
    for i, student in enumerate(rows, 1):
        pid = student[pid_column]
        # We don't catch errors on this call because if it throws,
        # then the script has failed, we cannot gracefully handle it.
        try:
            student_info = await api_client.get_ldap_user_info(pid)
        except APIException as e:
            exception = Exception(f'({i}) failed to request info for student with pid "{pid}", reason: {e.data["message"]} ({e.error_code}), skipping...')
            logger.error(exception)
        try:
            await api_client.create_student(
                onyen=student_info["onyen"],
                first_name=student_info["first_name"],
                last_name=student_info["last_name"],
                email=student_info["email"]
            )
            logger.info(f'({i}) Created EduHeLx student "{student_info["onyen"]}"')
        except APIException as e:
            logger.error(f'({i}) Student with onyen "{student_info["onyen"]}" already exists, skipping...')

if __name__ == "__main__":
    import argparse
    import asyncio
    parser = argparse.ArgumentParser(description="Import a class roster")
    
    parser.add_argument("--roster_file", type=str, help="Path to class roster CSV file.")
    parser.add_argument("--pid_column", type=str, help="The name of the column that specifies the student's PID")
    parser.add_argument("--debug", help="Sets the log level to debug when running the script", action="store_true")

    args = parser.parse_args()
    roster_file = args.roster_file
    pid_column = args.pid_column

    # Set log level to debug
    debug = args.debug
    if debug:
        CustomizeLogger.set_log_level(logger, "debug")
    
    asyncio.run(main(roster_file, pid_column))
        

