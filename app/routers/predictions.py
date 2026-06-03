from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.prediction import (
    UserPredictionResponse,
    UserPredictionCreate
)

from app.services.prediction_service import (
    get_user_predictions_by_group,
    save_predictions
)


router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)


@router.get(
    "/group/{group_id}/user/{user_id}",
    response_model=UserPredictionResponse
)
def get_user_predictions_endpoint(
    group_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db)
):

    prediction_set = (
        get_user_predictions_by_group(
            db=db,
            user_id=user_id,
            group_id=group_id
        )
    )

    if not prediction_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Predictions not found"
        )

    return prediction_set
  
@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def save_predictions_endpoint(
    request: UserPredictionCreate,
    db: Session = Depends(get_db)
):
    prediction_set = save_predictions(
        db=db,
        user_id=request.user_id,
        group_id=request.group_id,
        predictions=request.predictions
    )

    return {
        "message": "Predictions saved",
        "prediction_set_id":
            prediction_set.prediction_set_id
    }