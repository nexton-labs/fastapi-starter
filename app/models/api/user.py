import datetime
from typing import Optional, List
from uuid import UUID

import phonenumbers
from phonenumbers import NumberParseException
from pydantic import Field, BaseModel, validator, root_validator

from app.models.orm.user import User
from app.settings.globals import MFA_ENABLED
from app.utils.avatar import get_avatar_path_base64
from app.utils.constants import Gender, Role
from app.utils.password import verify_password_policy


class UserDetails(BaseModel):
    id: UUID = Field(..., description="User identifier")
    first_name: str = Field(..., description="User first name", example="Carl")
    last_name: str = Field(..., description="User last name", example="Wilson")
    username: str = Field(
        ...,
        description="User username",
        example="carl.wilson@example.ia or +1 345998789",
    )
    email: Optional[str] = Field(
        None, description="User email", example="carl.wilson@example.ia"
    )
    phone: Optional[str] = Field(None, description="User phone", example="+1 345998789")
    gender: Optional[Gender] = Field(None, description="User gender")
    dob: Optional[datetime.datetime] = Field(None, description="User date of bird")
    avatar_url: Optional[str] = Field(None, description="User avatar base64 URL")
    has_consented: bool = Field(
        None, description="True if user has accepted application consents"
    )
    has_consented_date: Optional[datetime.datetime] = Field(
        None, description="Date when user has consented"
    )
    roles: List[Role] = Field([], description="List of user roles")

    @classmethod
    def from_model(cls, instance: User):
        return cls(
            id=instance.id,
            first_name=instance.first_name,
            last_name=instance.last_name,
            username=instance.username,
            email=instance.email,
            phone=instance.phone,
            gender=instance.gender,
            dob=instance.dob,
            avatar_url=get_avatar_path_base64(instance.avatar_path),
            has_consented=instance.has_consented,
            has_consented_date=instance.has_consented_date,
            roles=[role.name for role in instance.roles],  # type: ignore
        )


class UserMinimal(BaseModel):
    id: UUID = Field(..., description="User identifier")
    first_name: str = Field(..., description="User first name", example="Carl")
    last_name: str = Field(..., description="User last name", example="Wilson")
    avatar_url: Optional[str] = Field(None, description="User avatar base64 URL")


class UserCreateDB(BaseModel):
    first_name: str = Field(..., description="User first name", example="Carl")
    last_name: str = Field(..., description="User last name", example="Wilson")
    email: Optional[str] = Field(
        None, description="User email", example="carl.wilson@example.ia"
    )
    phone: Optional[str] = Field(None, description="User phone", example="+1 345998789")
    username: str = Field(..., description="User username", example="carl.wilson")
    gender: Optional[Gender] = Field(None, description="User gender")
    dob: Optional[datetime.datetime] = Field(None, description="User date of bird")
    has_consented: bool = Field(
        False, description="True if user has accepted application consents"
    )
    has_consented_date: Optional[datetime.datetime] = Field(
        None, description="Date when user has consented"
    )


class UserUpdateDB(BaseModel):
    first_name: Optional[str] = Field(
        None, description="User first name", example="Carl"
    )
    last_name: Optional[str] = Field(
        None, description="User last name", example="Wilson"
    )
    email: Optional[str] = Field(
        None, description="User email", example="carl.wilson@example.ia"
    )
    phone: Optional[str] = Field(None, description="User phone", example="+1 345998789")
    username: Optional[str] = Field(
        None, description="User username", example="carl.wilson"
    )
    gender: Optional[Gender] = Field(None, description="User gender")
    dob: Optional[datetime.datetime] = Field(None, description="User date of bird")
    avatar_path: Optional[str] = Field(None, description="User avatar path")
    has_consented: bool = Field(
        None, description="True if user has accepted application consents"
    )
    has_consented_date: Optional[datetime.datetime] = Field(
        None, description="Date when user has consented"
    )


class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(
        None, description="User first name", example="Carl"
    )
    last_name: Optional[str] = Field(
        None, description="User last name", example="Wilson"
    )
    gender: Optional[Gender] = Field(None, description="User gender")
    dob: Optional[datetime.datetime] = Field(None, description="User date of bird")
    avatar_path: Optional[str] = Field(None, description="User avatar path")
    has_consented: bool = Field(
        None, description="True if user has accepted application consents"
    )


class UserInvitation(BaseModel):
    email: Optional[str] = Field(
        None, description="User email", example="carl.wilson@toi.ia"
    )
    phone: Optional[str] = Field(None, description="User phone", example="+1 345998789")
    first_name: Optional[str] = Field(
        None, description="User first name", example="Carl"
    )
    last_name: Optional[str] = Field(
        None, description="User last name", example="Wilson"
    )

    @root_validator
    def check_email_or_phone(cls, values):  # pylint: disable=E0213
        email, phone = values.get("email"), values.get("phone")
        if MFA_ENABLED:
            if phone is None:
                raise ValueError("The phone of the patient is required due to MFA")
        else:
            if email is None and phone is None:
                raise ValueError(
                    "The email or phone of the patient is needed to send the invite"
                )
        return values

    @validator("phone")
    def phone_format(cls, value):  # pylint: disable=E0213
        try:
            if not phonenumbers.is_valid_number(phonenumbers.parse(value, None)):
                raise ValueError("The phone number is not in the correct format")
        except NumberParseException:
            raise ValueError("The phone number is not in the correct format")
        return value


class UserSignup(UserInvitation):
    password: str = Field(..., description="User password", example="Example1234!")

    @validator("password")
    def password_policy(cls, value):  # pylint: disable=E0213
        password_problems = verify_password_policy(value)
        for problem in password_problems:
            if problem == "length":
                raise ValueError("too short")
            if problem == "upper":
                raise ValueError("must contain upper case characters")
            if problem == "lower":
                raise ValueError("must contain lower case characters")
            if problem == "digit":
                raise ValueError("must contain digits")
        return value
