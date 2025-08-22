To run the GUI in rqt out-of-the-box, run:

```bash
ros2 run rqt_gui rqt_gui -s rqt_lifecycle_node_gui.plugin.Plugin
```

You can install/run demo lifecycles:

```bash
sudo apt update
sudo apt install -y ros-jazzy-lifecycle
ros2 run lifecycle lifecycle_talker --ros-args -r __node:=talker1
```

## Building

To compile and install the package, run:

```bash
colcon build
```

## Testing

To test and generate a code coverage report, run:

```bash
colcon test --pytest-with-coverage
```

This will add a `coverage.html` file to the `build/rqt_lifecycle_node_gui` directory. That directory contains an `index.html` which can be opened to view the coverage report.
