from datetime import datetime
from sqlalchemy.orm import Session

import src.databases.schema as schema
import src.databases.model as model


def create_question(db: Session, question: schema.Question):
    try:
        new_question = model.Question(
            question=question.question,
            tag=question.tag,
            detail=question.detail,
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
    question = db.query(model.Question).all()
    if not question:
        return False
    return question


def delete_question(db: Session, question_id: int):
    question = db.query(model.Question).filter(model.Question.id == question_id).first()
    if not question:
        return False
    db.delete(question)
    db.commit()
    return True


def create_score(db: Session, score: schema.Score):
    try:
        new_score = model.Score(
            id=score.id,
            score=score.score,
            nickname=score.nickname,
            created_at=datetime.now(),
        )
        db.add(new_score)
        db.commit()
        db.refresh(new_score)
    except Exception as e:
        db.rollback()
        return False
    return score
