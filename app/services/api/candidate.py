# type: ignore
from typing import List
from uuid import UUID

from app.models.api.candidate import Candidate as CandidateDto
from app.models.api.candidate import CandidateCreate
from app.db.session import Session
from app.repositories import candidate_repo, job_repo


class CandidateService:
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


candidate_service = CandidateService()
