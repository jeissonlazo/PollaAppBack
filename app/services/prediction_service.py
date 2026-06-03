

from app.models.prediction import Prediction
from app.models.user_prediction import UserPrediction
from sqlalchemy.orm import Session

def create_user_predictions(
    db,
    user_id,
    group_id,
    predictions
):
    prediction_set = UserPrediction(
        user_id=user_id,
        group_id=group_id
    )

    db.add(prediction_set)
    db.commit()
    db.refresh(prediction_set)

    for item in predictions:

        prediction = Prediction(
            prediction_set_id=
                prediction_set.prediction_set_id,

            match_id=item.match_id,

            team1_id=item.team1_id,
            team2_id=item.team2_id,

            score_team1=item.score_team1,
            score_team2=item.score_team2
        )

        db.add(prediction)

    db.commit()

    return prediction_set
  
def get_user_predictions_by_group(
    db: Session,
    user_id,
    group_id
):
    prediction_set = (
        db.query(UserPrediction)
        .filter(
            UserPrediction.user_id == user_id,
            UserPrediction.group_id == group_id
        )
        .first()
    )

    if not prediction_set:
        return None

    predictions = (
        db.query(Prediction)
        .filter(
            Prediction.prediction_set_id ==
            prediction_set.prediction_set_id
        )
        .all()
    )

    return {
        "user_id": prediction_set.user_id,
        "group_id": prediction_set.group_id,
        "user_score": prediction_set.user_score,
        "predictions": predictions
    }
    
def save_predictions(
    db,
    user_id,
    group_id,
    predictions
):
    prediction_set = (
        db.query(UserPrediction)
        .filter(
            UserPrediction.user_id == user_id,
            UserPrediction.group_id == group_id
        )
        .first()
    )

    if not prediction_set:

        prediction_set = UserPrediction(
            user_id=user_id,
            group_id=group_id
        )

        db.add(prediction_set)
        db.commit()
        db.refresh(prediction_set)

    for item in predictions:

        existing_prediction = (
            db.query(Prediction)
            .filter(
                Prediction.prediction_set_id ==
                prediction_set.prediction_set_id,

                Prediction.match_id ==
                item.match_id
            )
            .first()
        )

        if existing_prediction:

            # No permitir editar partidos terminados

            if existing_prediction.ended:
                continue

            existing_prediction.score_team1 = (
                item.score_team1
            )

            existing_prediction.score_team2 = (
                item.score_team2
            )

        else:

            prediction = Prediction(
                prediction_set_id=
                    prediction_set.prediction_set_id,

                match_id=item.match_id,

                team1_id=item.team1_id,
                team2_id=item.team2_id,

                score_team1=item.score_team1,
                score_team2=item.score_team2
            )

            db.add(prediction)

    db.commit()

    return prediction_set