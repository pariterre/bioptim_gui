import filecmp
import os

import numpy as np

from bioptim_gui import (
    __version__,
    BioModels,
    Dynamics,
    DynamicsFcn,
    ObjectiveFunction,
    ObjectiveFunctionFcn,
    OptimalControlType,
    OptimizationVariable,
    InitialGuess,
    Bounds,
    Interpolation,
    OcpExporter,
)


def test_version():
    assert __version__ == "0.0.1"
    return


def test_create_trivial():
    # TODO create with bounds and initial_guess being None
    return


def test_create_pendulum():
    exporter = OcpExporter(
        optimal_control_type=OptimalControlType.OptimalControlProgram,
        bio_model_protocol=BioModels.BIORBD,
        bio_model_path="models/pendulum.bioMod",
        use_sx=True,
        phase_time=1.0,
        n_shooting=10,
        dynamics=Dynamics(fcn=DynamicsFcn.TORQUE_DRIVEN, is_expanded=True),
        state_variables=(
            OptimizationVariable(
                name="q",
                initial_guess=InitialGuess(
                    initial_guess=((0,), (0,)),
                    interpolation=Interpolation.CONSTANT,
                ),
                bounds=Bounds(
                    min=((0, -1, 0), (0, -2 * np.pi, np.pi)),
                    max=((0, 1, 0), (0, 2 * np.pi, np.pi)),
                    interpolation=Interpolation.CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT,
                ),
                phase=0
            ),
            OptimizationVariable(
                name="qdot",
                initial_guess=None,
                bounds=Bounds(
                    min=((0, -10, 0), (0, -10 * np.pi, 0)),
                    max=((0, 10, 0), (0, 10 * np.pi, 0)),
                    interpolation=Interpolation.CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT,
                ),
                phase=0,
            ),
        ),
        control_variables=(
            OptimizationVariable(
                name="tau",
                initial_guess=InitialGuess(
                    initial_guess=((0,), (0,)),
                    interpolation=Interpolation.CONSTANT,
                ),
                bounds=Bounds(
                    min=((-35,), (0,)),
                    max=((35,), (0,)),
                    interpolation=Interpolation.CONSTANT
                ),
                phase=0
            ),
        ),
        objective_functions=(
            ObjectiveFunction(fcn=ObjectiveFunctionFcn.Lagrange.MINIMIZE_CONTROL, args={"key": "tau"}),
        ),
    )

    # Generate the file and compare it the to model
    file_path = "temporary.py"
    exporter.export(file_path)
    filecmp.cmp(file_path, "expected/expected_create_pendulum.py")

    # Clean up and exit
    os.remove(file_path)
    return
