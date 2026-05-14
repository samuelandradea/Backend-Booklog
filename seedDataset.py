import csv
import sys
import time
from firebase.config import db


def seed(csv_path: str, batch_size: int = 500, skip: int = 0, delay: float = 1.5):
    collection = db.collection("books")

    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        batch = db.batch()
        count = 0
        skipped = 0

        for row in reader:
            if skipped < skip:
                skipped += 1
                continue

            doc_ref = collection.document()
            batch.set(doc_ref, {
                "author": row.get("author", ""),
                "bookformat": row.get("bookformat", ""),
                "desc": row.get("desc", ""),
                "genre": row.get("genre", ""),
                "img": row.get("img", ""),
                "isbn": row.get("isbn", ""),
                "isbn13": row.get("isbn13", ""),
                "link": row.get("link", ""),
                "pages": int(row["pages"]) if row.get("pages", "").isdigit() else 0,
                "rating": float(row["rating"]) if row.get("rating") else 0,
                "reviews": int(row["reviews"]) if row.get("reviews", "").isdigit() else 0,
                "title": row.get("title", ""),
                "totalratings": int(row["totalratings"]) if row.get("totalratings", "").isdigit() else 0,
            })
            count += 1

            if count % batch_size == 0:
                batch.commit()
                batch = db.batch()
                print(f"{count + skip} documentos inseridos...")
                time.sleep(delay)

        if count % batch_size != 0:
            batch.commit()

    print(f"Seed finalizado. {count} livros inseridos (skip={skip}).")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "../Booklog/data/data.csv"
    skip = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    seed(path, skip=skip)
