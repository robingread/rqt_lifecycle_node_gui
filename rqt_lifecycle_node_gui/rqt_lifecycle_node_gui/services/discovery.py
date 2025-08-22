import rclpy.node
import re


def check_node_is_lifecycle_node(
    node_name: str, services: list[tuple[str, list[str]]]
) -> bool:
    """Check whether a given node with a set of ROS services constitutes a ROS2 Lifecycle node.

    This is done by checking that a set of expected ROS2 service names with a given type are found to be exposed by the node.

    Args:
        node_name (str): The fully qualified name of the node (including the namespace).
        services (list): List of services that the node provides.

    Returns:
        bool: True if the node is a lifecycle node, else False.
    """
    assert node_name[0] == "/", "The node name must begin with a /"

    expected = [
        (
            f"{node_name}/change_state",
            ["lifecycle_msgs/srv/ChangeState"],
        ),
        (
            f"{node_name}/get_available_states",
            ["lifecycle_msgs/srv/GetAvailableStates"],
        ),
        (
            f"{node_name}/get_available_transitions",
            ["lifecycle_msgs/srv/GetAvailableTransitions"],
        ),
        (
            f"{node_name}/get_state",
            ["lifecycle_msgs/srv/GetState"],
        ),
        (
            f"{node_name}/get_transition_graph",
            ["lifecycle_msgs/srv/GetAvailableTransitions"],
        ),
    ]

    return all(s in services for s in expected)


def get_fully_qualified_node_name(namespace: str, name: str) -> str:
    full_name = f"/{namespace}/{name}"
    return re.sub(r"/+", "/", full_name)


def discover_lifecycle_node_names(node: rclpy.node.Node) -> list[str]:
    """Discover a list of Lifecycle nodes"""
    node_names = node.get_node_names_and_namespaces()
    print(node_names)

    lifecycle_nodes = []

    for name, ns in node_names:
        services = node.get_service_names_and_types_by_node(
            node_name=name,
            node_namespace=ns,
        )

        full_name = get_fully_qualified_node_name(ns, name)
        if not check_node_is_lifecycle_node(node_name=full_name, services=services):
            continue
        lifecycle_nodes.append(full_name)

    return lifecycle_nodes
