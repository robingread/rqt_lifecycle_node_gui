from .widgets import Widget, utils
from qt_gui.plugin import Plugin as RqtPlugin
from rqt_gui.ros2_plugin_context import Ros2PluginContext


class Plugin(RqtPlugin):

    def __init__(self, context: Ros2PluginContext) -> None:
        super().__init__(context)
        self.setObjectName("Plugin")
        self._widget = Widget()
        context.add_widget(self._widget)

        self._widget.add_node(
            node_name="test_node_1",
            state=utils.StateEnum.UNCONFIGURED,
        )
        self._widget.add_node(
            node_name="test_node_2",
            state=utils.StateEnum.INACTIVE,
        )
        self._widget.add_node(
            node_name="test_node_3",
            state=utils.StateEnum.ACTIVE,
        )
        self._widget.add_node(
            node_name=f"test_node_4",
            state=utils.StateEnum.FINALISED,
        )
        self._widget.add_node(
            node_name=f"test_node_5",
            state=utils.StateEnum.ERROR,
        )
