!-------------------------------------------------------------------------------
! Copyright (c) 2018-2025, Science and Technology Facilities Council
!
! Redistribution and use in source and binary forms, with or without
! modification, are permitted provided that the following conditions are met:
!
! * Redistributions of source code must retain the above copyright notice, this
!   list of conditions and the following disclaimer.
!
! * Redistributions in binary form must reproduce the above copyright notice,
!   this list of conditions and the following disclaimer in the documentation
!   and/or other materials provided with the distribution.
!
! * Neither the name of the copyright holder nor the names of its
!   contributors may be used to endorse or promote products derived from
!   this software without specific prior written permission.
!
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
! AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
! IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
! DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
! FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
! DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
! SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
! CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
! OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
! OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
!-------------------------------------------------------------------------------
! Author: A. R. Porter STFC Daresbury Lab
! Modified: I. Kavcic Met Office

module testkern_eval_2fs_mod

  use constants_mod
  use argument_mod
  use fs_continuity_mod
  use kernel_mod

  type, extends(kernel_type) :: testkern_eval_2fs_type
     type(arg_type)  :: meta_args(2) =  (/       &
       arg_type(GH_FIELD, GH_REAL, GH_INC,  W0), &
       arg_type(GH_FIELD, GH_REAL, GH_READ, W1)  &
       /)
     type(func_type) :: meta_funcs(1) = (/       &
       func_type(W1, GH_DIFF_BASIS)              &
       /)
     integer :: operates_on = CELL_COLUMN
     integer :: gh_shape = gh_evaluator
     integer :: gh_evaluator_targets(2) = (/W0, W1/)
   contains
     procedure, nopass :: code => testkern_eval_2fs_code
  end type testkern_eval_2fs_type

contains

  subroutine testkern_eval_2fs_code(nlayers, f0, f1,         &
                                    ndf_w0, undf_w0, map_w0, &
                                    ndf_w1, undf_w1, map_w1, &
                                    diff_basis_w1_on_w0,     &
                                    diff_basis_w1_on_w1)

    implicit none

    integer(kind=i_def), intent(in) :: nlayers
    integer(kind=i_def), intent(in) :: ndf_w0
    integer(kind=i_def), intent(in) :: ndf_w1
    integer(kind=i_def), intent(in) :: undf_w0, undf_w1
    integer(kind=i_def), intent(in), dimension(ndf_w0) :: map_w0
    integer(kind=i_def), intent(in), dimension(ndf_w1) :: map_w1
    real(kind=r_def), intent(inout), dimension(undf_w0) :: f0
    real(kind=r_def), intent(in), dimension(undf_w1)    :: f1
    real(kind=r_def), intent(in), dimension(3,ndf_w1,ndf_w0) :: diff_basis_w1_on_w0
    real(kind=r_def), intent(in), dimension(3,ndf_w1,ndf_w1) :: diff_basis_w1_on_w1

  end subroutine testkern_eval_2fs_code

end module testkern_eval_2fs_mod
