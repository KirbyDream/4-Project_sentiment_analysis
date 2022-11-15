import pandas as pd
from config.sql_connection import engine


def get_everything():
    query = """SELECT * FROM script;"""
    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")


def get_everything_from_character(name):
    query = f"""SELECT * 
    FROM script
    WHERE name = '{name}';"""
    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")


def get_just_dialogue(name):
    query = f"""SELECT text 
    FROM script
    WHERE name = '{name}';"""
    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")


def get_just_dialogue_episode(name, episode):
    query = f"""SELECT text 
    FROM script
    WHERE name = '{name}'
    and idepisode = '{episode}';
    """
    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")


def get_dialogue_all_episodes():
    query = f"""SELECT  idepisode, GROUP_CONCAT(text SEPARATOR ' ') as text
FROM script
group by idepisode;
    """
    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")


def insert_one_row(episode, name, text):
    query = f"""INSERT INTO script
     (`text`, idepisode, name) 
        VALUES ({text}, '{episode}', '{name}');
    """
    engine.execute(query)
    return f"Correctly introduced!"
