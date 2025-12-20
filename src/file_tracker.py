import difflib
import os
from typing import Generator

from .log import get_logger
from .terminal import (
    print_blue,
    print_green,
    print_red,
)

logger = get_logger(__name__)


class FileTracker:
    """
    Tracks file edits, allows to revert them.
    """

    def __init__(self):
        self._files = {}

    @property
    def tracked_files(self) -> list[str]:
        return list(self._files.keys())

    @property
    def has_edits(self) -> bool:
        return self._files != {}

    def track_file(self, path: str) -> bool:
        """
        Returns True if the file is new to the tracker else False.

        When a file is edited for the first time:
        * Make a backup copy of the file (file name is hidden and has a random
          suffix)
        * Keep track of the file copy in self._files (use absolute full path):
            {
                "<original-file-path>": {
                    "backup_file_path": "<backup-file-path>"
                },
                ...
            }
        * If file is created by edit, backup file path is None.
        """
        abs_path = os.path.abspath(path)

        # File already tracked, we're done.
        if abs_path in self._files:
            return False

        dir_path, file_path = os.path.split(abs_path)

        if os.path.exists(abs_path):
            backup_path = os.path.join(dir_path, f".{file_path}.bak")
            with open(abs_path) as infile:
                with open(backup_path, "w") as outfile:
                    outfile.write(infile.read())
        else:
            backup_path = None

        self._files[abs_path] = {"backup_file_path": backup_path}
        return True

    def file_diff(self, file_path) -> Generator[str, str, None]:
        from_file = self._files[file_path]["backup_file_path"]

        with open(file_path) as fi:
            after = fi.readlines()

        if from_file is not None:
            with open(from_file) as fi:
                before = fi.readlines()
        else:
            before = []

        return difflib.unified_diff(
            before,
            after,
            fromfile=file_path,
            tofile=file_path,
        )

    def print_file_diffs(self, path) -> None:
        print()
        for idx, line in enumerate(self.file_diff(path)):
            if line[-1] != "\n":
                line += "\n"
            if idx >= 2:
                if line[0] == "+":
                    print_green(line, end="")
                elif line[0] == "-":
                    print_red(line, end="")
                elif line.startswith("@@") and line.endswith("@@\n"):
                    print_blue(line, end="")
                else:
                    print(line, end="")
            else:
                print(line, end="")
        else:
            return

        # Only one blank line before next block of text.
        if not line.endswith("\n"):
            print()

    def untrack_file(self, path: str) -> None:
        abs_path = os.path.abspath(path)
        tracked = self._files.get(abs_path)
        if tracked is None:
            return

        if (backup := tracked["backup_file_path"]) is not None:
            if backup is not None:
                logger.info(f"Deleting backup file {backup}")
                os.remove(backup)

        del self._files[abs_path]

    def print_all_file_diffs(self) -> None:
        if not self.has_edits:
            print("\nThere are no file edits")
        for path in self._files:
            self.print_file_diffs(path)

    def confirm_file(self, path: str) -> None:
        self.untrack_file(path)
        print(f"\nConfirmed edits to {path}")

    def confirm_all(self) -> None:
        if not self.has_edits:
            print("\nThere are no file edits")
        # Cannot delete from a dictionary while iterating, so make a separate
        # list of paths to iterate.
        to_process = [path for path in self._files]
        for path in to_process:
            self.confirm_file(path)

    def revert_file(self, path: str) -> str:
        backup = self._files[path]["backup_file_path"]
        if backup is not None:
            logger.info(f"Reverting {path}")
            with open(backup) as infile:
                with open(path, "w") as outfile:
                    outfile.write(infile.read())
            logger.info(f"Deleting backup file {backup}")
            os.remove(backup)
        else:
            logger.info(f"Deleting {path}")
            os.remove(path)
        del self._files[path]
        msg = f"Reverted edits to {path}"
        print("\n" + msg)
        return msg

    def revert_all(self) -> str:
        if not self.has_edits:
            print("\nThere are no file edits")
        # Cannot delete from a dictionary while iterating, so make a separate
        # list of paths to iterate.
        to_process = [path for path in self._files]
        for path in to_process:
            self.revert_file(path)
        return f"Reverted edits to {', '.join(to_process)}"
