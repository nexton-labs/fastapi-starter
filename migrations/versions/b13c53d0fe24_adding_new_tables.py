"""adding_new_tables

Revision ID: b13c53d0fe24
Revises: b7341836c6f0
Create Date: 2020-08-03 21:12:31.922119

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b13c53d0fe24"
down_revision = "b7341836c6f0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "jobs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("description"),
        sa.UniqueConstraint("title"),
    )
    candidates = op.create_table(
        "candidates",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("linkedin_url", sa.String(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"],),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("linkedin_url"),
    )
    op.create_table(
        "candidate_jobs",
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("candidate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"],),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"],),
        sa.PrimaryKeyConstraint("candidate_id", "job_id"),
    )
    op.add_column("users", sa.Column("email", sa.String(), nullable=False))
    op.create_unique_constraint(None, "users", ["email"])
    op.drop_column("users", "hashed_password")

    op.bulk_insert(
        candidates,
        [
            {
                "id": "518efc42-4b0e-4618-97f0-c4a5277baecd",
                "name": "Ezequiel",
                "email": "ezequiel.picatto@nextonlabs.com",
                "linkedin_url": "https://www.linkedin.com/in/epicatto/",
            },
        ],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("hashed_password", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "users", type_="unique")
    op.drop_column("users", "email")
    op.drop_table("candidate_jobs")
    op.drop_table("candidates")
    op.drop_table("jobs")
    # ### end Alembic commands ###