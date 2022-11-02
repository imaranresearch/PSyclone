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

'''Module containing tests for the CommonMetadata class.

'''
import pytest

from fparser.two import Fortran2003

from psyclone.domain.lfric.kernel.common_metadata import CommonMetadata
from psyclone.domain.lfric.kernel.meta_mesh_arg_metadata import \
    MetaMeshArgMetadata
from psyclone.domain.lfric.kernel.lfric_kernel_metadata import \
    LFRicKernelMetadata


def test_init():
    '''Test that a CommonMetadata instance can be created.'''

    common_metadata = CommonMetadata()
    assert isinstance(common_metadata, CommonMetadata)


def test_check_fparser2():
    '''Test that the check_fparser2 method in the CommonMetadata class
    works as expected.

    '''
    fortran_string = "program test\nend program"
    fparser2_tree = CommonMetadata.create_fparser2(
        fortran_string, Fortran2003.Program)
    _ = CommonMetadata.check_fparser2(fparser2_tree, Fortran2003.Program)

    with pytest.raises(TypeError) as info:
        _ = CommonMetadata.check_fparser2("invalid", Fortran2003.Program)
    assert ("Expected kernel metadata to be encoded as an fparser2 Program "
            "object but found type 'str' with value 'invalid'."
            in str(info.value))


def test_create_fparser2():
    '''Test that the create_fparser2 method in the CommonMetadata class
    works as expected.

    '''
    encoding = Fortran2003.Part_Ref
    fortran_string = "arg_type(GH_FIELD, GH_REAL, GH_READ)"
    result = CommonMetadata.create_fparser2(fortran_string, encoding)
    assert isinstance(result, encoding)

    with pytest.raises(ValueError) as info:
        _ = CommonMetadata.create_fparser2("#!$%", encoding)
    assert ("Expected kernel metadata to be a Fortran Part_Ref, but found "
            "'#!$%'." in str(info.value))

    with pytest.raises(ValueError) as info:
        _ = LFRicKernelMetadata.create_fparser2(
            "hello", Fortran2003.Derived_Type_Def)
    assert ("Expected kernel metadata to be a Fortran Derived_Type_Def, "
            "but found 'hello'." in str(info.value))


def test_create_from_fortran_string():
    '''Test the create_from_fortran_string() method. Test with an example
    subclass (MetaMeshArgMetadata).

    '''
    # Makes use of Fortran2003.Part_Ref.
    meta = MetaMeshArgMetadata.create_from_fortran_string(
        "mesh_data_type(adjacent_face)")
    assert isinstance(meta, MetaMeshArgMetadata)
    assert meta.mesh == "adjacent_face"
