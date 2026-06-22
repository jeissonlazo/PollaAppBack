from sqlalchemy.orm import Session

from app.models.prediction import Prediction
from app.models.user_prediction import UserPrediction

from app.models.match import Match
from app.schemas import match

def calculate_points(
    real_team1: int, real_team2: int, pred_team1: int, pred_team2: int
) -> int:

    points = 0

    # ganador
    real_result = 1 if real_team1 > real_team2 else -1 if real_team1 < real_team2 else 0

    pred_result = 1 if pred_team1 > pred_team2 else -1 if pred_team1 < pred_team2 else 0

    if real_result == pred_result:
        points += 5

    # marcador exacto equipo 1
    if real_team1 == pred_team1:
        points += 2

    # marcador exacto equipo 2
    if real_team2 == pred_team2:
        points += 2

    # diferencia de goles
    real_diff = real_team1 - real_team2
    pred_diff = pred_team1 - pred_team2

    if real_diff == pred_diff:
        points += 1

    return points


def score_match_predictions(db: Session, match: Match):

    predictions = (
        db.query(Prediction).filter(Prediction.match_id == match.match_id).all()
    )

    for prediction in predictions:

        # evitar recalcular dos veces
        if prediction.ended:
            continue

        points = calculate_points(
            match.score_team1,
            match.score_team2,
            prediction.score_team1,
            prediction.score_team2,
        )

        prediction.ended = True

        user_prediction = (
            db.query(UserPrediction)
            .filter(UserPrediction.prediction_set_id == prediction.prediction_set_id)
            .first()
        )
        if user_prediction:
            user_prediction.user_score += points

    db.commit()
