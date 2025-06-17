from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QPushButton
from .utils import StateEnum, get_state_label_text


class NodeWidget(QWidget):
    def __init__(
        self, name: str, state: StateEnum.UNCONFIGURED, parent: QWidget = None
    ) -> None:
        super().__init__(parent=parent)
        self._name_label = QLabel(text=name, parent=self)
        self._status_label = QLabel(
            text=get_state_label_text(state),
            parent=self,
        )

        self._state = state

        self._configure = QPushButton(parent=self, text="Configure")
        self._activate = QPushButton(parent=self, text="Activate")
        self._shutdown = QPushButton(parent=self, text="Shutdown")

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._name_label)
        self._layout.addStretch()
        self._layout.addWidget(self._status_label)
        self._layout.addWidget(self._configure)
        self._layout.addWidget(self._activate)
        self._layout.addWidget(self._shutdown)

        self.setLayout(self._layout)

        self.set_state(state=state)

    @property
    def name(self) -> str:
        return self._name_label.text()

    @property
    def state(self) -> StateEnum:
        return self._state

    def set_state(self, state: StateEnum) -> None:
        self._state = state

        self._status_label.setText(get_state_label_text(state=state))

        if state == StateEnum.UNCONFIGURED:
            self._configure.setEnabled(True)
            self._activate.setEnabled(False)
            self._shutdown.setEnabled(True)

        elif state == StateEnum.INACTIVE:
            self._configure.setEnabled(True)
            self._configure.setText("Unconfigure")
            self._activate.setEnabled(True)
            self._shutdown.setEnabled(True)

        elif state == StateEnum.ACTIVE:
            self._configure.setEnabled(False)
            self._configure.setText("Unconfigure")
            self._activate.setEnabled(True)
            self._activate.setText("Deactivate")
            self._shutdown.setEnabled(True)

        elif state == StateEnum.FINALISED:
            self._configure.setEnabled(False)
            self._activate.setEnabled(False)
            self._shutdown.setEnabled(False)
