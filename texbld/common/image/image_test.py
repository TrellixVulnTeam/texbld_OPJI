from texbld.common.image import *
import texbld.common.exceptions as exceptions


def test_image_hash_matches():
    x = SourceImage(
        name="hello", packages=["biber"],
        setup=["curl https://github.com"],
        files={},
        project_files={},
        project_commands={},
        install="apk add", update="apk update", inherit=DockerImage(name="hello"))
    y = SourceImage(
        name="hello", packages=["biber"],
        setup=["curl https://github.com"],
        files={},
        project_files={},
        project_commands={},
        install="apk add", update="apk update", inherit=DockerImage(name="hello"))
    assert x.image_hash() == y.image_hash()


def test_image_hash_nomatch():
    x = SourceImage(
        name="hello", packages=["biber"],
        setup=["curl https://github.com"],
        files={},
        project_files={},
        project_commands={},
        install="apk add", update="apk update", inherit=None)
    y = SourceImage(
        name="hello", packages=["biber"],
        setup=["curl https//github.com"],
        files={},
        project_files={},
        project_commands={},
        install="apk add", update="apk update", inherit=None)
    assert x.image_hash() != y.image_hash()


def test_nested_hash():
    s1 = SourceImage(
        name="hello", packages=["biber"],
        setup=[],
        files={},
        project_files={},
        project_commands={},
        install="apk add", update="apk update", inherit=DockerImage("alpine"))
    local1 = LocalImage(name="dependency", source=s1, testing=True)
    s2 = SourceImage(
        name="hello", packages=["biber", "py3-numpy"],
        setup=[],
        files={},
        project_files={},
        project_commands={},
        install="apk add", update="apk update", inherit=local1)
    local2 = LocalImage(name="image_name", source=s2, testing=True)
    s3 = SourceImage(
        name="hello", packages=["biber", "py3-numpy"],
        setup=[],
        files={},
        project_files={},
        project_commands={},
        install="apk add", update="apk update", inherit=local1)
    local3 = LocalImage(name="image_name", source=s3, testing=True)
    # should not fail
    assert local2.image_hash() == local3.image_hash()


def test_nested_hash_fail():
    s1 = SourceImage(
        name="hello", packages=["biber"],
        setup=[],
        files={},
        project_files={},
        project_commands={},
        install="apk add", update="apk update", inherit=DockerImage("alpine"))
    local1 = LocalImage(name="dependency", source=s1, testing=True)
    s2 = SourceImage(
        name="hello", packages=["biber", "py3-numpy"],
        setup=[],
        files={},
        project_files={},
        project_commands={},
        install="apk add", update="apk update", inherit=local1)
    local2 = LocalImage(name="image_name", source=s2, testing=True)
    s3 = SourceImage(
        name="hello", packages=["biber", "py3-pygments"],
        setup=[],
        files={},
        project_files={},
        project_commands={},
        install="apk add", update="apk update", inherit=local1)
    local3 = LocalImage(name="image_name", source=s3, testing=True)
    # should not fail
    assert local2.image_hash() != local3.image_hash()
