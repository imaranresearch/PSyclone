! -----------------------------------------------------------------------------
! BSD 3-Clause License
!
! Copyright (c) 2020-2021, Science and Technology Facilities Council.
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
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
! "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
! LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
! FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
! COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
! INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
! BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
! LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
! CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
! LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
! ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
! POSSIBILITY OF SUCH DAMAGE.
! -----------------------------------------------------------------------------
! Author J. Henrichs, Bureau of Meteorology
! Modified I. Kavcic, Met Office

!> This module implements a NAN verification for the LFRic API
!! 

module nan_test_psy_data_mod
    use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                              real32, real64, &
                                              stderr=>Error_Unit
    use field_mod, only : field_type
    use nan_test_base_mod, only : NANTestBaseType, is_enabled

    implicit none

    type, extends(NANTestBaseType), public:: nan_test_PSyDataType

    contains
        ! The LFRic-specific procedures defined here
        procedure :: DeclareField,  ProvideField
        procedure :: DeclareFieldVector,  ProvideFieldVector

        ! Declare generic interface for PreDeclareVariable:
        generic, public :: PreDeclareVariable => &
            DeclareField,                        &
            DeclareFieldVector

        !> The generic interface for providing the value of variables
        !! (which checks for non normal IEEE numbers)
        generic, public :: ProvideVariable => &
            ProvideField,                     &
            ProvideFieldVector
                                              
    end type nan_test_PSyDataType

contains

    ! -------------------------------------------------------------------------
    !> This subroutine does not do anything (as declaration is not needed
    !! for NAN checking).
    !! @param[in,out] this The instance of the nan_test_PSyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    !! @param[in,out] this The instance of the nan_test_PSyDataType.
    subroutine DeclareField(this, name, value)
        implicit none
        class(nan_test_PSyDataType), intent(inout), target :: this
        character(*), intent(in) :: name
        type(field_type), intent(in) :: value

    end subroutine DeclareField

    ! -------------------------------------------------------------------------
    !> This subroutine checks whether an LFRic field has NAN or infinite
    !! floating point values.
    !! @param[in,out] this The instance of the nan_test_PSyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine ProvideField(this, name, value)
        use field_mod, only : field_type, field_proxy_type
        implicit none

        class(nan_test_PSyDataType), intent(inout), target :: this
        character(*), intent(in)                           :: name
        type(field_type), intent(in)                       :: value

        type(field_proxy_type) :: value_proxy
        
        if (.not. is_enabled) return

        if (this%verbosity>1) then
            write(stderr, *) "PSyData - testing ", name
        endif
        value_proxy = value%get_proxy()
        call this%ProvideVariable(name, value_proxy%data)
    end subroutine ProvideField

    ! -------------------------------------------------------------------------
    !> This subroutine declares LFRic vector fields. No functionality is
    !! needed here, so it is just an empty function.
    !! @param[in,out] this The instance of the nan_test_PSyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    subroutine DeclareFieldVector(this, name, value)
        use field_mod, only : field_type
        implicit none

        class(nan_test_PSyDataType), intent(inout), target :: this
        character(*), intent(in)                           :: name
        type(field_type), dimension(:), intent(in)         :: value
    end subroutine DeclareFieldVector

    ! -------------------------------------------------------------------------
    !> This subroutine checks whether an LFRic vector field has NAN or
    !! infinite floating point values.
    !! @param[in,out] this The instance of the nan_test_PSyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[in] value The vector of fields.
    subroutine ProvideFieldVector(this, name, value)
        use field_mod, only : field_type
        implicit none

        class(nan_test_PSyDataType), intent(inout), target :: this
        character(*), intent(in)                           :: name
        type(field_type), dimension(:), intent(in)         :: value

        integer      :: i
        character(8) :: index_string   ! Enough for a 6 digit number plus '()'

        if (.not. is_enabled) return

        ! Provide each member of the vector as a normal field. This way
        ! the NAN/infinite testing will be done for each member individually.
        do i=1, size(value, 1)
            write(index_string, '("(",i0,")")') i
            call this%ProvideVariable(name//trim(index_string), value(i))
        enddo
    end subroutine ProvideFieldVector

    ! -------------------------------------------------------------------------
    
end module nan_test_psy_data_mod

