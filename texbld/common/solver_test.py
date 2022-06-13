import pytest
from texbld.common.image.image import DockerImage, LocalImage
from texbld.common.exceptions import DependencyCycle, FsNotFound
from texbld.common.solver import Solver


def test_success():
    # exists in the tests.
    s = Solver(LocalImage(name="test_dep1_2"))
    images = s.images()
    assert len(images) == 3
    assert images[0].__class__ == LocalImage
    assert images[1].__class__ == LocalImage
    assert images[2].__class__ == DockerImage


def test_depcycle():
    # test_dep2_1 -> test_dep2_2 -> test_dep2_3 -> test_dep2_1 (dependency cycle)
    with pytest.raises(DependencyCycle):
        s = Solver(LocalImage(name="test_dep2_1"))
    with pytest.raises(DependencyCycle):
        s = Solver(LocalImage(name="test_dep2_2"))
    with pytest.raises(DependencyCycle):
        s = Solver(LocalImage(name="test_dep2_3"))


def test_nodepcycle():
    # test_dep4_3 -> test_dep4_1 -> test_dep4_2 -> test_dep4_3 (at somethingelse.toml)
    s = Solver(LocalImage(name="test_dep4_3", config="image.toml"))


def test_notfound():
    with pytest.raises(FsNotFound):
        s = Solver(LocalImage(name="test_dep3"))
