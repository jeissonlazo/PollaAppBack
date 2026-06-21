from app.models.prediction import Prediction
from app.models.user_prediction import UserPrediction
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.match import Match
from app.models.user import User

def create_user_predictions(db, user_id, group_id, predictions):
    prediction_set = UserPrediction(user_id=user_id, group_id=group_id)

    db.add(prediction_set)
    db.commit()
    db.refresh(prediction_set)

    for item in predictions:

        prediction = Prediction(
            prediction_set_id=prediction_set.prediction_set_id,
            match_id=item.match_id,
            team1_id=item.team1_id,
            team2_id=item.team2_id,
            score_team1=item.score_team1,
            score_team2=item.score_team2,
        )

        db.add(prediction)

    db.commit()

    return prediction_set


def get_user_predictions_by_group(db: Session, user_id, group_id):
    prediction_set = (
        db.query(UserPrediction)
        .filter(UserPrediction.user_id == user_id, UserPrediction.group_id == group_id)
        .first()
    )
    if not prediction_set:
        return None

    predictions = (
        db.query(Prediction)
        .filter(Prediction.prediction_set_id == prediction_set.prediction_set_id)
        .all()
    )

    return {
        "user_id": prediction_set.user_id,
        "group_id": prediction_set.group_id,
        "user_score": prediction_set.user_score,
        "predictions": predictions,
    }


def save_predictions(db, user_id, group_id, predictions):
    prediction_set = (
        db.query(UserPrediction)
        .filter(UserPrediction.user_id == user_id, UserPrediction.group_id == group_id)
        .first()
    )

    if not prediction_set:

        prediction_set = UserPrediction(user_id=user_id, group_id=group_id)

        db.add(prediction_set)
        db.commit()
        db.refresh(prediction_set)

    for item in predictions:

        existing_prediction = (
            db.query(Prediction)
            .filter(
                Prediction.prediction_set_id == prediction_set.prediction_set_id,
                Prediction.match_id == item.match_id,
            )
            .first()
        )
        if existing_prediction:

            # No permitir editar partidos terminados

            if existing_prediction.ended:
                continue

            existing_prediction.score_team1 = item.score_team1

            existing_prediction.score_team2 = item.score_team2

        else:

            prediction = Prediction(
                prediction_set_id=prediction_set.prediction_set_id,
                match_id=item.match_id,
                team1_id=item.team1_id,
                team2_id=item.team2_id,
                score_team1=item.score_team1,
                score_team2=item.score_team2,
            )
            print("Adding new prediction")
            db.add(prediction)

    db.commit()

    return prediction_set


def update_prediction(db, prediction_id, score_team1, score_team2):
    prediction = (
        db.query(Prediction).filter(Prediction.prediction_id == prediction_id).first()
    )

    if not prediction:
        return None

    match = db.query(Match).filter(Match.match_id == prediction.match_id).first()

    if not match:
        raise Exception("Match not found")

    if match.match_date <= datetime.utcnow():
        raise Exception("Predictions can no longer be edited")

    prediction.score_team1 = score_team1
    prediction.score_team2 = score_team2

    db.commit()
    db.refresh(prediction)

    return prediction


def get_group_match_predictions(db, group_id, match_id):

    match = db.query(Match).filter(Match.match_id == match_id).first()

    if not match:
        return None

    predictions = (
        db.query(
            User.username,
            User.id.label("user_id"),
            User.first_name,
            User.last_name,
            Prediction.score_team1,
            Prediction.score_team2,
        )
        .join(
            UserPrediction,
            Prediction.prediction_set_id == UserPrediction.prediction_set_id,
        )
        .join(
            User,
            UserPrediction.user_id == User.id,
        )
        .filter(
            UserPrediction.group_id == group_id,
            Prediction.match_id == match_id,
        )
        .all()
    )

    if predictions is None:
        return None

    # Ocultar resultados hasta que empiece el partido
    if match.match_date <= datetime.utcnow():
        return [
            {
                "user_id": prediction.user_id,
                "username": prediction.username,
                "score_team1": prediction.score_team1,
                "score_team2": prediction.score_team2,
                "first_name": prediction.first_name,
                "last_name": prediction.last_name,
            }
            for prediction in predictions
        ]
    else:
        return [
            {
                "user_id": prediction.user_id,
                "username": prediction.username,
                "score_team1": None,
                "score_team2": None,
                "first_name": prediction.first_name,
                "last_name": prediction.last_name,
            }
            for prediction in predictions
        ]

    return predictions
