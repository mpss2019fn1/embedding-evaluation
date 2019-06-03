import os
from datetime import datetime
from pathlib import Path

import git
import yaml


class NullFileTaskLogger:
    def __init__(self, *args, **kwargs):
        pass

    def write_metadata_file(self, *args, **kwargs):
        pass

    def new_file(self, *args, **kwargs):
        return Path(os.devnull)


class FileTaskLogger:
    def __init__(self, parent_directory, task):
        self.task = task
        self.directory = Path(parent_directory).joinpath(self.task.name)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.write_metadata_file()

    def write_metadata_file(self):
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha

        metadata = {**self.task.configuration, **{'git-sha': sha, 'timestamp': datetime.now()}}
        with self.directory.joinpath('metadata.yaml').open('w') as metadata_file:
            yaml.dump(metadata, metadata_file)

    def new_file(self, filename):
        new_file = self.directory.joinpath(filename)
        new_file.touch()
        return new_file
