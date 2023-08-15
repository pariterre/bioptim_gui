import sys

# TODO port to PyQt6
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QComboBox,
    QPushButton,
    QFileDialog,
)

from .ocp_exporter import OcpExporter
from ..bioptim_interface.optimal_control_type import OptimalControlType


class BioptimGui(QMainWindow):
    _current_ocp_type: int = 0

    def __init__(self):
        self._app = QApplication(sys.argv)
        super(BioptimGui, self).__init__()
        self._build_main_window()

        self._build_select_ocp_type_combo_box()
        self._build_generate_ocp_button()

    def exec(self):
        self.show()
        self._app.exec_()

    def _build_main_window(self):
        self.setWindowTitle("Bioptim program generator")

        central_widget = QWidget()
        self._central_grid_layout = QGridLayout(central_widget)
        self.setCentralWidget(central_widget)

    def _build_select_ocp_type_combo_box(self):
        def on_ocp_selected(index):
            self._current_ocp_type = index

        available_ocp_types = tuple(str(e.value) for e in OptimalControlType)

        combo_box = QComboBox()
        combo_box.addItems(available_ocp_types)
        combo_box.setCurrentIndex(self._current_ocp_type)
        combo_box.currentIndexChanged.connect(on_ocp_selected)
        self._central_grid_layout.addWidget(combo_box, 0, 0)

    def _build_generate_ocp_button(self):
        def on_click():
            self._generate_ocp_file()

        button = QPushButton("Export OCP")
        button.clicked.connect(on_click)
        self._central_grid_layout.addWidget(button, 1, 0)

    def _generate_ocp_file(self):
        selection = QFileDialog.getSaveFileName(filter="Python Files (*.py)")
        filename = selection[0]
        exporter = OcpExporter()
        exporter.export(filename)
