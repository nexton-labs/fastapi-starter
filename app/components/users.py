from sqlalchemy.orm import Session

from app.models.api.user import (
    UserCreateDB,
    UserSignup,
    UserInvitation,
    UserUpdateDB,
)
from app.models.orm.user import User
from app.repositories import user_repo, role_repo
from app.utils.cognito_management import cognito_management
from app.utils.constants import Role as RoleEnum


class UserComponent:
    def signup(self, db: Session, data: UserSignup) -> User:
        if data.email:
            existing_user = user_repo.get_by_username(db=db, username=data.email)  # type: ignore
            if existing_user:
                raise ValueError("There already exist a user with the email")
        else:
            existing_user = user_repo.get_by_username(db=db, username=data.phone)  # type: ignore
            if existing_user:
                raise ValueError("There already exist a user with the phone")

        user_create = UserCreateDB(
            username=data.email if data.email else data.phone,
            email=data.email,
            phone=data.phone,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        user: User = user_repo.create(db=db, obj_in=user_create)

        if data.email:
            cognito_management.sign_up_by_email(
                email=user.username,
                password=data.password,
                user_id=user.id,  # type: ignore
                phone=data.phone,
            )
        else:
            cognito_management.sign_up_by_phone(
                phone=user.username,
                password=data.password,
                user_id=user.id,  # type: ignore
                email=data.email,
            )
        return user

    def invitation(self, db: Session, data: UserInvitation) -> User:
        if data.email:
            existing_user = user_repo.get_by_username(db=db, username=data.email)  # type: ignore
            if existing_user:
                raise ValueError("There already exist a user with the email")
        else:
            existing_user = user_repo.get_by_username(db=db, username=data.phone)  # type: ignore
            if existing_user:
                raise ValueError("There already exist a user with the phone")

        user_create = UserCreateDB(
            username=data.email if data.email else data.phone,
            email=data.email,
            phone=data.phone,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        user: User = user_repo.create(db=db, obj_in=user_create)

        if data.email:
            cognito_management.invite_user_by_email(
                email=user.username,
                user_id=user.id,  # type: ignore
                resend=False,
                phone=data.phone,
            )
        else:
            cognito_management.invite_user_by_phone(
                phone=user.username,
                user_id=user.id,  # type: ignore
                resend=False,
                email=data.email,
            )
        return user

    def invitation_reminder(self, user: User) -> User:
        if user.username == user.email:
            cognito_management.invite_user_by_email(
                email=user.email, user_id=user.id, phone=user.phone, resend=True  # type: ignore
            )
        elif user.username == user.phone:
            cognito_management.invite_user_by_phone(
                phone=user.phone, user_id=user.id, email=user.email, resend=True  # type: ignore
            )
        return user

    def resend_invitation(self, db: Session, user: User, data: UserInvitation) -> User:
        old_username = user.username
        username = None
        if data.email:
            username = data.email
        if data.phone:
            username = data.phone

        user_update = UserUpdateDB(
            username=username, email=data.email, phone=data.phone
        )
        user = user_repo.update(db=db, db_obj=user, obj_in=user_update)

        cognito_management.delete_user(username=old_username,)

        if user.username == data.email:
            cognito_management.invite_user_by_email(
                email=user.username,
                user_id=user.id,  # type: ignore
                resend=False,
                phone=user.phone,
            )
        elif user.username == data.phone:
            cognito_management.invite_user_by_phone(
                phone=user.username,
                user_id=user.id,  # type: ignore
                resend=False,
                email=user.email,
            )
        return user

    def add_role(self, db: Session, user: User, role: RoleEnum) -> User:
        existing_role = role_repo.get_by_name(db=db, name=role.name)  # type: ignore
        if not existing_role:
            raise ValueError("The role does not exist")

        user = user_repo.add_role(db=db, user=user, role=existing_role)
        return user

    def remove_role(self, db: Session, user: User, role: RoleEnum) -> User:
        existing_role = role_repo.get_by_name(db=db, name=role.name)  # type: ignore
        if not existing_role:
            raise ValueError("The role does not exist")

        user = user_repo.remove_role(db=db, user=user, role=existing_role)
        return user


user_component = UserComponent()
