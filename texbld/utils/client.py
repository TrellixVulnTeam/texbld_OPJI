from abc import ABC, abstractmethod
import os
import shutil
from texbld.common.directory import BUILD_CACHE_DIR
from typing import TYPE_CHECKING

from texbld.docker.dockergen import generate_dockerfile

if TYPE_CHECKING:
    from texbld.common.image.image import Image


class Client(ABC):
    @abstractmethod
    def unpack(self):
        pass

    def copy_to_builds(self, image: 'Image'):
        dockerfile = generate_dockerfile(image)
        buildpath = os.path.join(BUILD_CACHE_DIR, image.docker_image_name())
        if os.path.isdir(buildpath):
            shutil.rmtree(buildpath)
        os.makedirs(buildpath)
        for src in image.get_source().files:
            relpath = src.split('/')
            oldpath = os.path.join(image.package_dir(), *relpath)
            newpath = os.path.join(buildpath, *relpath)
            os.makedirs(os.path.dirname(newpath), exist_ok=True)
            if os.path.isdir(oldpath):
                shutil.copytree(oldpath, newpath)
            else:
                shutil.copy(oldpath, newpath)
        open(os.path.join(buildpath, "Dockerfile"), "w").write(dockerfile)
