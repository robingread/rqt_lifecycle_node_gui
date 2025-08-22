from rqt_lifecycle_node_gui import StateEnum, TransitionEnum

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication
from rqt_lifecycle_node_gui.widgets import NodeWidget
import os
import pytest
import sys

os.environ["QT_QPA_PLATFORM"] = "offscreen"


class SignalHandler(QObject):
    """Helper class used to provide a Qt Slot so that the NodeWidget signals can be connected
    and their payloads recorded."""

    def __init__(self, widget: NodeWidget, parent: QObject = None) -> None:
        super().__init__(parent=parent)

        widget.on_button_press_signal.connect(self.handler)

        self.name = None
        self.transition = None

    @pyqtSlot(str, TransitionEnum)
    def handler(self, name: str, transition: TransitionEnum) -> None:
        """Qt Slot for handling a signal from the NodeWidget class.

        Args:
            name (str): The name of the node.
            transition (TransitionEnum): The desired state transition.
        """
        self.name = name
        self.transition = transition


@pytest.fixture(scope="session", autouse=True)
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_get_name():
    widget = NodeWidget(name="test")
    assert widget.name == "test"
    widget.deleteLater()


def test_get_state():
    widget = NodeWidget(name="test", state=StateEnum.ACTIVE)
    assert widget.state == StateEnum.ACTIVE
    widget.deleteLater()


@pytest.mark.parametrize(
    "state",
    [
        (StateEnum.UNCONFIGURED),
        (StateEnum.INACTIVE),
        (StateEnum.ACTIVE),
        (StateEnum.FINALIZED),
        (StateEnum.ERROR),
    ],
)
def test_set_state(state):
    widget = NodeWidget(name="test", state=StateEnum.ACTIVE)
    assert widget.state == StateEnum.ACTIVE

    widget.set_state(state=state)
    assert widget.state == state

    widget.deleteLater()


@pytest.mark.parametrize(
    "initial_state, name, transition",
    [
        (StateEnum.UNCONFIGURED, "test", TransitionEnum.CONFIGURE),
        (StateEnum.INACTIVE, "test", TransitionEnum.CLEANUP),
        (StateEnum.ACTIVE, None, None),
        (StateEnum.FINALIZED, None, None),
    ],
)
def test_on_configure_press(initial_state, name, transition):
    widget = NodeWidget(name="test", state=initial_state)
    handler = SignalHandler(widget=widget)

    widget.on_configure_press()

    assert handler.name == name
    assert handler.transition == transition

    widget.deleteLater()


@pytest.mark.parametrize(
    "initial_state, name, transition",
    [
        (StateEnum.UNCONFIGURED, None, None),
        (StateEnum.INACTIVE, "test", TransitionEnum.ACTIVATE),
        (StateEnum.ACTIVE, "test", TransitionEnum.DEACTIVATE),
        (StateEnum.FINALIZED, None, None),
    ],
)
def test_on_activate_press(initial_state, name, transition):
    widget = NodeWidget(name="test", state=initial_state)
    handler = SignalHandler(widget=widget)

    widget.on_activate_press()

    assert handler.name == name
    assert handler.transition == transition

    widget.deleteLater()


@pytest.mark.parametrize(
    "initial_state, name, transition",
    [
        (StateEnum.UNCONFIGURED, "test", TransitionEnum.SHUTDOWN_FROM_UNCONFIGURED),
        (StateEnum.INACTIVE, "test", TransitionEnum.SHUTDOWN_FROM_INACTIVE),
        (StateEnum.ACTIVE, "test", TransitionEnum.SHUTDOWN_FROM_ACTIVE),
        (StateEnum.FINALIZED, None, None),
    ],
)
def test_on_shutdown_press(initial_state, name, transition):
    widget = NodeWidget(name="test", state=initial_state)
    handler = SignalHandler(widget=widget)

    widget.on_shutdown_press()

    assert handler.name == name
    assert handler.transition == transition

    widget.deleteLater()
