import requests
import pandas as pd
import numpy as np
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt


sns.set()

con = sqlite3.connect('fpl2.db')

con.row_factory = sqlite3.Row
cur = con.cursor()


def init_db():
    cur.execute('DROP TABLE IF EXISTS all_picks;')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS all_picks(gw INTEGER, id INTEGER, element VARCHAR, points FLOAT, element_type VARCHAR, multiplier INTEGER, name VARCHAR, team VARCHAR, team_name VARCHAR, event_points VARCHAR, xPTS FLOAT, xPLC FLOAT, form FLOAT)')

    con.commit()

    cur.execute('DROP TABLE IF EXISTS picked;')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS picked(gw INTEGER, element VARCHAR, points FLOAT, element_type VARCHAR, multiplier INTEGER, name VARCHAR, team VARCHAR, team_name VARCHAR)')

    con.commit()

    cur.execute('DROP TABLE IF EXISTS captains;')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS captains(gw INTEGER, element VARCHAR, element_type VARCHAR, points FLOAT, name VARCHAR, team VARCHAR, team_name VARCHAR)')

    con.commit()

    cur.execute('DROP TABLE IF EXISTS v_captains;')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS v_captains(gw INTEGER, element VARCHAR, element_type VARCHAR, name VARCHAR, points FLOAT, team VARCHAR, team_name VARCHAR)')

    con.commit()

    cur.execute('DROP TABLE IF EXISTS bench;')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS bench(gw INTEGER, element VARCHAR, element_type VARCHAR, name VARCHAR, event_points FLOAT, team VARCHAR, team_name VARCHAR)')

    con.commit()

    cur.execute('DROP TABLE IF EXISTS plot;')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS plot(gw INTEGER, name VARCHAR, team_name VARCHAR, All INTEGER, Next INTEGER, Leader INTEGER, transfers INTEGER, Capt INTEGER, Vcapt INTEGER, Bench INTEGER, value FLOAT, Place INTEGER)')

    con.commit()

    cur.execute('DROP TABLE IF EXISTS stat;')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS stat(name VARCHAR, team_name VARCHAR, All INTEGER, Next INTEGER, Leader INTEGER, transfers INTEGER, Capt INTEGER, Vcapt INTEGER, Bench INTEGER, value FLOAT, Place INTEGER)')

    con.commit()

    cur.execute('DROP TABLE IF EXISTS transfers;')
    cur.execute('CREATE TABLE IF NOT EXISTS transfers(gw INTEGER, name VARCHAR, team_name VARCHAR, transfers INTEGER)')

    con.commit()

    cur.execute('DROP TABLE IF EXISTS value;')
    cur.execute('CREATE TABLE IF NOT EXISTS value(name VARCHAR, team_name VARCHAR, value FLOAT)')

    con.commit()


def init_gracze():
    cur.execute('DROP TABLE IF EXISTS gracze;')
    cur.execute('CREATE TABLE IF NOT EXISTS gracze (id INTEGER PRIMARY KEY, klub varchar, nazwa varchar)')
    r = requests.get('https://fantasy.premierleague.com/api/leagues-classic/7206/standings/')

    json = r.json()
    print(json.keys())
    temp = pd.DataFrame(json['standings'])
    temp = list(temp['results'])
    ids = []
    team_names = []
    names = []
    for i in range(len(temp)):
        ids.append(temp[i]['entry'])
        team_names.append(temp[i]['entry_name'])
        names.append(temp[i]['player_name'])

    sql = "INSERT INTO gracze (id, klub,nazwa) VALUES (?, ?,?)"
    val = [(str(ids[i]), str(team_names[i]), str(names[i])) for i in range(len(temp))]
    cur.executemany(sql, val)

    potw = True
    while potw:
        potw_inp = input("Zatwierdzasz zmiany? Y/N ")
        if potw_inp == "Y":
            con.commit()
            print("Zmiany zatwierdzone")
            potw = False
        elif potw_inp == "N":
            con.rollback()
            print("Zmiany odrzucone")
            potw = False
        else:
            print("Y/N")

    print("MANAGERS IN THE LEAGUE:")
    cur.execute("SELECT * FROM gracze")
    rows = cur.fetchall()
    for row in rows:
        print(row[1], row[0])


