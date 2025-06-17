from PyQt5.QtWidgets import QVBoxLayout, QWidget
from . import NodeWidget
from .utils import StateEnum


class Widget(QWidget):
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
        return True

    def has_node(self, node_name: str) -> bool:
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
