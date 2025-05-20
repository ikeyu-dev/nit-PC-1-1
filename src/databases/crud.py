from datetime import datetime
from sqlalchemy.orm import Session

import src.databases.schema as themes_schema
import src.databases.model as themes_model


def create_question(db: Session, question: themes_schema.Themes):
    new_question = themes_model.theme(
        question=question.question,
        tag=question.tag,
        ja=question.ja,
        created_at=datetime.now(),
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return question


def get_all_question(db: Session):
    question = db.query(themes_model.theme).all()
    if not question:
        return False
    return question


def delete_question(db: Session, question_id: int):
    question = (
        db.query(themes_model.theme)
        .filter(themes_model.theme.id == question_id)
        .first()
    )
    if not question:
        return False
    db.delete(question)
    db.commit()
    return True
