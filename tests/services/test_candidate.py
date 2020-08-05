# type: ignore
from app.models.api.candidate import CandidateCreate
from app.models.orm.user import User
from app.services.api import candidate_service
from app.repositories import candidate_repo


def test_create_candidate(db):
    assert not candidate_repo.find_multi(db)

    test_user = User(username="test1", email="test@email.com")
    db.add(test_user)
    db.commit()

    test_candidate = CandidateCreate(
        name="test candidate",
        email="test@testing.com",
        linkedin_url="https://linkedin.com/in/test",
    )

    candidate_service.create(user_id=test_user.id, db=db, candidate=test_candidate)

    assert candidate_repo.find_multi(db)