def init_pilkarzyki(GW):
    r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')

    json = r.json()
    elements_df = pd.DataFrame(json['elements'])
    elements_type = pd.DataFrame(json['element_types'])
    teams_df = pd.DataFrame(json['teams'])

    el_df = elements_df[['id', 'web_name', 'team', 'element_type', 'event_points', 'form', 'now_cost']]
    el_df['now_cost'] = el_df['now_cost'] / 10
    el_df['element_type'] = el_df.element_type.map(elements_type.set_index('id').singular_name)
    el_df['team'] = el_df.team.map(teams_df.set_index('id').name)

    el_df['gw'] = GW
    el_df['xPTS'] = elements_df['ep_this']

    el_df.to_sql('pilkarzyki', con=con, if_exists='append', index=False)
    chk = pd.read_sql("SELECT * FROM pilkarzyki", con)
    print(chk)
    potw = True
    while potw:
        potw_inp = input("Do you accept changes? Y/N ")
        if potw_inp == "Y":
            print("Changes accepted")
            potw = False
        elif potw_inp == "N":
            cur.execute("DELETE FROM pilkarzyki WHERE gw = ?", (GW))
            print("Changes rejected")
            potw = False
        else:
            print("Y/N")


def show_pilkarzyki(GW):
    sh = pd.read_sql("SELECT * FROM pilkarzyki WHERE gw = " + str(GW), con)
    with pd.option_context('display.max_rows', 50, 'display.max_columns', 10):
        print(sh)


def show_picks():
    picks_df = pd.read_sql("SELECT * FROM picked", con)
    cap_df = pd.read_sql("SELECT * FROM captains", con)
    vcap_df = pd.read_sql("SELECT * FROM v_captains", con)
    bench_df = pd.read_sql("SELECT * FROM bench", con)
    value_df = pd.read_sql("SELECT * FROM value", con)
    transfers_df = pd.read_sql("SELECT * FROM transfers", con)
    with pd.option_context('display.max_rows', 50, 'display.max_columns', 10):
        print(picks_df)
    with pd.option_context('display.max_rows', 50, 'display.max_columns', 10):
        print(cap_df)
    with pd.option_context('display.max_rows', 50, 'display.max_columns', 10):
        print(vcap_df)
    with pd.option_context('display.max_rows', 50, 'display.max_columns', 10):
        print(bench_df)
    with pd.option_context('display.max_rows', 50, 'display.max_columns', 10):
        print(value_df)
    with pd.option_context('display.max_rows', 50, 'display.max_columns', 10):
        print(transfers_df)


def overwrite_pilkarzyki(GW):
    r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
    json = r.json()
    elements_df = pd.DataFrame(json['elements'])
    elements_type = pd.DataFrame(json['element_types'])
    teams_df = pd.DataFrame(json['teams'])
    el_df = elements_df[['id', 'web_name', 'team', 'element_type', 'event_points', 'form', 'now_cost']]
    el_df['now_cost'] = el_df['now_cost'] / 10
    el_df['element_type'] = el_df.element_type.map(elements_type.set_index('id').singular_name)
    el_df['team'] = el_df.team.map(teams_df.set_index('id').name)
    el_df['gw'] = GW
    el_df['xPTS'] = elements_df['ep_next']
    cur.execute("DELETE FROM pilkarzyki WHERE gw = " + str(GW))
    con.commit()
    el_df.to_sql('pilkarzyki', con=con, if_exists='append', index=False)


