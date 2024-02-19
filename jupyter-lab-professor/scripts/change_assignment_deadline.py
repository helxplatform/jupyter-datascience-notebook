import os
import requests
import sys
from dateutil.parser import parse
from eduhelx_utils.custom_logger import CustomizeLogger
from api import get_api_client

config_path=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'logging_config.json'))
logger = CustomizeLogger.make_logger(config_path)

if __name__ == "__main__":
    import argparse
    import asyncio
    parser = argparse.ArgumentParser(description="Modify the deadline of an assignment")
    
    parser.add_argument("--assignment_name", type=str, help="The name of the assignment")
    parser.add_argument("--new_deadline", type=str, help="The new deadline of the assignment, use \"null\" to unset the deadline.")
    parser.add_argument("--debug", help="Sets the log level to debug when running the script", action="store_true")

    args = parser.parse_args()
    assignment_name = args.assignment_name
    new_deadline = args.new_deadline
    debug = args.debug

    if assignment_name == None:
        print("Error: assignment_name is required")
        sys.exit(1)
    if new_deadline == None:
        print("Error: new_deadline is required")
        sys.exit(1)
    if debug:
        CustomizeLogger.set_log_level(logger, "debug")

    if new_deadline.lower() == "null" or new_deadline.lower() == "none":
        new_deadline = None
    else:
        try:
            parse(new_deadline)
        except ValueError:
            print('Error: Invalid date format for new deadline. Example format: "2012-01-19 17:21:00 EST"')
            sys.exit(1)

    try:
        api = get_api_client()
        res = asyncio.run(api.update_assignment(assignment_name, {
            "due_date": new_deadline
        }))
    except Exception as e:
        logger.error("Error: " + str(e))
        sys.exit(1)

    if res.status_code != 200:
        logger.error("Error: API endpoint returned status code: " + str(res.status_code))
        sys.exit(1)

    logger.info("Success: Deadline for assignment " + assignment_name + " changed to " + new_deadline)
