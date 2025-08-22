from .services import discovery, interface
from .widgets import Widget
from .state import StateEnum, TransitionEnum
from qt_gui.plugin import Plugin as RqtPlugin
from rqt_gui.ros2_plugin_context import Ros2PluginContext
from functools import partial
import rclpy.node
from PyQt5.QtCore import pyqtSlot


class Plugin(RqtPlugin):

    def __init__(self, context: Ros2PluginContext) -> None:
        super().__init__(context)
        self.setObjectName("Plugin")
        self._node: rclpy.node.Node = context.node

        self._widget = Widget()
        self._widget.on_button_press_signal.connect(self.on_gui_update)
        context.add_widget(self._widget)

        self._clients: dict[str, interface.NodeInterface] = {}

        # Discover all the nodes, and add a Widget and Client
        lifecycle_nodes = discovery.discover_lifecycle_node_names(node=self._node)

        for node in lifecycle_nodes:
            # Add the widget
            self._widget.add_node(node_name=node, state=StateEnum.UNCONFIGURED)

            # Setup the clients
            self._clients[node] = interface.NodeInterface(
                node=self._node, node_name=node
            )

        self._timer = self._node.create_timer(1.0, self.update)

    def update(self) -> None:
        for client in self._clients.values():
            client.get_state(callback=self.get_state_callback)

    def get_state_callback(self, node_name: str, state: StateEnum) -> None:
        self._widget.set_node_state(node_name=node_name, state=state)

    @pyqtSlot(str, StateEnum)
    def on_gui_update(self, node_name: str, transition: TransitionEnum) -> None:
        self._clients[node_name].set_transition(transition=transition)
