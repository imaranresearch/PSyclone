# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2021, Science and Technology Facilities Council.
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
# Author J. Henrichs, Bureau of Meteorology
# -----------------------------------------------------------------------------

'''This module provides a class to manage indices in variable accesses.'''

from __future__ import print_function, absolute_import


from psyclone.errors import InternalError


class ComponentIndices(object):
    '''This class stores index information for variable accesses. It stores
    one index list for each component of a variable, e.g. for `a(i)%b(j)`
    it would store `[ [i], [j] ]`. Even for scalar accesses an empty list
    is stored, so `a` would have the component indices `[ [] ]`, and `a%b`
    would have `[ [], [] ]`.

    As a shortcut, the `indices` parameter can be None or an empty list
    (which then creates the component indices as `[[]]`), a list `l` (which
    will then create the component indices as `[l]`).

    :param indices: the indices from which to create this object.
    :type indices: None, [], a list or a list of lists of \
        :py:class:`psyclone.psyir.nodes.Node`s

    :raises InternalError: if the indices parameter is not None, a list \
        or a list of lists.
    :raises InternalError: if the indices parameter is a list, and some \
        but not all members are a list.

    '''
    def __init__(self, indices=None):
        if indices is None or indices == []:
            self._component_indices = [[]]
        elif isinstance(indices, list):
            if all(isinstance(indx, list) for indx in indices):
                # All elements of the indices are a list - so we
                # got a list of lists:
                self._component_indices = indices
            elif all(not isinstance(indx, list) for indx in indices):
                self._component_indices = [indices]
            else:
                raise InternalError("ComponentIndices: Invalid "
                                    "list parameter '{0}' - some elements"
                                    " but not all are lists".format(indices))
        else:
            raise InternalError("Index object in ComponentIndices "
                                "constructor must be None, a list or "
                                "list of lists, got '{0}'".format(indices))

    # ------------------------------------------------------------------------
    def __str__(self):
        '''Returns a string representating the indices.'''
        return str(self._component_indices)

    # ------------------------------------------------------------------------
    def iterate(self):
        '''Allows iterating over all component indices. It returns a tuple
        with two elements, the first one indicating the component, the second
        the dimension for which the index is. The return tuple can be used
        in a dictionary access (see `__getitem__`) of this object.

        :returns: a tuple of the component index and index.
        :rtype: tuple(int, int)

        '''
        for comp_ind, component in enumerate(self._component_indices):
            for indx in range(len(component)):
                yield (comp_ind, indx)

    # ------------------------------------------------------------------------
    def __getitem__(self, indx):
        '''Allows to use this class as a dictionary. If `indx` is an integer,
        the list of indices for the specified component is returned. If `indx`
        is a tuple (as returned from `iterate`), it will return the PSyIR for
        index for the specified component at the specified dimension.

        :returns: either the list of indices for a component, or the index \
            PSyIR node for the specified tuple.
        :rtype: list of :py:class:`psyclone.psyir.nodes.Node`, or \
            :py:class:`psyclone.psyir.nodes.Node`

        '''
        if isinstance(indx, tuple):
            return self._component_indices[indx[0]][indx[1]]
        return self._component_indices[indx]

    # ------------------------------------------------------------------------
    def __len__(self):
        ''':returns: the number of components in this class.
        :rtype: int '''
        return len(self._component_indices)

    # ------------------------------------------------------------------------
    def get(self):
        ''':returns: the component indices list of lists.
        :rtype: list of list of :py:class:`psyclone.psyir.nodes.Node`
        '''
        return self._component_indices

    # ------------------------------------------------------------------------
    def is_array(self):
        '''Test whether there is an index used in any component. E.g. an access
        like `a(i)%b` with indices `[ [i], [] ]` would still be considered an
        array.

        :returns: whether any of the variable components uses an index, i.e.\
            the variable is an array.
        :rtype: bool
        '''
        return any(grp for grp in self._component_indices)


# ---------- Documentation utils -------------------------------------------- #
# The list of module members that we wish AutoAPI to generate
# documentation for. (See https://psyclone-ref.readthedocs.io)
__all__ = ["ComponentIndices"]