def init_picks(GW):
    gracze = pd.read_sql("SELECT * FROM gracze", con)
    el_df = pd.read_sql("SELECT * FROM pilkarzyki WHERE gw = " + str(GW), con)
    all_picks_df = pd.DataFrame()
    picks_df = pd.DataFrame()
    cap_df = pd.DataFrame()
    vcap_df = pd.DataFrame()
    bench_df = pd.DataFrame()
    info_df = pd.DataFrame()

    for i in range(len(gracze['id'])):
        print('Now processing ' + str(gracze['nazwa'][i]))
        r = requests.get(
            'https://fantasy.premierleague.com/api/entry/' + str(gracze['id'][i]) + '/event/' + str(GW) + '/picks/')
        json = r.json()
        temp = pd.DataFrame(json['picks'])
        temp = pd.merge(left=temp, right=el_df, left_on='element', right_on='id')
        temp['element'] = temp.element.map(el_df.set_index('id').web_name)
        temp['name'] = gracze['nazwa'][i]
        temp['team_name'] = gracze['klub'][i]
        temp['gw'] = GW

        # DO ZMIANY
        temp['xPLC'] = 0
        temp['points'] = temp['multiplier'] * temp['event_points']
        temp['transfers'] = json['entry_history']['event_transfers_cost']
        temp['value'] = json['entry_history']['value'] / 10
        all_picks_df = all_picks_df.append(temp[['gw', 'id', 'element', 'event_points', 'element_type', 'team',
                                                 'multiplier', 'name', 'points', 'team_name', 'xPTS', 'xPLC','form']],
                                           ignore_index=True)
        picks_df = picks_df.append(temp.loc[temp['multiplier'] != 0], ignore_index=True)
        cap_df = cap_df.append(temp.loc[temp['is_captain'] == True], ignore_index=True)
        vcap_df = vcap_df.append(temp.loc[temp['is_vice_captain'] == True], ignore_index=True)
        bench_df = bench_df.append(temp.loc[temp['multiplier'] == 0], ignore_index=True)
        if json['active_chip']=='bboost':
            temp['gw']=temp['gw']
            temp['element']=json['active_chip']
            temp['event_points']=0
            temp['element_type']=json['active_chip']
            temp['name'] = temp['name']
            temp['team'] = json['active_chip']
            temp['team_name'] = temp['team_name']
            bench_df = bench_df.append(temp, ignore_index = True)
        info_df = info_df.append(temp)

    picks_df = picks_df[['gw', 'element', 'points', 'element_type', 'multiplier', 'name', 'team', 'team_name']]
    cap_df = cap_df[['gw', 'element', 'points', 'element_type', 'name', 'team', 'team_name']]
    vcap_df = vcap_df[['gw', 'element', 'points', 'element_type', 'name', 'team', 'team_name']]
    bench_df = bench_df[['gw', 'element', 'event_points', 'element_type', 'name', 'team', 'team_name']]
    infov_df = info_df[['gw', 'name', 'team_name', 'value']]
    infot_df = info_df[['gw', 'name', 'team_name', 'transfers']]

    tablet = pd.pivot_table(infot_df, values=['transfers'], index=['name', 'team_name'])
    tablet['gw'] = GW
    tablev = pd.pivot_table(infov_df, values=['value'], index=['name', 'team_name'])

    cur.execute("DELETE FROM all_picks WHERE gw = ?", (GW,))
    con.commit()
    all_picks_df.to_sql('all_picks', con=con, if_exists='append', index=False)
    
    cur.execute("DELETE FROM picked WHERE gw = ?", (GW,))
    con.commit()
    picks_df.to_sql('picked', con=con, if_exists='append', index=False)
    
    cur.execute("DELETE FROM captains WHERE gw = ?", (GW,))
    con.commit()
    cap_df.to_sql('captains', con=con, if_exists='append', index=False)


    cur.execute("DELETE FROM v_captains WHERE gw = ?", (GW,))
    con.commit()
    vcap_df.to_sql('v_captains', con=con, if_exists='append', index=False)

    cur.execute("DELETE FROM bench WHERE gw = ?", (GW,))
    bench_df.to_sql('bench', con=con, if_exists='append', index=False)
    con.commit()

    cur.execute("DELETE FROM transfers WHERE gw = " + str(GW,))
    tablet.to_sql('transfers', con=con, if_exists='append')
    con.commit()

    cur.execute("DELETE FROM value")
    tablev.to_sql('value', con=con, if_exists='replace')
    con.commit()


