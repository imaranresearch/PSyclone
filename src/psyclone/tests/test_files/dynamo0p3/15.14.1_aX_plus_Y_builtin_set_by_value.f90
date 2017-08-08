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

  ! Description: single point-wise operation specified in an invoke call
  ! with scalar passed by value which includes explicit kind param.
  use testkern, only: testkern_type
  use inf,      only: field_type
  implicit none
  type(field_type) :: f1, f2, f3

  call invoke( aX_plus_Y(f3, 0.5_r_def, f1, f2) )

end program single_invoke
