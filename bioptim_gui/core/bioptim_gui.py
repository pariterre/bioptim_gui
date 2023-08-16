import sys

# TODO port to PyQt6
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QFileDialog,
    QLabel,
)

from .ocp_exporter import OcpExporter
from ..bioptim_interface.bio_model import BioModels
from ..bioptim_interface.optimal_control_type import OptimalControlType


class BioptimGui(QMainWindow):
    # Optimal control type
    _ocp_types_names = tuple(str(e.value) for e in OptimalControlType)
    _ocp_type_current_index: int = 0

    @property
    def optimal_control_type(self):
        return self._ocp_types_names[self._current_ocp_type_index]

    # BioModel
    _bio_models_names = tuple(f"{e.value}'s model" for e in BioModels)
    _bio_models_extensions = tuple(e.value.extension for e in BioModels)
    _bio_models_current_index: int = 0

    @property
    def bio_model_protocol(self):
        return self._bio_models_names[self._bio_models_current_index]

    _bio_model_path_qlabel: QLabel

    @property
    def bio_model_path(self):
        return self._bio_model_path_qlabel.text()

    def __init__(self):
        self._app = QApplication(sys.argv)
        super(BioptimGui, self).__init__()
        self._build_main_window()

        self._build_select_ocp_type_combo_box(0, 0)
        self._build_select_bio_model_protocol_combo_box(1, 0)
        self._build_bio_model_path_text_line(2, 0)
        self._build_generate_ocp_button(3, 0)

    def exec(self):
        self.show()
        self._app.exec_()

    def _build_main_window(self):
        self.setWindowTitle("Bioptim program generator")

        central_widget = QWidget()
        self._central_grid_layout = QGridLayout(central_widget)
        self.setCentralWidget(central_widget)

    def _build_select_ocp_type_combo_box(self, row: int, col: int):
        def on_ocp_selected(index):
            self._ocp_type_current_index = index

        combo_box = QComboBox()
        combo_box.addItems(self._ocp_types_names)
        combo_box.setCurrentIndex(self._ocp_type_current_index)
        combo_box.currentIndexChanged.connect(on_ocp_selected)
        self._central_grid_layout.addWidget(combo_box, row, col)

    def _build_select_bio_model_protocol_combo_box(self, row: int, col: int):
        def on_protocol_selected(index):
            self._bio_models_current_index = index
            self._bio_model_path_qlabel.setText("Select model path...")

        combo_box = QComboBox()
        combo_box.addItems(self._bio_models_names)
        combo_box.setCurrentIndex(self._bio_models_current_index)
        combo_box.currentIndexChanged.connect(on_protocol_selected)
        self._central_grid_layout.addWidget(combo_box, row, col)

    def _build_bio_model_path_text_line(self, row: int, col: int):
        def select_file():
            selection = QFileDialog.getOpenFileName(
                filter=f"{self.bio_model_protocol} (*.{self._bio_models_extensions[self._bio_models_current_index]})"
            )
            file_name = selection[0]
            if file_name is None or file_name == "":
                return
            self._bio_model_path_qlabel.setText(file_name)

        select_file_layout = QHBoxLayout()
        self._bio_model_path_qlabel = QLabel("Select model path...")
        button = QPushButton("...")
        button.clicked.connect(select_file)
        select_file_layout.addWidget(self._bio_model_path_qlabel)
        select_file_layout.addWidget(button)

        self._central_grid_layout.addLayout(select_file_layout, row, col)

    def _build_generate_ocp_button(self, row: int, col: int):
        def on_click():
            self._generate_ocp_file()

        button = QPushButton("Export OCP")
        button.clicked.connect(on_click)
        self._central_grid_layout.addWidget(button, row, col)

    def _generate_ocp_file(self):
        selection = QFileDialog.getSaveFileName(filter="Python Files (*.py)")
        filename = selection[0]

        exporter = OcpExporter(
            optimal_control_type=self.optimal_control_type,
            bio_model_protocol=self.bio_model_protocol,
            bio_model_path=self.bio_model_path,
        )
        exporter.export(filename)
