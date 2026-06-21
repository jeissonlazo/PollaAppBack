from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.prediction import (
    PredictionUpdate,
    UserPredictionResponse,
    UserPredictionCreate,
    UsersMatchPredictionResponse,
)

from app.services.prediction_service import (
    get_group_match_predictions,
    get_user_predictions_by_group,
    save_predictions,
    update_prediction,
)

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)


@router.get("/group/{group_id}/user/{user_id}", response_model=UserPredictionResponse)
def get_user_predictions_endpoint(
    group_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db)
):

    prediction_set = get_user_predictions_by_group(
        db=db, user_id=user_id, group_id=group_id
    )
    print(prediction_set)
    if not prediction_set:
        return {
            "user_id": str(user_id),
            "group_id": str(group_id),
            "user_score": 0,
            "predictions": [],
        }

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


@router.put("/{prediction_id}")
def update_prediction_endpoint(
    prediction_id: UUID, request: PredictionUpdate, db: Session = Depends(get_db)
):
    prediction = update_prediction(
        db=db,
        prediction_id=prediction_id,
        score_team1=request.score_team1,
        score_team2=request.score_team2,
    )

    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    return prediction


@router.get(
    "/group/{group_id}/match/{match_id}",
    response_model=list[UsersMatchPredictionResponse],
)
def get_group_match_predictions_endpoint(
    group_id: UUID, match_id: UUID, db: Session = Depends(get_db)
):
    try:

        predictions = get_group_match_predictions(
            db=db, group_id=group_id, match_id=match_id
        )

        return predictions

    except Exception as ex:

        raise HTTPException(status_code=403, detail=str(ex))
