# ROS Project Template

This repo offers up a skeleton for developing ROS2 projects inside a Docker containerised environment.

## Building the Dev Container

You man build the `dev` image manually by running:

```bash
docker compose build dev
```

Alternatively you can get [`VSCode`](https://code.visualstudio.com/) to build the image by starting vscode in this directory. It should automatically detect the `.devcontainer` directory and offer to open the project in the Devcontainer. If you agree, then the image will be build and the container started.

## Development

### Adding Source Code

To add new source code/packages, you simply att them to the `src` directory.

### Compiling

The project assumes that you're using `colcon` for building and testing the codebase. All the build, install and log files will be stored in the respective top-level `build/`, `install/` and `log/` directories, and these are included in the `.gitignore` file.

To compile code, run:

```bash
colcon build
```

To clean the workspace run:

```bash
colcon clean workspace --yes
```
