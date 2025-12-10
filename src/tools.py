import os
import subprocess
from typing import Optional

from .file_tracker import FileTracker
from .log import get_logger
from .spinner import spin_context

logger = get_logger(__name__)

FUNCTION_DECLARATIONS = [
    {
        "name": "read_text_file",
        "description": (
            "Reads as text file contents. Use this when you want to see file "
            "contents. Do no use to read a directory."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to read.",
                },
            },
            "required": ["path"],
        },
    },
    {
        "name": "list_files",
        "description": (
            "Lists files (not directories) at a given path. Use this to know "
            "what files are inside a directory. If no path is provided, lists "
            "files in the current directory."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "dirpath": {
                    "type": "string",
                    "description": (
                        "Path of the directory of which the files will be "
                        "listed."
                    ),
                },
            },
            "required": ["dirpath"],
        },
    },
    {
        "name": "list_directories",
        "description": (
            "Lists sub-directories/folders (not files) at a given path. If "
            "no path is provided, lists sub-directories/folders in the "
            "current directory."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "dirpath": {
                    "type": "string",
                    "description": (
                        "Path of the directory of which sub-directories will "
                        "be listed."
                    ),
                },
            },
            "required": ["dirpath"],
        },
    },
    {
        "name": "shell",
        "description": (
            "Runs a shell command on a Linux system. Returns standard output "
            "and standard error. Do not run `rm`, `rmdir`, or `mv`."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "args": {
                    "type": "string",
                    "description": "Shell command to run. For example: ls -l.",
                },
            },
            "required": ["args"],
        },
    },
    {
        "name": "edit_file",
        "description": (
            "Makes edits to a text file. Replaces 'old_str' with 'new_str' in "
            "the given file. 'old_str' and 'new_str' MUST be different from "
            "each other. If the file specified by 'path' does not exist, it "
            "will be created."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to edit.",
                },
                "old_str": {
                    "type": "string",
                    "description": (
                        "Text to search for. Must match exactly and must have "
                        "only one match."
                    ),
                },
                "new_str": {
                    "type": "string",
                    "description": "Text to replace 'old_str' with.",
                },
            },
            "required": ["path", "old_str", "new_str"],
        },
    },
    {
        "name": "code_search",
        "description": (
            "Search for code patterns using ripgrep (rg). Use this to find "
            "code patterns, function definitions, variable usage, or any text "
            "in the codebase. You can search by pattern, file type, or "
            "directory."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "The search pattern or regex to look for",
                },
                "path": {
                    "type": "string",
                    "description": (
                        "Optional path to search in (file or directory)."
                    ),
                },
                "file_type": {
                    "type": "string",
                    "description": (
                        "Optional file extension to limit search to (e.g. py, "
                        "js, go)."
                    ),
                },
                "case_sensitive": {
                    "type": "boolean",
                    "description": (
                        "Weather the search should be case-sensitive. Default "
                        "false."
                    ),
                },
            },
            "required": ["pattern", "path"],
        },
    },
]


def read_text_file(path: str) -> str:
    with spin_context(f"Reading {path}"):
        with open(path) as fi:
            return fi.read()


def list_files(dirpath: str = ".") -> list[str]:
    dirpath = os.path.realpath(dirpath or ".")
    with spin_context(f"Listing files in {dirpath}"):
        return [
            path
            for path in os.listdir(dirpath)
            if os.path.isfile(os.path.join(dirpath, path))
        ]


def list_directories(dirpath: str = ".") -> list[str]:
    dirpath = os.path.realpath(dirpath or ".")
    with spin_context(f"Listing directories in {dirpath}"):
        return [
            path
            for path in os.listdir(dirpath)
            if os.path.isdir(os.path.join(dirpath, path))
        ]


def shell(args: str) -> str:
    # Use shell to be able to use pipe.
    # args is string because we use shell.
    with spin_context(f"Executing '{args}'"):
        result = subprocess.run(
            args, capture_output=True, text=True, shell=True
        )
        if result.stderr:
            raise RuntimeError(result.stderr)
        return result.stdout


def edit_file(path: str, old_str: str, new_str: str) -> Optional[str]:
    with spin_context(f"Editing {path}"):
        return _edit_file(path, old_str, new_str)


def _edit_file(path: str, old_str: str, new_str: str) -> Optional[str]:
    if old_str == new_str:
        raise ValueError("new_str must be different from old_str")

    if old_str == "":
        with open(path, "a") as fi:
            fi.write(new_str)
        return "Success"

    with open(path) as fi:
        file_contents = fi.read()

    count = file_contents.count(old_str)
    if count == 0:
        raise ValueError(f"no match for old_str in file {path}")
    if count > 1:
        raise ValueError(
            f"old_str found {count} times in file {path}, must be unique"
        )

    with open(path, "w") as fi:
        fi.write(file_contents.replace(old_str, new_str))

    return "Success"


def code_search(
    pattern: str,
    path: str = ".",
    file_type: str = "",
    case_sensitive: bool = False,
) -> tuple[str, str]:
    args = ["rg", "--line-number", "--with-filename", "--color=never"]

    if not case_sensitive:
        args.append("--ignore-case")

    if file_type:
        args.extend(["--type", file_type])

    args.append(pattern)

    args.append(path or ".")

    cmd = " ".join(args)
    with spin_context(f"Searching code with '{cmd}'"):
        return shell(cmd)


class ToolManager:
    def __init__(self) -> None:
        self._tool_map = {
            "read_text_file": read_text_file,
            "list_files": list_files,
            "list_directories": list_directories,
            "shell": shell,
            "edit_file": edit_file,
            "code_search": code_search,
        }
        self._function_declarations = FUNCTION_DECLARATIONS
        self._file_tracker = FileTracker()

    def call_tool(self, name: str, args: dict) -> dict:
        result = None
        error = None
        logger.info(f"Calling {name} with {args}")
        try:
            if name == "edit_file":
                path = args["path"]
                try:
                    self._file_tracker.track_file(path)
                except Exception as err:
                    logger.error(f"Error tracking file {path}: {str(err)}")
                    raise
            result = self._tool_map[name](**args)
        except KeyError:
            error = f"Function '{name}' is not supported"
        except Exception as err:
            error = str(err)
        logger.info(f"Result: {result}\nError: {error}")
        return {"tool": name, "result": result, "error": error}

        return self._tool_map[name](**args)

    def get_tool_definitions(self) -> dict:
        return self._function_declarations

    @property
    def tracked_files(self) -> list[str]:
        return self._file_tracker.tracked_files

    @property
    def files_have_edits(self) -> bool:
        return self._file_tracker.has_edits

    def confirm_file_edits(self, path: str) -> None:
        return self._file_tracker.confirm_file(path)

    def confirm_all_file_edits(self) -> None:
        return self._file_tracker.confirm_all()

    def revert_file_edits(self, path: str) -> str:
        return self._file_tracker.revert_file(path)

    def revert_all_file_edits(self) -> str:
        return self._file_tracker.revert_all()

    def print_file_diffs(self, path: str) -> None:
        return self._file_tracker.print_file_diffs(path)

    def print_all_file_diffs(self) -> None:
        return self._file_tracker.print_all_file_diffs()
