from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.components import user_component
from app.models.api.candidate import (
    CandidateDetails,
    CandidateMinimal,
    CandidateCreateDB,
)
from app.models.api.user import UserInvitation, UserSignup
from app.models.orm.job import Job
from app.repositories import candidate_repo, job_repo
from app.utils.constants import Role


class CandidateService:
    def invite(self, db: Session, data: UserInvitation) -> CandidateDetails:
        user = user_component.invitation(db=db, data=data)
        user = user_component.add_role(db=db, user=user, role=Role.CANDIDATE)
        candidate_create = CandidateCreateDB()
        candidate = candidate_repo.create_candidate(
            db=db, user_id=user.id, data=candidate_create  # type: ignore
        )
        candidate_schema: CandidateDetails = CandidateDetails.from_model(candidate)
        return candidate_schema

    def resend_invitation(
        self, db: Session, candidate_id: UUID, data: UserInvitation
    ) -> CandidateDetails:
        candidate = candidate_repo.find(db=db, model_id=candidate_id)
        user_component.resend_invitation(db=db, user=candidate.user, data=data)
        # candidate = candidate_repo.find(db=db, model_id=candidate_id)
        candidate_schema: CandidateDetails = CandidateDetails.from_model(candidate)
        return candidate_schema

    def invitation_reminder(self, db: Session, candidate_id: UUID) -> CandidateDetails:
        candidate = candidate_repo.find(db=db, model_id=candidate_id)
        user_component.invitation_reminder(user=candidate.user)
        # candidate = candidate_repo.find(db=db, model_id=candidate_id)
        candidate_schema: CandidateDetails = CandidateDetails.from_model(candidate)
        return candidate_schema

    def signup(self, db: Session, data: UserSignup) -> CandidateDetails:
        user = user_component.signup(db=db, data=data)
        user = user_component.add_role(db=db, user=user, role=Role.CANDIDATE)
        candidate_create = CandidateCreateDB()
        candidate = candidate_repo.create_candidate(
            db=db, user_id=user.id, data=candidate_create  # type: ignore
        )
        candidate_schema: CandidateDetails = CandidateDetails.from_model(candidate)
        return candidate_schema

    def get_all(self, db: Session) -> List[CandidateMinimal]:
        candidates = candidate_repo.find_multi(db=db, limit=100)
        candidate_schemas: List[CandidateMinimal] = []
        for candidate in candidates:
            candidate_schemas.append(CandidateDetails.from_model(candidate))
        return candidate_schemas

    def get_details(self, db: Session, candidate_id: UUID) -> CandidateDetails:
        candidate = candidate_repo.find(db=db, model_id=candidate_id)
        candidate_schema: CandidateDetails = CandidateDetails.from_model(candidate)
        return candidate_schema

    def add_jobs(
        self, db: Session, candidate_id: UUID, job_ids: List[UUID]
    ) -> CandidateDetails:
        candidate = candidate_repo.find(db=db, model_id=candidate_id)

        jobs: List[Job] = []
        for job_id in job_ids:
            job = job_repo.find(db=db, model_id=job_id)
            jobs.append(job)

        candidate = candidate_repo.add_jobs(db=db, candidate=candidate, jobs=jobs)
        candidate_schema: CandidateDetails = CandidateDetails.from_model(candidate)
        return candidate_schema

    def remove_jobs(
        self, db: Session, candidate_id: UUID, job_ids: List[UUID]
    ) -> CandidateDetails:
        candidate = candidate_repo.find(db=db, model_id=candidate_id)

        jobs: List[Job] = []
        for job_id in job_ids:
            job = job_repo.find(db=db, model_id=job_id)
            jobs.append(job)

        candidate = candidate_repo.remove_jobs(db=db, candidate=candidate, jobs=jobs)
        candidate_schema: CandidateDetails = CandidateDetails.from_model(candidate)
        return candidate_schema


candidate_service = CandidateService()
