import json

import bioptim_gui_api.acrobatics_ocp.misc.acrobatics_config as config


def update_acrobatics_data(key: str, value) -> None:
    """
    Update the data of the acrobatics ocp

    Parameters
    ----------
    key: str
        The key to update
    value: Any
        The value to put in the key

    Returns
    -------
    None
    """
    with open(config.DefaultAcrobaticsConfig.datafile, "r") as f:
        data = json.load(f)
    data[key] = value
    with open(config.DefaultAcrobaticsConfig.datafile, "w") as f:
        json.dump(data, f)


def read_acrobatics_data(key: str = None):
    """
    Read the data of the acrobatics ocp

    Parameters
    ----------
    key: str
        The key to read

    Returns
    -------
    The data or the value of the key, the whole data if key is None
    """
    with open(config.DefaultAcrobaticsConfig.datafile, "r") as f:
        data = json.load(f)
    return data if key is None else data[key]


def update_phase_info(phase_names: list[str]) -> None:
    if len(phase_names) == 0:
        raise ValueError("n must be positive")

    data = read_acrobatics_data()

    n_phases = len(phase_names)
    final_time = data["final_time"]
    position = data["position"]
    with_visual_criteria = data["with_visual_criteria"]

    new_phases = [
        config.phase_name_to_phase(position, phase_names, i, with_visual_criteria) for i, _ in enumerate(phase_names)
    ]

    for i in range(n_phases):
        new_phases[i]["phase_name"] = phase_names[i]

    for i in range(0, n_phases):
        # rounding is necessary to avoid buffer overflow in the frontend
        new_phases[i]["duration"] = round(final_time / n_phases, 2)

    data["phases_info"] = new_phases
    with open(config.DefaultAcrobaticsConfig.datafile, "w") as f:
        json.dump(data, f)


def acrobatics_phase_names(nb_somersaults: int, position: str, half_twists: list[int]) -> list[str]:
    if position == "straight":
        return [f"Somersault {i + 1}" for i in range(nb_somersaults)] + ["Landing"]

    names = []

    # twist start
    if half_twists[0] > 0:
        names.append("Twist")

    last_have_twist = True
    next_have_twist = half_twists[1] > 0
    for i in range(1, nb_somersaults):
        is_last_somersault = i == nb_somersaults - 1
        # piking/tuck
        if last_have_twist:
            names.append("Pike" if position == "pike" else "Tuck")

        # somersaulting in pike
        if i == nb_somersaults - 1 or next_have_twist:
            names.append("Somersault")

        # kick out
        if next_have_twist or is_last_somersault:
            names.append("Kick out")

        # twisting
        if next_have_twist:
            names.append("Twist")

        last_have_twist = next_have_twist
        next_have_twist = is_last_somersault or half_twists[i + 1] > 0

    # nothing phase before landing if no twist
    if half_twists[-1] == 0:
        names.append("Waiting")

    # landing
    names.append("Landing")
    return names
