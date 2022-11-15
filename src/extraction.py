import re
import pandas as pd
import pandas as pd
import sqlalchemy as sqlalc
from getpass import getpass
import re
from sqlalchemy import exc

# EXTRACTION


def get_episode(path, episode):
    contenu = open(path, "r")
    script = contenu.read()
    my_serie = re.split(r"\n\n([A-Z]+ ?[A-Z]+)\n", script)
    list_name = []
    for i in range(1, len(my_serie), 2):
        dic = {}
        dic['name'] = my_serie[i]
        dic['text'] = my_serie[i+1]
        list_name.append(dic)

    df = pd.DataFrame(list_name)
    df["episode"] = episode
    return df

# LOADING


def connect_engine(password):
    dbName = "twin_peaks"
    connection_data = f"mysql+pymysql://root:{password}@localhost/{dbName}"
    engine = sqlalc.create_engine(connection_data)
    return engine

# checking existence before creating


def check(something, string):

    if something == "actor":
        query = list(engine.execute(
            f"SELECT name FROM actor WHERE name = '{string}';"))
        if len(query) > 0:
            return True
        else:
            return False

    if something == "episode":
        query = list(engine.execute(
            f"SELECT number FROM episode WHERE name = '{string}';"))
        if len(query) > 0:
            return True
        else:
            return False

# insert characters' names into db


def insertActor(actor_name):
    if check("actor", actor_name):
        return "It already exists"
    else:
        engine.execute(f"INSERT INTO actor (name) VALUES ('{actor_name}');")


# insert text for each character for each episode into script table
def insertScript(script, idepisode, idname):
    queryString = f"insert into script (`text` , idepisode, name) VALUES ('{script}', '{idepisode}', '{idname}');"
    # print(queryString)
    engine.execute(queryString)

# insert episode into episode table


def insertEpisode(number, season):
    engine.execute(
        f"INSERT INTO episode (number, season) VALUES ('{number}','{season}');")


def getcompound(name_):
    sql_df = pd.read_sql_query(
    f"""
    SELECT * from SCRIPT
    WHERE script.name = '{name_}';
    """, engine)
    df_polarity = requests.get(f"http://127.0.0.1:9000/sa/{name_}/").json()
    polarity_series = pd.Series(df_polarity)
    df_with_compound = pd.concat([sql_df,polarity_series], axis=1)
    df_with_compound.rename({0:"Compound"}, axis='columns', inplace=True)
    return df_with_compound
    