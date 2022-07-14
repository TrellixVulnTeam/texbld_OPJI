from dataclasses import dataclass, field
from texbld.exceptions import CommandNotFound
from texbld.common.image import Image
from texbld.common.solver import Solver
from texbld.config import LATEST_CONFIG_VERSION
from texbld.docker.build import build as build_dockerimage
import texbld.logger as logger


@dataclass
class Project:
    name: str
    image: Image
    commands: 'dict[str, str]'
    # should be absolute path
    directory: str = ""

    def build(self, cache=False):
        build_dockerimage(Solver(self.image), cache=cache)

    def run(self, command_name: str):
        from texbld.docker.client import dockerclient
        if command_name not in self.commands:
            raise CommandNotFound(command_name)
        logger.progress(f"Running {self.image.docker_image_name()}...")
        stream = dockerclient.containers.run(
            self.image.docker_image_name(),
            volumes={self.directory: {'bind': '/texbld', 'mode': 'rw'}},
            entrypoint=["sh", "-c", self.commands.get(command_name)], stream=True)
        for data in stream:
            print(data.decode())
        dockerclient.containers.prune()

    def project_dict(self):
        _, dct = self.image.project_dict()
        return dict(
            name=self.name,
            version=LATEST_CONFIG_VERSION,
            image=dct,
            commands=self.commands
        )
