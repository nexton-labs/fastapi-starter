from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.components import user_component
from app.models.api.user import (
    UserDetails,
    UserUpdateDB,
    UserSignup,
    UserInvitation,
    UserProfileUpdate,
)
from app.models.orm.user import User
from app.repositories import user_repo
from app.settings.globals import AWS_IMG_BUCKET
from app.utils.avatar import generate_user_avatar_path, get_avatar_path_base64
from app.utils.constants import Role
from app.utils.s3_management import s3_management

ALLOWED_AVATAR_TYPES = ["image/jpeg"]


class UserService:
    def signup(self, db: Session, data: UserSignup) -> UserDetails:
        user = user_component.signup(db=db, data=data)
        user_schema: UserDetails = UserDetails.from_model(user)
        return user_schema

    def invitation(self, db: Session, data: UserInvitation) -> UserDetails:
        user = user_component.invitation(db=db, data=data)
        user_schema: UserDetails = UserDetails.from_model(user)
        return user_schema

    def set_avatar(self, db: Session, user: User, file: UploadFile) -> Optional[str]:

        if not file or not file.filename or not file.file:
            raise ValueError("File must not be null")
        if file.content_type not in ALLOWED_AVATAR_TYPES:
            raise ValueError("File extension not allowed")

        file_name = generate_user_avatar_path(user, file.filename)
        s3_management.upload_file(file.file, file_name, AWS_IMG_BUCKET)

        data = UserUpdateDB(avatar_path=file_name)
        updated_user = user_repo.update(db=db, db_obj=user, obj_in=data)
        return get_avatar_path_base64(updated_user.avatar_path)

    def get_profile(
        self, db: Session, user: User,  # pylint: disable=W0613
    ) -> UserDetails:
        user_schema: UserDetails = UserDetails.from_model(user)
        return user_schema

    def update_profile(
        self, db: Session, user: User, data: UserProfileUpdate
    ) -> UserDetails:
        user_update = UserUpdateDB(**data.dict(exclude_unset=True))

        if (
            user_update.has_consented
            and user.has_consented != user_update.has_consented
        ):
            user_update.has_consented_date = datetime.utcnow()

        user = user_repo.update(db=db, db_obj=user, obj_in=user_update)

        user_schema: UserDetails = UserDetails.from_model(user)
        return user_schema

    def create_admin(self, db: Session, data: UserSignup) -> UserDetails:
        user = user_component.signup(db=db, data=data)
        user = user_component.add_role(db=db, user=user, role=Role.ADMIN)

        user_schema: UserDetails = UserDetails.from_model(user)

        return user_schema


user_service = UserService()
