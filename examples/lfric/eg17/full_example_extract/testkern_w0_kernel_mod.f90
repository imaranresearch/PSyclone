! BSD 3-Clause License
!
! Copyright (c) 2017-2022, Science and Technology Facilities Council
! All rights reserved.
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
! -----------------------------------------------------------------------------
! Author R. W. Ford, STFC Daresbury Lab
! Modified by J. Henrichs, Bureau of Meteorology
! Modified by I. Kavcic, Met Office

module testkern_w0_kernel_mod

  use argument_mod
  use kernel_mod
  use fs_continuity_mod, only: W0

  use constants_mod

  implicit none

  private

  type, public, extends(kernel_type) :: testkern_w0_kernel_type
     private
     type(arg_type), dimension(4) :: meta_args =       &
          (/ arg_type(gh_field, gh_real, gh_inc,  w0), &
             arg_type(gh_field, gh_real, gh_read, w0), &
             arg_type(gh_field*3, gh_real, gh_read, w0), &
             arg_type(gh_scalar, gh_logical, gh_read)  &
           /)
     integer :: operates_on = cell_column
   contains
     procedure, nopass :: code => testkern_w0_code
  end type testkern_w0_kernel_type

  public :: testkern_w0_code

contains

  subroutine testkern_w0_code(nlayers, fld1, fld2, chi1, chi2, chi3, &
                              some_logical, ndf_w0, undf_w0, map_w0)

    implicit none

    integer(kind=i_def), intent(in)                     :: nlayers
    integer(kind=i_def)                                 :: ndf_w0, undf_w0
    real(kind=r_def), dimension(undf_w0), intent(inout) :: fld1
    real(kind=r_def), dimension(undf_w0), intent(in)    :: fld2
    real(kind=r_def), dimension(undf_w0), intent(in)    :: chi1,chi2,chi3
    logical(kind=l_def), intent(in)                     :: some_logical
    integer(kind=i_def), dimension(ndf_w0)              :: map_w0

    integer(kind=i_def)                                 :: i, k

    do k=0, nlayers-1
      do i=1, ndf_w0
        fld1(map_w0(i)+k) = fld1(map_w0(i)+k) + fld2(map_w0(i)+k)
        if (some_logical) then
          fld1(map_w0(i)+k) = fld1(map_w0(i)+k) + 1
        endif
      end do
    end do

  end subroutine testkern_w0_code

end module testkern_w0_kernel_mod
