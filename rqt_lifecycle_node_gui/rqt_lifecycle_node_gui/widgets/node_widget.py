from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QPushButton
from .utils import get_state_label_text
from ..state import StateEnum, TransitionEnum


class NodeWidget(QWidget):

    on_button_press_signal = pyqtSignal(str, TransitionEnum)

    def __init__(
        self,
        name: str,
        state: StateEnum = StateEnum.UNCONFIGURED,
        parent: QWidget = None,
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

        self._configure.clicked.connect(self.on_configure_press)
        self._activate.clicked.connect(self.on_activate_press)
        self._shutdown.clicked.connect(self.on_shutdown_press)

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
            self._configure.setText("Configure")
            self._activate.setEnabled(False)
            self._activate.setText("Activate")
            self._shutdown.setEnabled(True)

        elif state == StateEnum.INACTIVE:
            self._configure.setEnabled(True)
            self._configure.setText("Unconfigure")
            self._activate.setEnabled(True)
            self._activate.setText("Activate")
            self._shutdown.setEnabled(True)

        elif state == StateEnum.ACTIVE:
            self._configure.setEnabled(False)
            self._configure.setText("Unconfigure")
            self._activate.setEnabled(True)
            self._activate.setText("Deactivate")
            self._shutdown.setEnabled(True)

        elif state == StateEnum.FINALIZED:
            self._configure.setEnabled(False)
            self._activate.setEnabled(False)
            self._shutdown.setEnabled(False)

        # else:
        #     raise KeyError(f"Unknown state: {state}")

    @pyqtSlot()
    def on_configure_press(self) -> None:
        if self._state not in [StateEnum.UNCONFIGURED, StateEnum.INACTIVE]:
            return

        if self._state == StateEnum.UNCONFIGURED:
            self.on_button_press_signal.emit(self.name, TransitionEnum.CONFIGURE)
        else:
            self.on_button_press_signal.emit(self.name, TransitionEnum.CLEANUP)

    @pyqtSlot()
    def on_activate_press(self) -> None:
        if self._state not in [StateEnum.INACTIVE, StateEnum.ACTIVE]:
            return

        if self._state == StateEnum.INACTIVE:
            self.on_button_press_signal.emit(self.name, TransitionEnum.ACTIVATE)
        else:
            self.on_button_press_signal.emit(self.name, TransitionEnum.DEACTIVATE)

    @pyqtSlot()
    def on_shutdown_press(self) -> None:
        if self._state not in [
            StateEnum.UNCONFIGURED,
            StateEnum.INACTIVE,
            StateEnum.ACTIVE,
        ]:
            return

        transition = TransitionEnum.SHUTDOWN_FROM_UNCONFIGURED

        if self._state == StateEnum.UNCONFIGURED:
            transition = TransitionEnum.SHUTDOWN_FROM_UNCONFIGURED
        elif self._state == StateEnum.INACTIVE:
            transition = TransitionEnum.SHUTDOWN_FROM_INACTIVE
        elif self._state == StateEnum.ACTIVE:
            transition = TransitionEnum.SHUTDOWN_FROM_ACTIVE

        self.on_button_press_signal.emit(self.name, transition)
