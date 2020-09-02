import requests
import pandas as pd
import numpy as np
import sqlite3

con = sqlite3.connect('fpl2.db')

con.row_factory = sqlite3.Row
cur = con.cursor()


# GRACZYKI

def init_gracze():
    cur.execute('DROP TABLE IF EXISTS gracze;')
    cur.execute('CREATE TABLE IF NOT EXISTS gracze (id INTEGER PRIMARY KEY, klub varchar)')
    r = requests.get('https://fantasy.premierleague.com/api/leagues-classic/7206/standings/')

    json = r.json()
    temp = pd.DataFrame(json['new_entries'])
    temp = list(temp['results'])
    ids = []
    team_names = []
    for i in range(6):
        ids.append(temp[i]['entry'])
        team_names.append(temp[i]['entry_name'])

    sql = "INSERT INTO gracze (id, klub) VALUES (?, ?)"
    val = [(str(ids[i]), str(team_names[i])) for i in range(6)]
    cur.executemany(sql, val)
    
    print("GRACZE W LIDZE:")
    cur.execute("SELECT * FROM gracze")
    rows = cur.fetchall()
    for row in rows:
        print(row[1], row[0])
        
    potw=True
    while(potw):
        potw_inp=input("Zatwierdzasz zmiany? Y/N ")
        if(potw_inp=="Y"):
            con.commit()
            print("Zmiany zatwierdzone")
            potw=False
        elif(potw_inp=="N"):
            con.rollback()
            print("Zmiany odrzucone")
            potw=False
        else:
            print("Y/N")

    


def init_pilkarzyki():
    cur.execute('DROP TABLE IF EXISTS pilkarzyki;')
    cur.execute('CREATE TABLE IF NOT EXISTS pilkarzyki (id INTEGER PRIMARY KEY,  team VARCHAR, element_type VARCHAR, '
                'event_points FLOAT, form FLOAT, web_name VARCHAR)')

    r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')

    json = r.json()
    elements_df = pd.DataFrame(json['elements'])
    elements_type = pd.DataFrame(json['element_types'])
    teams_df = pd.DataFrame(json['teams'])

    el_df = elements_df[['id', 'team', 'element_type', 'event_points', 'form', 'web_name']]
    el_df['element_type'] = el_df.element_type.map(elements_type.set_index('id').singular_name)
    el_df['team'] = el_df.team.map(teams_df.set_index('id').name)

    el_df.to_sql('pilkarzyki', con=con, if_exists='replace', index=False)

OK=True


while(OK):
    print("MAIN MENU")
    print("1. Zainicjalizuj graczy")
    print("2. Zainicjalizuj pilkarzykow")
    print("0. Wyjscie")
    wybor=input("Wybierz opcje: ")
    if(wybor=='1'):
        pok=True
        while(pok):
            potw=input("Ta funkcja nadpisuje graczy w bazie danych. Na pewno chcesz to zrobic? Y/N ")
            if(potw=="Y"):
                init_gracze()
                pok=False
            elif(potw=="N"):
                print("Baza nie zostala zaaktualizowana")
                pok=False
            else:
                print("Y/N")
    elif(wybor=='2'):
        pok=True
        while(pok):
            potw=input("Ta funkcja nadpisuje pilkarzy i ich dane w bazie danych. Na pewno chcesz to zrobic? Y/N ")
            if(potw=="Y"):
                init_pilkarzyki()
                pok=False
            elif(potw=="N"):
                print("Baza nie zostala zaaktualizowana")
                pok=False
            else:
                print("Y/N")
    elif(wybor=='0'):
        print("WYJSCIE")
        OK=False
    else:
        print("Zla opcja")