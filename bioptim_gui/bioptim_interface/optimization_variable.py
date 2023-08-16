from dataclasses import dataclass
from enum import Enum

import numpy as np

from ..misc.named_structure import NamedStructure


class Interpolation(Enum):
    CONSTANT = NamedStructure("InterpolationType.CONSTANT", "Constant")
    CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT = NamedStructure(
        "InterpolationType.CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT", "Start, intermediates and last"
    )


@dataclass
class Bounds:
    """
    min
        The minimum bounds for variable. It should be able to resolve to a np.ndarray 'n_elements X n_cols',
        where n_cols is dictated by the interpolation.
    max
        The maximum bounds for variable. It should be able to resolve to a np.ndarray 'n_elements X n_cols',
        where n_cols is dictated by the interpolation.
    interpolation
        The interpolation used to interpret the bounds structure.
    """

    min: tuple[tuple[float, ...], ...] | np.ndarray
    max: tuple[tuple[float, ...], ...] | np.ndarray
    interpolation: Interpolation


@dataclass
class InitialGuess:
    """
    initial_guess
        The initial guesses for the variable. It should be able to resolve to a np.ndarray 'n_elements X n_cols',
        where n_cols is dictated by the interpolation.
    interpolation
        The interpolation used to interpret the initial_guess structure.
    """

    initial_guess: tuple[tuple[float, ...], ...] | np.ndarray
    interpolation: Interpolation


@dataclass
class OptimizationVariable:
    name: str
    initial_guess: InitialGuess | None
    bounds: Bounds | None
    phase: int
