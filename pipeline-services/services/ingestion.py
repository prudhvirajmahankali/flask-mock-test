import requests
from sqlalchemy.orm import Session
from models.customer import Customer

FLASK_URL = "http://mock-server:5000/api/customers"

def fetch_all_data():
    page = 1
    limit = 10
    all_data = []

    while True:
        response = requests.get(FLASK_URL, params={"page": page, "limit": limit})
        data = response.json()

        records = data["data"]
        if not records:
            break

        all_data.extend(records)

        if len(all_data) >= data["total"]:
            break

        page += 1

    return all_data


def upsert_data(db: Session, records):
    for r in records:
        existing = db.query(Customer).filter_by(customer_id=r["customer_id"]).first()

        if existing:
            for key, value in r.items():
                setattr(existing, key, value)
        else:
            customer = Customer(**r)
            db.add(customer)

    db.commit()