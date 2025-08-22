from rqt_lifecycle_node_gui import StateEnum, TransitionEnum

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication
from rqt_lifecycle_node_gui.widgets import Widget
import os
import pytest
import sys

os.environ["QT_QPA_PLATFORM"] = "offscreen"


@pytest.fixture(scope="session", autouse=True)
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_init():
    widget = Widget()


def test_add_node_widget():
    widget = Widget()

    # Test that adding a node works
    assert widget.add_node(node_name="test_node", state=StateEnum.UNCONFIGURED) == True
    assert widget.has_node(node_name="test_node") == True

    # Test that adding the node again doesn't work
    assert widget.add_node(node_name="test_node", state=StateEnum.UNCONFIGURED) == False
    assert widget.has_node(node_name="test_node") == True


def test_has_node_widget():
    widget = Widget()
    assert widget.has_node(node_name="test") == False
