from datetime import datetime
from sqlalchemy.orm import Session

import src.databases.schema as themes_schema
import src.databases.model as questions_model


def create_question(db: Session, question: themes_schema.Question):
    try:
        new_question = questions_model.Question(
            question=question.question,
            tag=question.tag,
            ja=question.ja,
            created_at=datetime.now(),
        )
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
    except Exception as e:
        db.rollback()
        return False
    return question


def get_all_question(db: Session):
    question = db.query(questions_model.Question).all()
    if not question:
        return False
    return question


def delete_question(db: Session, question_id: int):
    question = (
        db.query(questions_model.Question)
        .filter(questions_model.Question.id == question_id)
        .first()
    )
    if not question:
        return False
    db.delete(question)
    db.commit()
    return True
