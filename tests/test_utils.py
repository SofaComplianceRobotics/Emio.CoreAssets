import Sofa
import os
import pytest

from emio.utils import getListFromArgs, getColorFromFilename, RGBAColor
from emio.utils.topology import getExtremityFromBase, getRigidPositionsFromSVGPath, getIndicesInBox, applyTranslation, applyRotation


def test_getListFromArgs():
    assert getListFromArgs(None) is None
    assert getListFromArgs("") is None
    assert getListFromArgs("beam") == ["beam"]
    assert getListFromArgs(["beam", "tetra", "beam"]) == ["beam", "tetra", "beam"]


def test_getColorFromFilename():
    assert getColorFromFilename("blueleg") == RGBAColor.blue
    assert getColorFromFilename("yellowpart") == RGBAColor.yellow
    assert getColorFromFilename("red") == RGBAColor.red
    assert getColorFromFilename("green") == RGBAColor.green
    assert getColorFromFilename("grey") == RGBAColor.grey
    assert getColorFromFilename("nocolor") == RGBAColor.white


def test_getExtremityFromBase():
    node = Sofa.Core.Node()
    node.addObject("RequiredPlugin", pluginName=["Sofa.Component.Topology.Container.Constant"])
    topology1 = node.addObject("MeshTopology", position=[[0, 0, 0], [10, 0, 0], [0, 20, 0]])
    assert getExtremityFromBase(topology1, 0) == 2


def test_getRigidPositionsFromSVGPath():
    path = os.path.dirname(os.path.abspath(__file__))
    positions = getRigidPositionsFromSVGPath(path + "/test_blueleg.svg")
    assert positions is not None
    assert len(positions) == 15
    assert positions[0][0:3] == [0.0, -22.389854, 0.0]

    positions = getRigidPositionsFromSVGPath("noleg.svg")
    assert positions is None


def test_getIndicesInBox():
    box = [1, 1, 1, 2, 2, 2]
    positions = [[0., 0., 0.]]
    indicesIn, indicesOut = getIndicesInBox(positions, box)
    assert indicesIn == []
    assert indicesOut == [0]

    box = [0, 0, 0, 2, 2, 2]
    positions = [[0., 0., 0.], [1., 1., 1.], [3., 3., 3.]]
    indicesIn, indicesOut = getIndicesInBox(positions, box)
    assert indicesIn == [0, 1]
    assert indicesOut == [2]

    box = [2, 2, 2, 0, 0, 0]
    indicesIn, indicesOut = getIndicesInBox(positions, box)
    assert indicesIn == [0, 1]
    assert indicesOut == [2]


def test_applyTranslation():
    positions = [[0, 0, -10], [10., 0., -10.]]
    translation = [10., 0., 0.]
    applyTranslation(positions, translation)
    assert positions[0] == [10., 0., -10.]
    assert positions[1] == [20., 0., -10.]
    assert translation == [10., 0., 0.]


def test_applyRotation():
    from math import pi, cos, sin
    positions = [[0, 0, -10, 0., 0., 0., 1.], [0., 10., 0., 0., 0., 0., 1.]]
    rotation = [pi/2., 0, 0]
    applyRotation(positions, rotation)
    assert positions[0] == pytest.approx([0., 10., 0., cos(pi/4.), 0., 0., sin(pi/4.)])
    assert positions[1] == pytest.approx([0., 0., 10., cos(pi/4.), 0., 0., sin(pi/4.)])
    assert rotation == [pi/2., 0., 0.]