def init_stat():
    picks_df = pd.read_sql("SELECT * FROM picked", con)
    cap_df = pd.read_sql("SELECT * FROM captains", con)
    vcap_df = pd.read_sql("SELECT * FROM v_captains", con)
    bench_df = pd.read_sql("SELECT * FROM bench", con)
    value_df = pd.read_sql("SELECT * FROM value", con)
    transfers_df = pd.read_sql("SELECT name, team_name, transfers FROM transfers", con)
    table = pd.pivot_table(picks_df, values='points', index=['name', 'team_name'], aggfunc=np.sum).sort_values(
        by='points', ascending=False)
    tablec = pd.pivot_table(cap_df, values='points', index=['name', 'team_name'], aggfunc=np.sum).sort_values(
        by='points', ascending=False)
    tablev = pd.pivot_table(vcap_df, values='points', index=['name', 'team_name'], aggfunc=np.sum).sort_values(
        by='points', ascending=False)
    tableb = pd.pivot_table(bench_df, values='event_points', index=['name', 'team_name'], aggfunc=np.sum).sort_values(
        by='event_points', ascending=False)
    tablet = pd.pivot_table(transfers_df, values='transfers', index=['name', 'team_name'], aggfunc=np.sum)
    stat = pd.merge(left=table, right=tablec, left_on=['name', 'team_name'], right_on=['name', 'team_name'])
    stat = stat.rename(columns={'points_x': 'All'})
    stat = stat.rename(columns={'points_y': 'Capt'})
    stat = pd.merge(left=stat, right=tablev, left_on=['name', 'team_name'], right_on=['name', 'team_name'])
    stat = stat.rename(columns={'points': 'Vcapt'})
    stat = pd.merge(left=stat, right=tableb, left_on=['name', 'team_name'], right_on=['name', 'team_name'])
    stat = stat.rename(columns={'event_points': 'Bench'})
    stat = pd.merge(left=stat, right=tablet, left_on=['name', 'team_name'], right_on=['name', 'team_name'])
    stat = stat.rename(columns={'transfers': 'Transfers'})
    stat['All']=stat['All']-stat['Transfers']
    stat=stat.sort_values(by = 'All', ascending = False)
    stat = pd.merge(left=stat, right=abs(stat['All'].diff()), left_on=['name', 'team_name'],
                    right_on=['name', 'team_name'])
    stat = stat.rename(columns={'All_y': 'Next'})
    stat = stat.rename(columns={'All_x': 'All'})
    stat = pd.merge(left=stat, right=abs(stat['All'] - stat['All'].iloc[0]), left_on=['name', 'team_name'],
                    right_on=['name', 'team_name'])
    stat = stat.rename(columns={'All_y': 'Leader'})
    stat = stat.rename(columns={'All_x': 'All'})
    stat.fillna(0)
    stat['Next'] = stat['Next'].fillna(0).astype(int)
    stat = pd.merge(left=stat, right=value_df[['name', 'team_name', 'value']], left_on=['name', 'team_name'],
                    right_on=['name', 'team_name'])
    stat = stat.rename(columns={'value': 'Value'})

    stat['Place'] = stat['All'].rank(method='min', ascending=False).fillna(0).astype(int)
    stat.to_sql('stat', con=con, if_exists='replace')
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(stat)
    stat.to_excel('stat.xlsx')


def init_transfers(GW):
    tran_df = pd.DataFrame()
    el_df = pd.read_sql("SELECT id,web_name FROM pilkarzyki WHERE gw = " + str(GW), con)
    gracze = pd.read_sql("SELECT * FROM gracze", con)
    for i in range(len(gracze['id'])):
        r = requests.get('https://fantasy.premierleague.com/api/entry/' + str(gracze['id'][i]) + '/transfers/')
        json = r.json()
        if len(json) != 0:
            temp = pd.DataFrame(json)[['element_in', 'element_out', 'event']]
            temp = temp[temp['event'] == GW]
            temp['manager'] = gracze['nazwa'][i]
            temp['element_in'] = temp.element_in.map(el_df.set_index('id').web_name)
            temp['element_out'] = temp.element_out.map(el_df.set_index('id').web_name)
            tran_df = tran_df.append(temp, ignore_index=True)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(tran_df)
    print("NAJCZESCIEJ OUT:")
    print(tran_df.groupby('element_out').size())
    print("NAJCZESCIEJ IN:")
    print(tran_df.groupby('element_in').size())


