# type: ignore
from typing import List
from uuid import UUID

from fastapi import UploadFile

from app.db.session import Session
from app.models.api.candidate import Candidate as CandidateDto, CandidateUpdate
from app.models.api.candidate import CandidateCreate
from app.models.orm.candidate import Candidate
from app.repositories import candidate_repo, job_repo
from app.settings.globals import AWS_IMG_BUCKET, CANDIDATE_AVATAR_PATH
from app.utils.file_management import file_management


class CandidateService:
    ALLOWED_AVATAR_TYPES = ["image/jpeg"]

    def create(
        self, user_id: UUID, candidate: CandidateCreate, db: Session
    ) -> CandidateDto:
        candidate = candidate_repo.create_by_user_id(
            user_id=user_id, obj_in=candidate, db=db
        )
        return CandidateDto.from_orm(candidate)

    def get_user_candidates(self, user_id: UUID, db: Session) -> List[CandidateDto]:
        return candidate_repo.find_by_user_id(db=db, user_id=user_id)

    def add_job(self, candidate_id: UUID, job_id: UUID, db: Session) -> CandidateDto:
        candidate = candidate_repo.find(db=db, model_id=candidate_id)
        job_repo.attach_job_to_candidate(candidate, job_id, db=db)
        return CandidateDto.from_orm(candidate)

    def set_candidate_avatar(
        self, candidate_id: UUID, file: UploadFile, db: Session
    ) -> str:
        candidate = candidate_repo.find(db=db, model_id=candidate_id)
        if not candidate:
            raise ValueError("Candidate does not exist")

        if not file or not file.filename or not file.file:
            raise ValueError("File must not be null")
        if file.content_type not in self.ALLOWED_AVATAR_TYPES:
            raise ValueError("File extension not allowed")

        file_name = self.generate_avatar_path(candidate)
        file_management.upload_file(file.file, file_name, AWS_IMG_BUCKET)

        candidate_update = CandidateUpdate(
            name=candidate.name,
            email=candidate.email,
            linkedin_url=candidate.linkedin_url,
            avatar_path=file_name,
        )
        candidate_repo.update(db=db, db_obj=candidate, obj_in=candidate_update)
        return file_name

    def generate_avatar_path(self, candidate: Candidate) -> str:
        return CANDIDATE_AVATAR_PATH.format(candidate_id=candidate.id)


candidate_service = CandidateService()
