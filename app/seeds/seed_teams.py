# app/seeds/seed_teams.py

import json
from pathlib import Path

from app.core.database import SessionLocal
from app.models.team import Team


def seed_teams():

    db = SessionLocal()

    try:

        root_path = Path(__file__).resolve().parents[2]

        json_file = root_path / "teams.json"

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as file:
            teams = json.load(file)

        inserted = 0
        skipped = 0

        for team in teams:

            exists = (
                db.query(Team)
                .filter(
                    Team.code == team["code"]
                )
                .first()
            )

            if exists:
                skipped += 1
                continue

            new_team = Team(
                country=team["country"],
                code=team["code"],
                flag=team["flag"]
            )

            db.add(new_team)

            inserted += 1

        db.commit()

    except Exception as ex:

        db.rollback()

    finally:

        db.close()


if __name__ == "__main__":
    seed_teams()
