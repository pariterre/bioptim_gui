from dataclasses import dataclass

from ..bioptim_interface.optimal_control_type import OptimalControlType
from ..bioptim_interface.bio_model import BioModels
from ..bioptim_interface.dynamics import Dynamics
from ..bioptim_interface.objective_function import ObjectiveFunction
from ..bioptim_interface.optimization_variable import OptimizationVariable
from ..misc.__version__ import __version__


@dataclass
class OcpExporter:
    optimal_control_type: OptimalControlType
    bio_model_protocol: BioModels
    bio_model_path: str

    phase_time: float
    n_shooting: int
    use_sx: bool

    dynamics: Dynamics

    state_variables: tuple[OptimizationVariable, ...]
    control_variables: tuple[OptimizationVariable, ...]

    objective_functions: tuple[ObjectiveFunction, ...]

    def export(self, filename):
        with open(filename, "w+") as file:
            # Write the header
            file.write(
                "\"\"\"\n"
                f"This file was automatically generated using BioptimGUI version {__version__}\n"
                "\"\"\"\n"
                "\n"
                "from bioptim import *\n"  # TODO Pariterre - Do not import '*'
                "\n"
                "\n"
            )

            # Write the docstring of prepare_ocp section
            file.write(
                "def prepare_ocp():\n"
                "\t\"\"\"\n"
                "\tThis function build an optimal control program and instantiate it. "
                "It can be seen as a factory for the\n"
                "\tOptimalControlProgram class.\n"
                "\t\n"
                "\tParameters\n"
                "\t----------\n"
                "\t\n"
                "\tReturns\n"
                "\t-------\n"
                "\tThe OptimalControlProgram ready to be solved\n"
                "\t\"\"\"\n"
                "\t\n"
            )

            # Write the Generic section
            file.write(
                f"\t# Declaration of generic elements\n"
                f"\tbio_model = {repr(self.bio_model_protocol.value)}(\"{self.bio_model_path}\")\n"
                f"\tn_shooting = {self.n_shooting}\n"
                f"\tphase_time = {self.phase_time}\n"
                f"\t\n"
            )

            # Write the dynamics section
            file.write(
                f"\t# Declaration of the dynamics function used during integration\n"
                f"\tdynamics = Dynamics({repr(self.dynamics.fcn.value)}, expand={self.dynamics.is_expanded})\n"
                "\t\n"
            )

            # Write the variable section
            file.write(
                f"\t# Declaration of optimization variables bounds and initial guesses\n"
            )
            for var_type, all_variables in zip(("x", "u"), (self.state_variables, self.control_variables)):
                file.write(
                    f"\t{var_type}_bounds = BoundsList()\n"
                )
                for variable in all_variables:
                    if variable.bounds:
                        file.write(
                            f"\t{var_type}_bounds.add(\n"
                            f"\t\t\"{variable.name}\",\n"
                            f"\t\tmin_bound={variable.bounds.min},\n"
                            f"\t\tmax_bound={variable.bounds.max},\n"
                            f"\t\tinterpolation={repr(variable.bounds.interpolation.value)},\n"
                            f"\t\tphase={variable.phase},\n"
                            f"\t)")
                    file.write("\t\n")
                    file.write("\t\n")

                file.write(
                    f"\t{var_type}_initial_guesses = InitialGuessList()\n"
                )
                for variable in all_variables:
                    if variable.initial_guess:
                        file.write(
                            f"\t{var_type}_initial_guesses.add(\n"
                            f"\t\t\"{variable.name}\",\n"
                            f"\t\tinitial_guess={variable.initial_guess.initial_guess},\n"
                            f"\t\tinterpolation={repr(variable.initial_guess.interpolation.value)},\n"
                            f"\t\tphase={variable.phase},\n"
                            f"\t)")
                        file.write("\t\n")
                file.write("\t\n")

            # Write the objective functions
            file.write("\tobjective_functions = ObjectiveList()\n")
            for objective_function in self.objective_functions:
                file.write(
                    f"\tobjective_functions.add(\n"
                    f"\t\tobjective={repr(objective_function.fcn.value)},\n"
                    + "".join([f"\t\t{key}=\"{value}\",\n" for key, value in objective_function.args.items()]) +
                    f"\t)\n"
                )
            file.write("\t\n")

            # Write the return section
            file.write(
                f"\t# Construct and return the optimal control program (OCP)\n"
                f"\treturn {repr(self.optimal_control_type.value)}(\n"
                "\t\tbio_model=bio_model,\n"
                "\t\tn_shooting=n_shooting,\n"
                "\t\tphase_time=phase_time,\n"
                "\t\tdynamics=dynamics,\n"
                "\t\tx_bounds=x_bounds,\n"
                "\t\tu_bounds=u_bounds,\n"
                "\t\tx_init=x_initial_guesses,\n"
                "\t\tu_init=u_initial_guesses,\n"
                "\t\tobjective_functions=objective_functions,\n"
                f"\t\tuse_sx={self.use_sx},\n"
                "\t)\n"
                "\n"
                "\n"
            )

            # Write run as a script section
            file.write(
                "def main():\n"
                "\t\"\"\"\n"
                "\tIf this file is run, then it will perform the optimization\n"
                "\t\"\"\"\n"
                "\t\n"
                "\t# --- Prepare the ocp --- #\n"
                f"\tocp = prepare_ocp()\n"
                "\t\n"
                "\t# --- Solve the ocp --- #\n"
                "\tsol = ocp.solve(Solver.IPOPT())\n"
                "\tsol.print_cost()\n"
                "\t\n"
                "\n"
                "if __name__ == \"__main__\":\n"
                "\tmain()\n"
            )