def init_gw_stat(GW):
    picks_df = pd.read_sql("SELECT * FROM picked WHERE gw = " + str(GW), con)
    cap_df = pd.read_sql("SELECT * FROM captains WHERE gw = " + str(GW), con)
    vcap_df = pd.read_sql("SELECT * FROM v_captains WHERE gw = " + str(GW), con)
    bench_df = pd.read_sql("SELECT * FROM bench WHERE gw = " + str(GW), con)
    value_df = pd.read_sql("SELECT * FROM value", con)
    transfers_df = pd.read_sql("SELECT * FROM transfers WHERE gw = " + str(GW), con)
    table = pd.pivot_table(picks_df, values='points', index=['name', 'team_name'], aggfunc=np.sum).sort_values(
        by='points', ascending=False)
    tablec = pd.pivot_table(cap_df, values='points', index=['name', 'team_name'], aggfunc=np.sum).sort_values(
        by='points', ascending=False)
    tablev = pd.pivot_table(vcap_df, values='points', index=['name', 'team_name'], aggfunc=np.sum).sort_values(
        by='points', ascending=False)
    tableb = pd.pivot_table(bench_df, values='event_points', index=['name', 'team_name'], aggfunc=np.sum).sort_values(
        by='event_points', ascending=False)
    tablet = pd.pivot_table(transfers_df, values='transfers', index=['name', 'team_name'], aggfunc=np.sum)
    stat = pd.merge(left=table, right=tablec, left_on=['name', 'team_name'], right_on=['name', 'team_name'])
    stat = stat.rename(columns={'points_x': 'AllP'})
    stat = stat.rename(columns={'points_y': 'Capt'})
    stat = pd.merge(left=stat, right=tablev, left_on=['name', 'team_name'], right_on=['name', 'team_name'])
    stat = stat.rename(columns={'points': 'Vcapt'})
    stat = pd.merge(left=stat, right=tableb, left_on=['name', 'team_name'], right_on=['name', 'team_name'])
    stat = stat.rename(columns={'event_points': 'Bench'})
    stat = pd.merge(left=stat, right=tablet, left_on=['name', 'team_name'], right_on=['name', 'team_name'])
    stat = stat.rename(columns={'transfers': 'Transfers'})
    stat['AllP']=stat['AllP']-stat['Transfers']    
    stat = pd.merge(left=stat, right=abs(stat['AllP'].diff()), left_on=['name', 'team_name'],
                    right_on=['name', 'team_name'])
    stat = stat.rename(columns={'AllP_y': 'Next'})
    stat = stat.rename(columns={'AllP_x': 'AllP'})
    stat = pd.merge(left=stat, right=abs(stat['AllP'] - stat['AllP'].iloc[0]), left_on=['name', 'team_name'],
                    right_on=['name', 'team_name'])
    stat = stat.rename(columns={'AllP_y': 'Leader'})
    stat = stat.rename(columns={'AllP_x': 'AllP'})
    stat.fillna(0)
    stat['Next'] = stat['Next'].fillna(0).astype(int)
    stat = pd.merge(left=stat, right=value_df[['name', 'team_name', 'value']], left_on=['name', 'team_name'],
                    right_on=['name', 'team_name'])
    stat = stat.rename(columns={'value': 'Value'})
    stat['Place'] = stat['AllP'].rank(method='min', ascending=False).fillna(0).astype(int)
    stat['GW'] = GW
    stat=stat.sort_values(by = 'AllP', ascending = False)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(stat)
    cur.execute("DELETE FROM plot WHERE gw = " + str(GW))
    con.commit()
    pok = True
    while pok:
        potw = input("Zaktualizowac? Y/N ")
        if potw == "Y":
            stat.to_sql('plot', con=con, if_exists='append', index=False)
            print("Baza zostala zaaktualizowana")
            pok = False
        elif potw == "N":
            print("Baza nie zostala zaaktualizowana")
            pok = False
        else:
            print("Y/N")
    save = input("Zapisac do csv? Y/N ")
    ok = True
    while ok:
        if save == 'Y':
            stat.to_csv('stat_gw.csv', mode='a', index=False, encoding='utf-8-sig')
            ok = False
        elif save == 'N':
            ok = False
        else:
            print("Y/N")

