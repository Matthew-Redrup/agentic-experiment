from agentic_edu.modules.rand import generate_session_id
from datetime import datetime
import re


def test_generate_session_id():
    session_id = generate_session_id("get jobs with 'Completed' or 'Started' status")
    assert isinstance(session_id, str), "The session id must be a string"
    assert session_id.startswith(
        "get_jobs_with_completed_or_sta"
    ), "The session id must start with the truncated prompt"
    assert re.search(
        r"__\d{2}_\d{2}_\d{2}$", session_id
    ), "The session id must end with '__HH_MM_SS'"


def test_generate_session_id_empty_string():
    session_id = generate_session_id("")
    assert session_id.endswith(
        "__" + datetime.now().strftime("%H_%M_%S")
    ), "The session id must end with '__HH_MM_SS'"


def test_generate_session_id_special_chars():
    session_id = generate_session_id("get jobs with 'Completed' or 'Started' status!")
    assert session_id.startswith(
        "get_jobs_with_completed_or_sta"
    ), "The session id must start with the truncated prompt"
    assert session_id.endswith(
        "__" + datetime.now().strftime("%H_%M_%S")
    ), "The session id must end with '__HH_MM_SS'"


def test_generate_session_id_long_string():
    session_id = generate_session_id(
        "get jobs with 'Completed' or 'Started' status and 'Pending' or 'Failed'"
    )
    assert session_id.startswith(
        "get_jobs_with_completed_or_sta"
    ), "The session id must start with the truncated prompt"
    assert session_id.endswith(
        "__" + datetime.now().strftime("%H_%M_%S")
    ), "The session id must end with '__HH_MM_SS'"
