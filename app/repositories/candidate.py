# type: ignore
from typing import List
from uuid import UUID

from app.db.session import Session
from app.models.api.candidate import CandidateCreate, CandidateUpdate
from app.models.orm.candidate import Candidate
from app.repositories.base import BaseRepository


class CandidateRepository(BaseRepository[Candidate, CandidateCreate, CandidateUpdate]):
    def find_by_user_id(self, user_id: UUID, db: Session) -> List[Candidate]:
        return db.query(self.model).filter(Candidate.user_id == user_id).all()

    def create_by_user_id(
        self, user_id: UUID, obj_in: CandidateCreate, db: Session
    ) -> Candidate:
        db_candidate = self.model(
            name=obj_in.name,
            email=obj_in.email,
            linkedin_url=obj_in.linkedin_url,
            user_id=user_id,
        )

        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)
        return db_candidate


candidate_repo = CandidateRepository(Candidate)