def init_pred(GW):
    xpts=pd.DataFrame()
    from sklearn import linear_model
    gracze = pd.read_sql("SELECT * FROM gracze", con)
    for i in range(len(gracze['id'])):
        stat=pd.read_sql('SELECT gw, name, team_name, AllP FROM plot', con)
        data=stat[stat['name']==gracze['nazwa'][i]]
        x=data.reset_index().iloc[:,1].values.reshape(-1,1)
        y=data.reset_index().iloc[:,4].cumsum().values.reshape(-1,1)
        lm = linear_model.LinearRegression()
        lm.fit(x,y)
        xpred = np.arange(GW,GW+1).reshape(-1,1)
        ypred = lm.predict(xpred).item()
        temp=pd.DataFrame([[gracze['nazwa'][i],(round(ypred,0)-y[GW-2]).item()]],columns=['gracz','reg'])
        xpts=xpts.append(temp, ignore_index=True)
    all_picks=pd.read_sql("SELECT gw,id,element,points,form,name,xPTS FROM all_picks WHERE gw="+str(GW), con)
    stat=pd.pivot_table(all_picks, values=['form','xPTS'], index=['name'],aggfunc={'form':np.sum,'xPTS':np.sum})
    stat = pd.merge(left=stat, right=xpts, left_on=['name'], right_on=['gracz'])
    cols=['gracz','reg','form','xPTS']
    stat=stat.reindex(columns=cols)
    col = stat.loc[: , "reg":"xPTS"]
    stat['mean'] = round(col.mean(axis=1),0)
    print(stat)
    
def show_plots(GW):
    stat = pd.read_sql('SELECT gw, name, team_name, AllP FROM plot', con)
    gracze = pd.read_sql("SELECT * FROM gracze", con)
    temp=pd.pivot_table(stat,values='AllP',index='gw',columns='team_name',aggfunc=np.sum)
    points=temp.cumsum()
    points.plot(figsize=(20,20)).tick_params(axis='both', which='major', labelsize=20)
    plt.locator_params(nbins=GW)
    plt.show()
    plc=pd.DataFrame(index=gracze['klub'])
    for i in range(len(points)):
        plc[str(i)]=points.iloc[i].rank(ascending=False,method='max')
    plc.T.plot(figsize=(20,20)).set_ylim(17, 0)
    plt.show()

def show_means():
    count = pd.read_sql("SELECT element, count(*) as ile FROM picked GROUP BY element ORDER BY ile desc", con)
    sm = pd.read_sql("SELECT element, sum(points) as suma FROM picked GROUP BY element ORDER BY suma desc", con)
    mu = pd.merge(left=count,right=sm,left_on=['element'],right_on=['element'])
    mu['sr']=mu['suma']/mu['ile']
    mu = mu[['element','sr']]
    mu = mu.sort_values(by='sr', ascending = False)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(mu)
        
    count = pd.read_sql("SELECT team, count(*) as ile FROM picked GROUP BY team ORDER BY ile desc", con)
    sm = pd.read_sql("SELECT team, sum(points) as suma FROM picked GROUP BY team ORDER BY suma desc", con)
    mu = pd.merge(left=count,right=sm,left_on=['team'],right_on=['team'])
    mu['sr']=mu['suma']/mu['ile']
    mu = mu[['team','sr']]
    mu = mu.sort_values(by='sr', ascending = False)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(mu)
        
    count = pd.read_sql("SELECT element_type, count(*) as ile FROM picked GROUP BY element_type ORDER BY ile desc", con)
    sm = pd.read_sql("SELECT element_type, sum(points) as suma FROM picked GROUP BY element_type ORDER BY suma desc", con)
    mu = pd.merge(left=count,right=sm,left_on=['element_type'],right_on=['element_type'])
    mu['sr']=mu['suma']/mu['ile']
    mu = mu[['element_type','sr']]
    mu = mu.sort_values(by='sr', ascending = False)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(mu)

OK = True

