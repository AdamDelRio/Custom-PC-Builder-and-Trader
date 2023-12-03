import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np


def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

num_users = 200000
fake = Faker()
posts_sample_distribution = np.random.default_rng().negative_binomial(0.04, 0.01, num_users)
category_sample_distribution = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                 num_users,
                                                p=[0.1, 0.05, 0.1, 0.3, 0.05, 0.05, 0.05, 0.05, 0.15, 0.1])
total_posts = 0

# create fake posters with fake names and birthdays
with engine.begin() as conn:
    print("creating fake posters...")
    posts = []
    for i in range(num_users):
        if (i % 10 == 0):
            print(i)
        

        email = fake.unique.email()
        username = email.split('@')[0]

        poster_id = conn.execute(sqlalchemy.text("""
        INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id;
        """), {"username": username, "email": email, }).fetchone()[0]

    print("total posts: ", total_posts)
    