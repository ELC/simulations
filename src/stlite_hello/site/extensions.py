from pathlib import Path


class SiteBuildError(Exception):
    """Base error for static site construction."""


class OutputNotDirectoryError(SiteBuildError):
    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(f"Output path must be a directory: {path}")
