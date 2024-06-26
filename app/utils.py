import math
import os
import re

from .logger import get_logger

logger = get_logger(__name__)


def delete_file(file_path):
    """
    Deletes a file if it exists.

    Args:
        file_path (str): Path to the file.

    Returns:
        bool: True if the file was successfully deleted or didn't exist, False otherwise.
    """
    try:
        os.remove(file_path)
        return True
    except FileNotFoundError:
        return True
    except OSError as e:
        print(f"Error deleting {file_path}: {e.strerror}")
        return False


def clean_file_name(title):
    """
    Clean the title to make it safe for use as a file name.

    Args:
        title (str): The title to clean.

    Returns:
        str: The cleaned file name.
    """
    # Remove special characters and replace spaces and dots with underscores
    cleaned_title = re.sub(r"[^a-zA-Z0-9\s.]", "_", title)
    # Remove consecutive underscores
    cleaned_title = re.sub(r"_+", "_", cleaned_title)
    # Remove leading and trailing underscores
    cleaned_title = cleaned_title.strip("_").replace(" ", "")
    return cleaned_title


def create_directory(directory: str) -> None:
    """
    Create a directory if it does not exist.

    Args:
        directory (str): The directory path to create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


class DirectoryManager:
    """
    A context manager for managing directories. It ensures the directory exists
    and provides a list of file paths within the directory.

    Attributes:
        directory (str): The path to the directory to be managed.

    Methods:
        __enter__(): Checks if the directory exists and returns a list of file paths.
        __exit__(exc_type, exc_value, traceback): Logs any exceptions that occur within the context.
    """

    def __init__(self, directory):
        """
        Initializes the DirectoryManager with the given directory path.

        Args:
            directory (str): The path to the directory to be managed.
        """
        self.directory = directory

    def __enter__(self):
        """
        Checks if the directory exists and returns a list of file paths.

        Returns:
            list: A list of file paths within the directory.

        Raises:
            FileNotFoundError: If the directory does not exist.
        """
        if not os.path.exists(self.directory):
            raise FileNotFoundError(f"Directory '{self.directory}' does not exist.")

        file_paths = []
        for file_name in os.listdir(self.directory):
            file_path = os.path.join(self.directory, file_name)
            if os.path.isfile(file_path):
                file_paths.append(file_path)

        return file_paths

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Logs any exceptions that occur within the context.

        Args:
            exc_type (type): The exception type.
            exc_value (Exception): The exception instance.
            traceback (traceback): The traceback object.
        """
        if exc_type is not None:
            logger.exception(f"An error occurred: {exc_value}")


def get_file_name_without_extension(file_path: str) -> str:
    """
    Extract the file name without extension from the given file path.

    Args:
        file_path (str): The path of the file.

    Returns:
        str: The file name without extension.

    Example:
        If file_path is '/path/to/file.txt', the function returns 'file'.
    """
    file_name_with_extension = os.path.basename(file_path)
    file_name_without_extension, _ = os.path.splitext(file_name_with_extension)
    return file_name_without_extension


def format_time(seconds: float) -> str:
    """
    Formats a time duration given in seconds into the HH:MM:SS,MMM format.

    Args:
        seconds (float): Time duration in seconds.

    Returns:
        str: Formatted time string in the format HH:MM:SS,MMM.
    """
    sign = "-" if seconds < 0 else ""
    seconds = abs(seconds)

    hours = math.floor(seconds / 3600)
    seconds %= 3600

    minutes = math.floor(seconds / 60)
    seconds %= 60

    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)

    formatted_time = f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    return formatted_time


def create_directory_for_file(file_path: str) -> None:
    """
    Create the directory for the given file path if it does not exist.

    Args:
        file_path (str): The file path for which to create the directory.
    """
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)


def is_video_file(file_path: str) -> bool:
    """
    Check if the file at the given path is a video file.

    Args:
        file_path (str): The path to the file to check.

    Returns:
        bool: True if the file is a video file, False otherwise.
    """
    video_extensions = [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm", ".m4v"]
    file_extension = os.path.splitext(file_path)[1].lower()
    return file_extension in video_extensions
