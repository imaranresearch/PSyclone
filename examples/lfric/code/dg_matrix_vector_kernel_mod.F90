!-----------------------------------------------------------------------------
! Copyright (c) 2017-2025,  Met Office, on behalf of HMSO and Queen's Printer
! For further details please refer to the file LICENCE.original which you
! should have received as part of this distribution.
!-----------------------------------------------------------------------------
! LICENCE.original is available from the Met Office Science Repository Service:
! https://code.metoffice.gov.uk/trac/lfric/browser/LFRic/trunk/LICENCE.original
! -----------------------------------------------------------------------------
! BSD 3-Clause License
!
! Modifications copyright (c) 2017-2025, Science and Technology Facilities Council
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
! Modified by I. Kavcic, Met Office
! Modified by R. W. Ford, STFC Daresbury Lab
!
module dg_matrix_vector_kernel_mod

  use argument_mod,      only : arg_type,                   &
                                GH_FIELD, GH_OPERATOR,      &
                                GH_REAL, GH_READ, GH_WRITE, &
                                ANY_DISCONTINUOUS_SPACE_1,  &
                                ANY_SPACE_1, GH_READWRITE,  &
                                CELL_COLUMN

  use constants_mod,     only : r_def, i_def
  use kernel_mod,        only : kernel_type

  implicit none

  private

  !----------------------------------------------------------------------------
  ! Public types
  !----------------------------------------------------------------------------

  type, public, extends(kernel_type) :: dg_matrix_vector_kernel_type
    private
    type(arg_type) :: meta_args(3) = (/                                           &
         arg_type(GH_FIELD,    GH_REAL, GH_READWRITE, ANY_DISCONTINUOUS_SPACE_1), &
         arg_type(GH_FIELD,    GH_REAL, GH_READ,      ANY_SPACE_1),               &
         arg_type(GH_OPERATOR, GH_REAL, GH_READ,      ANY_DISCONTINUOUS_SPACE_1,  &
                                                      ANY_SPACE_1)                &
         /)

    integer :: operates_on = CELL_COLUMN
  contains
    procedure, nopass :: dg_matrix_vector_code
  end type

  !----------------------------------------------------------------------------
  ! Contained functions/subroutines
  !----------------------------------------------------------------------------
  public dg_matrix_vector_code

contains

!> @brief Computes lhs = matrix*x for discontinuous function spaces
!> @param[in] cell Horizontal cell index
!> @param[in] nlayers Number of layers
!> @param[in,out] lhs Output lhs (A*x)
!> @param[in] x Input data
!> @param[in] ncell_3d Total number of cells
!> @param[in] matrix Matrix values in LMA form
!> @param[in] ndf1 Number of degrees of freedom per cell for the output field
!> @param[in] undf1 Unique number of degrees of freedom  for the output field
!> @param[in] map1 Dofmap for the cell at the base of the column for the
!!            output field
!> @param[in] map2 Dofmap for the cell at the base of the column for the
!!            input field
!> @param[in] ndf2 Number of degrees of freedom per cell for the input field
!> @param[in] undf2 Unique number of degrees of freedom for the input field
subroutine dg_matrix_vector_code(cell,              &
                                 nlayers,           &
                                 lhs, x,            &
                                 ncell_3d,          &
                                 matrix,            &
                                 ndf1, undf1, map1, &
                                 ndf2, undf2, map2)

  implicit none

  ! Arguments
  integer(kind=i_def),                  intent(in)    :: cell, nlayers, &
                                                         ncell_3d
  integer(kind=i_def),                  intent(in)    :: undf1, ndf1
  integer(kind=i_def),                  intent(in)    :: undf2, ndf2
  integer(kind=i_def), dimension(ndf1), intent(in)    :: map1
  integer(kind=i_def), dimension(ndf2), intent(in)    :: map2
  real(kind=r_def), dimension(undf2),              intent(in)    :: x
  real(kind=r_def), dimension(undf1),              intent(inout) :: lhs
  real(kind=r_def), dimension(ncell_3d,ndf1,ndf2), intent(in)    :: matrix

  ! Internal variables
  integer(kind=i_def)               :: df, k, ik
  real(kind=r_def), dimension(ndf2) :: x_e
  real(kind=r_def), dimension(ndf1) :: lhs_e

  do k = 0, nlayers-1
    do df = 1, ndf2
      x_e(df) = x(map2(df)+k)
    end do
    ik = (cell-1)*nlayers + k + 1
    lhs_e = matmul(matrix(ik,:,:),x_e)
    do df = 1,ndf1
       lhs(map1(df)+k) = lhs_e(df)
    end do
  end do
end subroutine dg_matrix_vector_code

end module dg_matrix_vector_kernel_mod
