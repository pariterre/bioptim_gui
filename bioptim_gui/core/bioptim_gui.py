import sys

# TODO port to PyQt6
from PyQt5.QtCore import QLocale
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QFileDialog,
    QLabel,
)

from .ocp_exporter import OcpExporter
from ..bioptim_interface.bio_model import BioModels
from ..bioptim_interface.optimal_control_type import OptimalControlType


QLocale.setDefault(QLocale(QLocale.English))


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

    _phase_time: float

    @property
    def phase_time(self):
        return self._phase_time

    _n_shooting: int

    @property
    def n_shooting(self):
        return self._n_shooting

    @property
    def bio_model_path(self):
        return self._bio_model_path_qlabel.text()

    def __init__(self):
        self._app = QApplication(sys.argv)
        super(BioptimGui, self).__init__()
        self._build_main_window()

        self._build_select_ocp_type_combo_box(0, 0)
        self._build_select_bio_model_protocol_combo_box(1, 0)
        self._build_bio_model_path_selection(2, 0)
        self._build_phase_time_declaration(3, 0)
        self._build_n_shooting_declaration(4, 0)
        self._build_generate_ocp_button(5, 0)

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

    def _build_bio_model_path_selection(self, row: int, col: int):
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

    def _build_phase_time_declaration(self, row: int, col: int):
        def on_text_changed(text):
            if text == "":
                self._phase_time = 0
            else:
                self._phase_time = float(text)

        layout = QHBoxLayout()
        phase_time_label = QLabel("Phase time")
        text_edit = QLineEdit()
        text_edit.setValidator(QDoubleValidator())
        text_edit.textChanged.connect(on_text_changed)

        layout.addWidget(phase_time_label)
        layout.addWidget(text_edit)

        self._central_grid_layout.addLayout(layout, row, col)

    def _build_n_shooting_declaration(self, row: int, col: int):
        def on_text_changed(text):
            if text == "":
                self._n_shooting = 0
            else:
                self._n_shooting = int(text)

        layout = QHBoxLayout()
        shooting_point_label = QLabel("Number of shooting points")
        text_edit = QLineEdit()
        text_edit.setValidator(QIntValidator())
        text_edit.textChanged.connect(on_text_changed)

        layout.addWidget(shooting_point_label)
        layout.addWidget(text_edit)

        self._central_grid_layout.addLayout(layout, row, col)

    def _build_generate_ocp_button(self, row: int, col: int):
        def on_click():
            self._generate_ocp_file()

        button = QPushButton("Export OCP")
        button.clicked.connect(on_click)
        self._central_grid_layout.addWidget(button, row, col)

    def _generate_ocp_file(self):
        selection = QFileDialog.getSaveFileName(filter="Python Files (*.py)")
        filename = selection[0]
        if filename is None or filename == "":
            return

        exporter = OcpExporter(
            optimal_control_type=self.optimal_control_type,
            bio_model_protocol=self.bio_model_protocol,
            bio_model_path=self.bio_model_path,
            phase_time=self.phase_time,
            n_shooting=self.n_shooting,
        )
        exporter.export(filename)
