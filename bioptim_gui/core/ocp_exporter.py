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
                '"""\n'
                f"This file was automatically generated using BioptimGUI version {__version__}\n"
                '"""\n'
                "\n"
                "from bioptim import *\n"  # TODO Pariterre - Do not import '*'
                "\n"
                "\n"
            )

            # Write the docstring of prepare_ocp section
            file.write(
                "def prepare_ocp():\n"
                '    """\n'
                "    This function build an optimal control program and instantiate it. "
                "It can be seen as a factory for the\n"
                "    OptimalControlProgram class.\n"
                "\n"
                "    Parameters\n"
                "    ----------\n"
                "\n"
                "    Returns\n"
                "    -------\n"
                "    The OptimalControlProgram ready to be solved\n"
                '    """\n'
                "\n"
            )

            # Write the Generic section
            file.write(
                f"    # Declaration of generic elements\n"
                f'    bio_model = {repr(self.bio_model_protocol.value)}("{self.bio_model_path}")\n'
                f"    n_shooting = {self.n_shooting}\n"
                f"    phase_time = {self.phase_time}\n"
                f"\n"
            )

            # Write the dynamics section
            file.write(
                f"    # Declaration of the dynamics function used during integration\n"
                f"    dynamics = Dynamics({repr(self.dynamics.fcn.value)}, expand={self.dynamics.is_expanded})\n"
                "\n"
            )

            # Write the variable section
            file.write(f"    # Declaration of optimization variables bounds and initial guesses\n")
            for var_type, all_variables in zip(("x", "u"), (self.state_variables, self.control_variables)):
                file.write(f"    {var_type}_bounds = BoundsList()\n")
                for variable in all_variables:
                    if variable.bounds:
                        file.write(
                            f"    {var_type}_bounds.add(\n"
                            f'        "{variable.name}",\n'
                            f"        min_bound={variable.bounds.min},\n"
                            f"        max_bound={variable.bounds.max},\n"
                            f"        interpolation={repr(variable.bounds.interpolation.value)},\n"
                            f"        phase={variable.phase},\n"
                            f"    )"
                        )
                    file.write("\n")
                    file.write("\n")

                file.write(f"    {var_type}_initial_guesses = InitialGuessList()\n")
                for variable in all_variables:
                    if variable.initial_guess:
                        file.write(
                            f"    {var_type}_initial_guesses.add(\n"
                            f'        "{variable.name}",\n'
                            f"        initial_guess={variable.initial_guess.initial_guess},\n"
                            f"        interpolation={repr(variable.initial_guess.interpolation.value)},\n"
                            f"        phase={variable.phase},\n"
                            f"    )"
                        )
                        file.write("\n")
                file.write("\n")

            # Write the objective functions
            file.write("    objective_functions = ObjectiveList()\n")
            for objective_function in self.objective_functions:
                file.write(
                    f"    objective_functions.add(\n"
                    f"        objective={repr(objective_function.fcn.value)},\n"
                    + "".join([f'        {key}="{value}",\n' for key, value in objective_function.args.items()])
                    + f"    )\n"
                )
            file.write("\n")

            # Write the return section
            file.write(
                f"    # Construct and return the optimal control program (OCP)\n"
                f"    return {repr(self.optimal_control_type.value)}(\n"
                "        bio_model=bio_model,\n"
                "        n_shooting=n_shooting,\n"
                "        phase_time=phase_time,\n"
                "        dynamics=dynamics,\n"
                "        x_bounds=x_bounds,\n"
                "        u_bounds=u_bounds,\n"
                "        x_init=x_initial_guesses,\n"
                "        u_init=u_initial_guesses,\n"
                "        objective_functions=objective_functions,\n"
                f"        use_sx={self.use_sx},\n"
                "    )\n"
                "\n"
                "\n"
            )

            # Write run as a script section
            file.write(
                "def main():\n"
                '    """\n'
                "    If this file is run, then it will perform the optimization\n"
                '    """\n'
                "\n"
                "    # --- Prepare the ocp --- #\n"
                f"    ocp = prepare_ocp()\n"
                "\n"
                "    # --- Solve the ocp --- #\n"
                "    sol = ocp.solve(Solver.IPOPT())\n"
                "    sol.print_cost()\n"
                "\n"
                "\n"
                'if __name__ == "__main__":\n'
                "    main()\n"
            )
