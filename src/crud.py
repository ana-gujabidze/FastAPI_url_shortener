# src/crud.py

from sqlalchemy.orm import Session

import keygen
import models
import schemas


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    # delete URLs older than 30 days
    sql = "DELETE FROM urls WHERE created_at < datetime ('now', '-30 day')"
    db.execute(sql)
    # create short code for shortened URL
    if url.custom_code and url.custom_code != "string":
        key = url.custom_code
    else:
        key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=5)}"
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key)
        .first()
    )


def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key)
        .first()
    )


def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url
