import os
from pathlib import Path
from eduhelx_utils import api

secret_path = Path("/etc/jlp-credential-secret")

api_host = os.environ["GRADER_API_HOST"]
api_port = int(os.environ["GRADER_API_PORT"])

api_url = f"http://{api_host}:{api_port}/"

def get_api_client() -> api.Api:
    class_secret_path = secret_path
    with open(class_secret_path / "onyen", "r") as f:
        onyen = f.read().strip()
    with open(class_secret_path / "password", "r") as f:
        password = f.read().strip()
    return api.Api(
        api_url=api_url,
        user_onyen=onyen,
        user_autogen_password=password,
    )