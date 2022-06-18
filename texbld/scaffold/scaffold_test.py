
import os
import shutil

import pytest
from texbld.directory import SCAFFOLD_TESTS
from texbld.common.image.image import LocalImage
from texbld.common.project.parse import parse_project
from texbld.config import PROJECT_CONFIG_FILE
from texbld.scaffold.scaffold import scaffold


def test_1():
    image = LocalImage(name="test_sc1_2")
    directory = os.path.join(SCAFFOLD_TESTS, "scaffold_1")
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    scaffold(image, directory)
    project = parse_project(
        open(os.path.join(directory, PROJECT_CONFIG_FILE)).read())
    assert os.path.isfile(os.path.join(directory, "main.md"))
    assert os.path.isfile(os.path.join(directory, "main.tex"))
    assert os.path.isfile(os.path.join(directory, "Makefile"))
    assert "test_sc1_2" in open(os.path.join(directory, "main.tex")).read()
    assert project.commands.get("compile") == "pandoc main.md -o main.pdf"
    assert project.commands.get("watch") == "latexmk -pdf -pvc main.tex"
    assert project.commands.get("clean") == "rm -rf main.tex"


def test_scaffold_exists():
    image = LocalImage(name="test_sc1_2")
    directory = os.path.join(SCAFFOLD_TESTS, "scaffold_exists")
    os.makedirs(directory, exist_ok=True)
    with pytest.raises(FileExistsError):
        scaffold(image, directory)


def test_scaffold_nofile():
    directory = os.path.join(SCAFFOLD_TESTS, "scaffold_nofile")
    image = LocalImage(name="test_sc2")
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    with pytest.raises(FileNotFoundError):
        scaffold(image, directory)
