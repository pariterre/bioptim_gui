"""
This file was automatically generated using BioptimGUI version 0.0.1
"""

from bioptim import *


def prepare_ocp():
	"""
	This function build an optimal control program and instantiate it. It can be seen as a factory for the
	OptimalControlProgram class.
	
	Parameters
	----------
	
	Returns
	-------
	The OptimalControlProgram ready to be solved
	"""
	
	# Declaration of generic elements
	bio_model = BiorbdModel("models/pendulum.bioMod")
	n_shooting = 10
	phase_time = 1.0
	
	# Declaration of the dynamics function used during integration
	dynamics = Dynamics(DynamicsFcn.TORQUE_DRIVEN, expand=True)
	
	# Declaration of optimization variables bounds and initial guesses
	x_bounds = BoundsList()
	x_bounds.add(
		"q",
		min_bound=((0, -1, 0), (0, -6.283185307179586, 3.141592653589793)),
		max_bound=((0, 1, 0), (0, 6.283185307179586, 3.141592653589793)),
		interpolation=InterpolationType.CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT,
		phase=0,
	)	
	
	x_bounds.add(
		"qdot",
		min_bound=((0, -10, 0), (0, -31.41592653589793, 0)),
		max_bound=((0, 10, 0), (0, 31.41592653589793, 0)),
		interpolation=InterpolationType.CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT,
		phase=0,
	)	
	
	x_initial_guesses = InitialGuessList()
	x_initial_guesses.add(
		"q",
		initial_guess=((0,), (0,)),
		interpolation=InterpolationType.CONSTANT,
		phase=0,
	)	
	
	u_bounds = BoundsList()
	u_bounds.add(
		"tau",
		min_bound=((-35,), (0,)),
		max_bound=((35,), (0,)),
		interpolation=InterpolationType.CONSTANT,
		phase=0,
	)	
	
	u_initial_guesses = InitialGuessList()
	u_initial_guesses.add(
		"tau",
		initial_guess=((0,), (0,)),
		interpolation=InterpolationType.CONSTANT,
		phase=0,
	)	
	
	objective_functions = ObjectiveList()
	objective_functions.add(
		objective=ObjectiveFcn.Lagrange.MINIMIZE_CONTROL,
		key="tau",
	)
	
	# Construct and return the optimal control program (OCP)
	return OptimalControlProgram(
		bio_model=bio_model,
		n_shooting=n_shooting,
		phase_time=phase_time,
		dynamics=dynamics,
		x_bounds=x_bounds,
		u_bounds=u_bounds,
		x_init=x_initial_guesses,
		u_init=u_initial_guesses,
		objective_functions=objective_functions,
		use_sx=True,
	)


def main():
	"""
	If this file is run, then it will perform the optimization
	"""
	
	# --- Prepare the ocp --- #
	ocp = prepare_ocp()
	
	# --- Solve the ocp --- #
	sol = ocp.solve(Solver.IPOPT())
	sol.print_cost()
	

if __name__ == "__main__":
	main()
