from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from src import db
from ...databases import model, crud, schema


model.Base.metadata.create_all(bind=db.engine)

router = APIRouter(
    prefix="/qustion",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)

load_dotenv()


@router.get(
    "/all",
)
async def get_all_question(db: Session = Depends(db.db_session)):
    """
    get all question from json file.
    """
    try:
        all_questions = crud.get_all_question(db)
        if not all_questions:
            raise HTTPException(
                status_code=200, detail="success but question not found"
            )
        return all_questions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"unexpected error: {str(e)}")


@router.post(
    "/create",
)
async def create_question(
    question: schema.Themes,
    db: Session = Depends(db.db_session),
):
    """
    create question from json file.
    """
    try:
        new_question = crud.create_question(db, question)
        if not new_question:
            raise HTTPException(status_code=500, detail="failed to create question")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"unexpected error: {str(e)}")
    return JSONResponse(status_code=200, content={"created": "success"})


@router.delete(
    "/delete/{question_id}",
)
async def delete_question(
    question_id: int,
    db: Session = Depends(db.db_session),
):
    """
    delete question from json file.
    """
    try:
        deleted_question = crud.delete_question(db, question_id)
        if not deleted_question:
            raise HTTPException(status_code=500, detail="failed to delete question")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"unexpected error: {str(e)}")
    return JSONResponse(
        content={"question": "deleted", "deleted_question": deleted_question}
    )
