import os
from pathlib import Path
from typing import Optional, Union

from email_validator import EmailNotValidError

from smtpymailer.validation import validate_user_email


def find_project_root(marker: Optional[Union[str, list]] = None) -> Optional[Path]:
    """
    Traverse up from the current path until a directory containing the marker is found.

    Args:
        marker (Optional[Union[str, list]]): A string or a list of strings representing the file(s) or directory names to look for.
                                             If not provided, defaults to [".git", "setup.py", "requirements.txt", "README.md"].

    Returns:
        Optional[Path]: The path to the directory containing the marker, or None if not found.
    """
    if marker is None:
        marker = [".git", "setup.py", "requirements.txt", "README.md"]
    elif isinstance(marker, str):
        marker = [marker]

    current_file_path = Path(__file__).resolve()
    for parent in current_file_path.parents:
        if any((parent / m).exists() for m in marker):
            return parent

    return None


def is_file_with_path(path: str) -> bool:
    """
    Args:
        path: A string representing the path to the file.

    Return:
        A boolean value indicating whether the file exists at the specified path.

    Description:
        This method takes a path parameter and checks if the file exists at that path.
        It converts the given path to an absolute path using `os.path.abspath` function.
        Then, it uses `os.path.isfile` function to determine whether the absolute path refers to a file.
        The method returns `True` if the file exists at the specified path, and `False` otherwise.

    """
    absolute_path = os.path.abspath(path)
    return os.path.isfile(absolute_path)


def ensure_list(value: any) -> list:
    """
    Ensures that the given value is a list.

    Args:
        value (any): The recipient to be checked and converted to a list if necessary.

    Returns:
        list: The recipient as a list.

    """
    if value is None:
        return []
    return [value] if not isinstance(value, list) else value


def recipients_to_str(recipients):
    """
    Converts the recipients list to a string representation.

    Args:
        recipients: A list of recipients.

    Returns:
        A string representation of the recipients list, with each recipient separated by a comma and space.
        If the recipients list is empty, an empty string is returned.
    """
    return ", ".join(ensure_list(recipients)) if recipients else ""


def convert_bool(val):
    """
    Converts a string to a boolean value.

    Args:
        val (str): The string to convert.

    Returns:
        bool: True if the string is "True", False otherwise.
    """
    return val in ["True", "true", 1, "1", "Yes", "yes", "Y", "y", True]


def validate_and_extend(all_recipients: list, recipient_type: Union[str, list]):
    """
    Validates and extends the all_recipients list with validated email addresses. If a recipient type is provided
    as a string or list, it is first normalized into a list format. Each email address in this list is then validated.
    Valid email addresses are appended to the all_recipients list. If an invalid email is found, an error is raised.

    Args:
        all_recipients (list): The main list of all recipients that will be extended with validated emails.
        recipient_type (Union[str, list]): A string or list of email addresses to validate and add to all_recipients.

    Raises:
        EmailNotValidError: If any of the email addresses in recipient_type is not valid.

    """

    if recipient_type:
        recipient_list = ensure_list(recipient_type)
        for email in recipient_list:
            if validate_user_email(email):
                all_recipients.append(email)


def build_all_recipients_and_validate(
    recipients: Union[str, list],
    cc_recipients: Optional[Union[str, list]] = None,
    bcc_recipients: Optional[Union[str, list]] = None,
):
    """
    Constructs a complete list of validated email addresses for an email, including To, CC, and BCC recipients.
    It takes individual or lists of email addresses for each category, normalizes them, and then validates each email.
    All valid email addresses across these categories are compiled into a single list. An error is raised if any email
    address is found to be invalid.

    Args:
        recipients (Union[str, list]): A string or list of email addresses for the 'To' recipients.
        cc_recipients (Optional[Union[str, list]]): Optionally, a string or list of email addresses for
            the 'CC' recipients.
        bcc_recipients (Optional[Union[str, list]]): Optionally, a string or list of email addresses for
            the 'BCC' recipients.

    Returns:
        list: A list of all validated email addresses across the To, CC, and BCC fields.

    Raises:
        EmailNotValidError: If any of the provided email addresses are not valid.
    """
    if not len(ensure_list(recipients)) > 0:
        raise ValueError("No recipients provided")

    all_recipients = []
    for recipient_type in [recipients, cc_recipients, bcc_recipients]:
        validate_and_extend(all_recipients, recipient_type)

    return all_recipients
