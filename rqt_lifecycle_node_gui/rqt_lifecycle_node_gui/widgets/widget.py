from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from . import NodeWidget
from ..state import StateEnum, TransitionEnum


class Widget(QWidget):
    on_button_press_signal = pyqtSignal(str, TransitionEnum)

    def __init__(self) -> None:
        super().__init__()

        # Used to store the widgets for each node entry
        self._node_map: dict[str, NodeWidget] = {}

        # Layout used to keep the Widgets layout
        self._widget_layout = QVBoxLayout()

        # Main layout used to push all the node widgets up to the top
        self._layout = QVBoxLayout()
        self._layout.addLayout(self._widget_layout)
        self._layout.addStretch()
        self.setLayout(self._layout)

    def add_node(self, node_name: str, state: StateEnum) -> bool:
        if self.has_node(node_name=node_name):
            return False
        self._node_map[node_name] = NodeWidget(name=node_name, state=state, parent=self)
        self._widget_layout.addWidget(self._node_map[node_name])
        self._node_map[node_name].on_button_press_signal.connect(
            self._on_node_ui_update
        )
        return True

    def has_node(self, node_name: str) -> bool:
        """Check whether there is a Widget for a node with a given name.

        Args:
            node_name (str): Name of the node to check.

        Returns:
            bool: True if there is a widget registered to the node name, else False.
        """
        return node_name in self._node_map.keys()

    def remove_node(self, node_name: str) -> bool:
        """Remove a node entry from the Widget.

        Args:
            node_name (str): The name of the node to remove.

        Returns:
            bool: True if the node was removed, else False.
        """
        if not self.has_node(node_name=node_name):
            return False

        self._layout.removeWidget(self._node_map[node_name])
        del self._node_map[node_name]
        return True

    def set_node_state(self, node_name: str, state: int) -> None:
        if not self.has_node(node_name=node_name):
            return

        self._node_map[node_name].set_state(state)

    @pyqtSlot(str, TransitionEnum)
    def _on_node_ui_update(self, node_name: str, transition: TransitionEnum) -> None:
        self.on_button_press_signal.emit(node_name, transition)
