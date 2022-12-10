import pandas as pd

from sqlalchemy import create_engine


if __name__ == "__main__":
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
    # random query to test agains DB
    query = "select * from public.stg_prepared_source ps where ps.new_active > ps.active;"
    df = pd.read_sql(query, engine)
    print(df)
