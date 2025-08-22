import rclpy.node
import rclpy.task
from rclpy.callback_groups import ReentrantCallbackGroup
import lifecycle_msgs.srv
from functools import partial
from ..state import StateEnum, TransitionEnum


class NodeInterface:
    def __init__(self, node: rclpy.node.Node, node_name: str) -> None:
        self._node = node
        self._node_name = node_name
        self._callback_group = ReentrantCallbackGroup()

        get_state_name = f"{node_name}/get_state"

        self._get_state_client = node.create_client(
            srv_name=get_state_name,
            srv_type=lifecycle_msgs.srv.GetState,
            callback_group=self._callback_group,
        )

        self._set_state_client = node.create_client(
            srv_name=f"{node_name}/change_state",
            srv_type=lifecycle_msgs.srv.ChangeState,
            callback_group=self._callback_group,
        )

    def get_state(self, callback) -> bool:
        request = lifecycle_msgs.srv.GetState.Request()
        future = self._get_state_client.call_async(request=request)
        future.add_done_callback(callback=partial(self._on_get_state, callback))
        return True

    def set_transition(self, transition: TransitionEnum) -> None:
        request = lifecycle_msgs.srv.ChangeState.Request()
        request.transition.id = transition.value
        future = self._set_state_client.call_async(request=request)
        future.add_done_callback(callback=self._on_set_state_callback)
        return True

    def _on_get_state(self, callback: None, future: rclpy.task.Future) -> None:
        if not callable(callback):
            return
        result: lifecycle_msgs.srv.GetState_Response = future.result()
        label: str = result.current_state.label
        state = StateEnum.from_str(label)
        callback(self._node_name, state)

    def _on_set_state_callback(self, future: rclpy.task.Future) -> None:
        pass
