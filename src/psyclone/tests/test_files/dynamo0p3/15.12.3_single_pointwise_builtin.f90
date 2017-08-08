! Modifications copyright (c) 2017, Science and Technology Facilities Council
!-------------------------------------------------------------------------------
! (c) The copyright relating to this work is owned jointly by the Crown,
! Met Office and NERC 2015.
! However, it has been created with the help of the GungHo Consortium,
! whose members are identified at https://puma.nerc.ac.uk/trac/GungHo/wiki
!-------------------------------------------------------------------------------
! Author A. R. Porter STFC Daresbury Lab
! Modified I. Kavcic Met Office

program single_invoke

  ! Description: single point-wise operation specified in an invoke call.
  ! Check that we raise an appropriate error for mising definitions.
  use testkern, only: testkern_type
  use inf,      only: field_type
  implicit none
  type(field_type) :: f1

  call invoke( setval_c(f1, 0.0) )

end program single_invoke

subroutine expected_code(fld, value)
        do df1 = 1, ndf_w3
           idx = ((cell-1)*nlayers + (k-1))*ndf_w3 + df1
           fld(idx) = value
        end do
end subroutine expected_code