while OK:
    print("MAIN MENU")
    print("1. Start of the gameweek procedure")
    print("2. End of the gameweek procedure")
    print("3. Export data")
    print("4. Show count of picked players (overall and GW)")
    print("5. Show all-season statistics")
    print("6. Show GW statistics")
    print("7. Show point means")    
    print("8. Show transfers")
    print("9. Search for a player")
    print("10. Show captains")
    print("11. Show plots")
    print("12. Show predictions (WIP)")
    print("13. Initialise picks") 
    print("14. Overwrite players")
    print("15. Show picks database")
    print("16. Show players database")
    print("17. Initialise players")
    print("18. Update managers")
    print("19. Initialise databases")
    print("0. Exit")
    wybor = input("Pick a number: ")

    if wybor == '1':
        GW = input("Pick GW: ")
        init_pilkarzyki(GW)
        init_picks(GW)
        cap_df = pd.read_sql("SELECT element, name FROM captains WHERE gw = " + str(GW), con)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(cap_df)   
        
    elif wybor == '2':
        GW = input("Pick GW: ")
        overwrite_pilkarzyki(GW)
        init_picks(GW)
    
    elif wybor == '3':
        wr = pd.read_sql("SELECT * FROM picked", con)
        save = input("Save to CSV file? Y/N ")
        ok = True
        while ok:
            if save == 'Y':
                wr.to_csv('gracz.csv', index=False, encoding='utf-8-sig')
                ok = False
            elif save == 'N':
                ok = False
            else:
                print("Y/N")
                
        wr = pd.read_sql("SELECT * FROM captains", con)
        save = input("Save to CSV file? Y/N ")
        ok = True
        while ok:
            if save == 'Y':
                wr.to_csv('kapitanowie.csv', index=False, encoding='utf-8-sig')
                ok = False
            elif save == 'N':
                ok = False
            else:
                print("Y/N")
            
    elif wybor == '4':
        GW = input("Pick GW: ")
        picks_df = pd.read_sql("SELECT * FROM picked WHERE gw = " + str(GW), con)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(picks_df['element'].value_counts())
        
        sh = pd.read_sql("SELECT element, count(*) as ile FROM picked GROUP BY element ORDER BY ile desc", con)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(sh)
        sh = pd.read_sql("SELECT team, count(*) as ile FROM picked GROUP BY team ORDER BY ile desc", con)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(sh)
        

    elif wybor == '5':
        init_stat()

    elif wybor == '6':
        GW = input("Pick GW: ")
        init_gw_stat(GW)

    elif wybor == '7':
        show_means()

    elif wybor == '8':
        GW = int(input("Pick GW: "))
        init_transfers(GW)

    elif wybor == '9':
        GW = input("Pick GW: ")
        all_picks_df = pd.read_sql("SELECT element, name FROM all_picks WHERE gw = " + str(GW), con)
        szuk = input("WHO ARE YOU LOOKING FOR? ")
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(all_picks_df[(all_picks_df['element'] == str(szuk))])

    elif wybor == '10':
        GW = input("Pick GW: ")
        cap_df = pd.read_sql("SELECT element, name FROM captains WHERE gw = " + str(GW), con)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(cap_df)

    elif wybor == '11':
        GW = int(input("Pick GW: "))
        show_plots(GW)   

    elif wybor == '12':
        GW = int(input("Pick GW: "))
        init_pred(GW)

    elif wybor == '13':
        GW = input("Pick GW: ")
        init_picks(GW)

    elif wybor == '14':
        GW = input("Pick GW: ")
        overwrite_pilkarzyki(GW)
        show_pilkarzyki(GW)

    elif wybor == '15':
        show_picks()
            
    elif wybor == '16':
        GW = input("Pick GW: ")
        show_pilkarzyki(GW)
    
    elif wybor == '17':
        pok = True
        GW = input("Pick GW: ")
        while pok:
            potw = input("This function overwrites players info in database. Do you want to continue? Y/N ")
            if potw == "Y":
                init_pilkarzyki(GW)
                pok = False
            elif potw == "N":
                print("Database not updated")
                pok = False
            else:
                print("Y/N")

    elif wybor == '18':
        pok = True
        while pok:
            potw = input("This function overwrites manager info in database. Do you want to continue? Y/N ")
            if potw == "Y":
                init_gracze()
                pok = False
            elif potw == "N":
                print("Database not updated")
                pok = False
            else:
                print("Y/N")
    
    elif wybor == '19':
        pok = True
        while pok:
            potw = input("This function overwrites databases. Do you want to continue? Y/N (NOT RECOMMENDED)")
            if potw == "Y":
                init_db()
                pok = False
            elif potw == "N":
                print("Databeses not updated")
                pok = False
            else:
                print("Y/N")

    #elif wybor == 'D':
        #cur.execute('DROP TABLE IF EXISTS all_picks;')
        #cur.execute(
            #'CREATE TABLE IF NOT EXISTS all_picks(gw INTEGER, id INTEGER, element VARCHAR, points FLOAT, element_type VARCHAR, multiplier INTEGER, name VARCHAR, team VARCHAR, team_name VARCHAR, event_points VARCHAR, xPTS FLOAT, xPLC FLOAT, form FLOAT)')

        #con.commit()

    elif wybor == '0':
        print("EXIT")
        OK = False
        
    else:
        print("Wrong number")
    
