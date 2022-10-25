# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2022, Science and Technology Facilities Council
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
# Author R. W. Ford, STFC Daresbury Lab

'''Module containing the OperatorArgMetadata class which captures the metadata
associated with an operator argument. Supports the creation, modification
and Fortran output of a Operator argument.

'''
from fparser.two import Fortran2003

from psyclone.domain.lfric import LFRicConstants
from psyclone.domain.lfric.kernel.scalar_arg_metadata import ScalarArgMetadata


class OperatorArgMetadata(ScalarArgMetadata):
    '''Class to capture LFRic kernel metadata information for an operator
    argument.

    :param Optional[str] datatype: the datatype of this operator \
        (GH_INTEGER, ...).
    :param Optional[str] access: the way the kernel accesses this \
        operator (GH_WRITE, ...).
    :param Optional[str] function_space_to: the function space that \
        this operator maps to (W0, ...).
    :param Optional[str] function_space_from: the function space that \
        this operator maps from (W0, ...).

    '''
    # The name used to specify an operator argument in LFRic metadata.
    form = "GH_OPERATOR"
    # The relative positions of LFRic function-space-to and
    # function-space-from metadata. Metadata for an operator argument
    # is provided in the following format 'arg_type(form, datatype,
    # access, function_space_to, function_space_from)'. Therefore, for
    # example, the index of the function_space_to argument
    # (function_space_to_arg_index) is 3. Index values not provided
    # here are common to the parent classes and are inherited from
    # them.
    function_space_to_arg_index = 3
    function_space_from_arg_index = 4

    def __init__(self, datatype=None, access=None, function_space_to=None,
                 function_space_from=None):
        super().__init__(datatype, access)
        self._function_space_to = None
        self._function_space_from = None
        if function_space_to is not None:
            self.function_space_to = function_space_to
        if function_space_from is not None:
            self.function_space_from = function_space_from

    @staticmethod
    def create_from_fparser2(fparser2_tree):
        '''Create an instance of this class from an fparser2 tree.

        :param fparser2_tree: fparser2 tree capturing the metadata for \
            an operator argument.
        :type fparser2_tree: :py:class:`fparser.two.Fortran2003.Part_Ref`

        :returns: an instance of OperatorArgMetadata.
        :rtype: :py:class:`psyclone.domain.lfric.kernel.OperatorArgMetadata`

        '''
        OperatorArgMetadata.check_fparser2(fparser2_tree, "arg_type")
        OperatorArgMetadata.check_nargs(fparser2_tree, 5)
        OperatorArgMetadata.check_first_arg(fparser2_tree, "Operator")
        datatype, access = OperatorArgMetadata.get_type_and_access(
            fparser2_tree)
        function_space_to = OperatorArgMetadata.get_arg(
            fparser2_tree, OperatorArgMetadata.function_space_to_arg_index)
        function_space_from = OperatorArgMetadata.get_arg(
            fparser2_tree, OperatorArgMetadata.function_space_from_arg_index)
        OperatorArgMetadata.check_remaining_args(
            fparser2_tree, datatype, access, function_space_to,
            function_space_from)
        return OperatorArgMetadata(
            datatype, access, function_space_to, function_space_from)

    def fortran_string(self):
        ''':returns: the metadata represented by this class as Fortran.
        :rtype: str

        :raises ValueError: if one or more of the datatype, access, \
            function_space_to or function_space_from values have not \
            been set.

        '''
        if not (self.datatype and self.access and self.function_space_to and
                self.function_space_from):
            raise ValueError(
                f"Values for datatype, access, function_space_to and "
                f"function_space_from must be provided before calling the "
                f"fortran_string method, but found '{self.datatype}', "
                f"'{self.access}', '{self.function_space_to}' and "
                f"'{self.function_space_from}', respectively.")

        return (f"arg_type({self.form}, {self.datatype}, {self.access}, "
                f"{self.function_space_to}, {self.function_space_from})")

    @staticmethod
    def check_access(value):
        '''
        :param str value: the access descriptor to validate.
        '''
        const = LFRicConstants()
        OperatorArgMetadata.check_value(
            value, "access descriptor", const.VALID_OPERATOR_ACCESS_TYPES)

    @staticmethod
    def check_datatype(value):
        '''
        :param str value: the datatype to check for validity.
        '''
        const = LFRicConstants()
        OperatorArgMetadata.check_value(
            value, "datatype descriptor", const.VALID_OPERATOR_DATA_TYPES)

    @property
    def function_space_to(self):
        '''
        :returns: the first function space for this operator \
            argument (that this operator maps to).
        :rtype: str
        '''
        return self._function_space_to

    @function_space_to.setter
    def function_space_to(self, value):
        '''
        :param str value: set the function space to the \
            specified value.

        raises ValueError: if the provided value is not a valid \
            function space.

        '''
        const = LFRicConstants()
        self.check_value(
            value, "function_space_to", const.VALID_FUNCTION_SPACES)
        self._function_space_to = value

    @property
    def function_space_from(self):
        '''
        :returns: the second function space for this operator \
            argument (that this operator maps from).
        :rtype: str
        '''
        return self._function_space_from

    @function_space_from.setter
    def function_space_from(self, value):
        '''
        :param str value: set the function space to the \
            specified value.
        '''
        const = LFRicConstants()
        self.check_value(
            value, "function_space_from", const.VALID_FUNCTION_SPACES)
        self._function_space_from = value
