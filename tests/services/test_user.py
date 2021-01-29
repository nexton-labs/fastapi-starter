import pytest
from fastapi import UploadFile

from app.models.api.user import UserProfileUpdate, UserInvitation
from app.services.api import user_service  # type: ignore
from app.utils.cognito_management import CognitoManagement
from app.utils.s3_management import S3Management  # type: ignore
from tests.utils import (
    build_user,
    get_user,
)


def test_get_profile(db):
    user = build_user(db)

    result = user_service.get_profile(db, user=user)
    assert result
    assert result.id == user.id


def test_update_profile(db):
    user = build_user(db)

    data = UserProfileUpdate(
        first_name="update_patient",
        last_name="update",
        gender="MALE",
        has_consented=True,
    )

    updated_user = user_service.update_profile(db=db, user=user, data=data)

    assert data.first_name == updated_user.first_name
    assert data.last_name == updated_user.last_name
    assert data.gender == updated_user.gender
    assert updated_user.gender
    assert updated_user.has_consented_date


def test_set_avatar(db, mocker):
    user = build_user(db)

    file = UploadFile(filename="test_file.png", content_type="image/jpeg")

    mocker.patch.object(S3Management, "upload_file", return_value="")
    mocker.patch.object(S3Management, "generate_presigned_url", return_value="")

    result = user_service.set_avatar(db=db, file=file, user=user)

    updated_user = user_service.get_profile(db=db, user=user)

    assert result
    assert updated_user.avatar_url


def test_set_avatar_file_null(db):
    user = build_user(db)

    with pytest.raises(ValueError):
        user_service.set_avatar(db=db, file=None, user=user)


def test_set_avatar_file_not_allowed(db):
    user = build_user(db)

    file = UploadFile(filename="test_file.txt", content_type="text/plain")

    with pytest.raises(ValueError):
        user_service.set_avatar(db=db, file=file, user=user)


def test_invitation_by_email(db, mocker):
    invitation = UserInvitation(
        email="email@test.com", first_name="FirstName", last_name="LastName",
    )

    mock_cognito_signup = mocker.patch.object(CognitoManagement, "invite_user_by_email")
    result = user_service.invitation(db=db, data=invitation)

    user = get_user(db, user_id=result.id)

    assert result
    assert result.id == user.id
    assert result.username == invitation.email
    assert result.email == invitation.email
    assert result.first_name == invitation.first_name
    assert result.last_name == invitation.last_name

    mock_cognito_signup.assert_called_with(
        email=user.email, user_id=user.id, resend=False, phone=None
    )


def test_invitation_email_not_available(db):
    email = "test@test.com"
    user = build_user(db, email=email)
    invitation = UserInvitation(email=user.email)
    with pytest.raises(ValueError):
        user_service.invitation(db=db, data=invitation)


def test_invitation_by_phone(db, mocker):
    invitation = UserInvitation(
        phone="+543416412222", first_name="FirstName", last_name="LastName",
    )

    mock_cognito_signup = mocker.patch.object(CognitoManagement, "invite_user_by_phone")
    result = user_service.invitation(db=db, data=invitation)

    user = get_user(db, user_id=result.id)

    assert result
    assert result.id == user.id
    assert result.username == invitation.phone
    assert result.phone == invitation.phone
    assert result.first_name == invitation.first_name
    assert result.last_name == invitation.last_name

    mock_cognito_signup.assert_called_with(
        phone=invitation.phone, user_id=user.id, resend=False, email=None
    )


def test_invitation_phone_not_available(db):
    phone = "+543416412222"
    user = build_user(db, phone=phone)
    invitation = UserInvitation(phone=user.phone)

    with pytest.raises(ValueError):
        user_service.invitation(db=db, data=invitation)
