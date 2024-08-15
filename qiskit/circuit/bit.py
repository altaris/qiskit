# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Quantum bit and Classical bit objects.
"""
import copy

from qiskit.circuit.exceptions import CircuitError


class Bit:
    """Implement a generic bit.

    .. note::
        This class should not be instantiated directly. This is just a superclass
        for :class:`~.Clbit` and :class:`~.circuit.Qubit`.
    """

    __slots__ = {"_register", "_index", "_hash", "_repr"}

    def __init__(self, register=None, index=None) -> None:
        """Create a new generic bit."""
        if (register, index) == (None, None):
            self._register = None
            self._index = None
            # To sidestep the overridden Bit.__hash__ and use the default hash
            # algorithm (only new-style Bits), call default object hash method.
            self._hash = object.__hash__(self)
        else:
            try:
                index = int(index)
            except Exception as ex:
                raise CircuitError(
                    f"index needs to be castable to an int: type {type(index)} was provided"
                ) from ex

            if index < 0:
                index += register.size

            if index >= register.size:
                raise CircuitError(
                    f"index must be under the size of the register: {index} was provided"
                )

            self._register = register
            self._index = index
            self._hash = hash((self._register, self._index))
            self._repr = f"{self.__class__.__name__}({self._register}, {self._index})"

    def __repr__(self) -> str:
        """Return the official string representing the bit."""
        if (self._register, self._index) == (None, None):
            # Similar to __hash__, use default repr method for new-style Bits.
            return object.__repr__(self)
        return self._repr

    def __hash__(self):
        return self._hash

    def __eq__(self, other) -> bool:
        if (self._register, self._index) == (None, None):
            return other is self

        try:
            return self._repr == other._repr
        except AttributeError:
            return False

    def __copy__(self) -> "Bit":
        # Bits are immutable.
        return self

    def __deepcopy__(self, memo=None) -> "Bit":
        if (self._register, self._index) == (None, None):
            return self

        # Old-style bits need special handling for now, since some code seems
        # to rely on their registers getting deep-copied.
        bit = type(self).__new__(type(self))
        bit._register = copy.deepcopy(self._register, memo)
        bit._index = self._index
        bit._hash = self._hash
        bit._repr = self._repr
        return bit
