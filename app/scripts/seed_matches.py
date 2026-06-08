import json
from datetime import datetime

from app.core.database import SessionLocal
from app.models.match import Match
from app.models.team import Team

def seed_matches():

    db = SessionLocal()

    with open("matches.json", "r", encoding="utf-8") as file:
        matches_data = json.load(file)

    for item in matches_data:

        team1 = (
            db.query(Team)
            .filter(
              (Team.country == item["team1"]) |
              (Team.code == item["team1"])
            )
            .first()
        )

        team2 = (
            db.query(Team)
            .filter(
              (Team.country == item["team2"]) |
              (Team.code == item["team2"])
            )
            .first()
        )

        defined = team1 is not None and team2 is not None

        match_date = datetime.strptime(
            item["date"],
            "%Y-%m-%d"
        )

        new_match = Match(
            round=item["round"],
            match_date=match_date,
            time=item["time"],
            group_name=item.get("group", ""),
            ground=item["ground"],

            team1_id=team1.team_id if team1 else None,
            team2_id=team2.team_id if team2 else None,

            score_team1=0,
            score_team2=0,

            finish=False,
            defined=defined
        )

        db.add(new_match)

    db.commit()
    db.close()

    print("Matches seeded successfully")


if __name__ == "__main__":
    seed_matches()