# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2023-2024, Science and Technology Facilities Council.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# -----------------------------------------------------------------------------
# Author: A. R. Porter, STFC Daresbury Lab
# -----------------------------------------------------------------------------

''' This module contains the GenericInterfaceSymbol.'''

from collections import namedtuple
from psyclone.psyir.symbols.routinesymbol import RoutineSymbol


class GenericInterfaceSymbol(RoutineSymbol):
    '''Symbol identifying a generic interface that maps to a number of
    different callable routines.

    :param str name: name of the interface.
    :param routines: the routines that this interface provides access to.
    :type routines: list[tuple[
                             :py:class:`psyclone.psyir.symbols.RoutineSymbol`,
                             bool]]
    :param kwargs: additional keyword arguments provided by
                   :py:class:`psyclone.psyir.symbols.TypedSymbol`
    :type kwargs: unwrapped dict.

    '''
    RoutineInfo = namedtuple("RoutineInfo", ["symbol", "from_container"])

    def __init__(self, name, routines, **kwargs):
        super().__init__(name, **kwargs)
        # Use the setter for 'routines' as it performs checking.
        self._routines = []
        self.routines = routines

    @property
    def routines(self):
        '''
        :returns: information on all of the routines to which this interface
                  provides access.
        :rtype: list[tuple[:py:class:`psyclone.psyir.symbols.RoutineSymbol`,
                           bool]]
        '''
        return self._routines

    @routines.setter
    def routines(self, values):
        '''
        Setter for the list of routines to which this interface provides
        access.

        :param values: the RoutineSymbols and whether or not each of them
            is a module procedure.
        :type values: list[
            tuple[:py:class:`psyclone.psyir.symbols.RoutineSymbol`, bool]]

        :raises ValueError: if no (or an empty) list of values is provided.
        :raises TypeError: if `symbols` is not a list that consists only of
                           (RoutineSymbol, bool) tuples.
        '''
        if not values:
            raise ValueError("A GenericInterfaceSymbol requires a list of "
                             "RoutineSymbols but none were provided.")
        if not isinstance(values, list):
            raise TypeError(f"A GenericInterfaceSymbol requires a list of "
                            f"tuples describing its member routines but got: "
                            f"'{values}'")
        self._routines = []
        for item in values:
            if not isinstance(item, tuple):
                raise TypeError(
                    f"A GenericInterfaceSymbol ('{self.name}') requires a "
                    f"list of tuples but got: '{type(item).__name__}'")
            if (len(item) != 2 or not isinstance(item[0], RoutineSymbol) or
                    not isinstance(item[1], bool)):
                raise TypeError(
                    f"Each tuple used to define a routine within the "
                    f"GenericInterfaceSymbol '{self.name}' must consist of a "
                    f"RoutineSymbol and a bool but got: "
                    f"{[type(rt).__name__ for rt in item]}")
            self._routines.append(self.RoutineInfo(item[0], item[1]))

    @property
    def container_routines(self):
        '''
        :returns: those routines that are defined in a Container.
        :rtype: list[:py:class:`psyclone.psyir.symbols.RoutineSymbol`]
        '''
        result = []
        for value in self._routines:
            if value.from_container:
                result.append(value.symbol)
        return result

    @property
    def external_routines(self):
        '''
        :returns: those routines that are external procedures.
        :rtype: list[:py:class:`psyclone.psyir.symbols.RoutineSymbol`]
        '''
        result = []
        for value in self._routines:
            if not value.from_container:
                result.append(value.symbol)
        return result

    def __str__(self):
        return (f"{self.name}: {type(self).__name__}<{self.datatype}, "
                f"routines={[rt.symbol.name for rt in self.routines]}>")

    def copy(self):
        '''Create and return a copy of this object. Any references to the
        original will not be affected so the copy will not be referred
        to by any other object.

        :returns: A symbol object with the same properties as this
                  symbol object.
        :rtype: :py:class:`psyclone.psyir.symbols.GenericInterfaceSymbol`

        '''
        # The constructors for all Symbol-based classes have 'name' as the
        # first positional argument.
        return type(self)(self.name, self.routines, datatype=self.datatype,
                          visibility=self.visibility,
                          interface=self.interface)


# For Sphinx AutoAPI documentation generation
__all__ = ["GenericInterfaceSymbol"]
