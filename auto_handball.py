#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
from selenium import webdriver
import pandas as pd
import re
import itertools
import os
from datetime import date
import numpy as np
import statistics

def bet_scraping(betfajl, out):
    #definialunk egy bongeszot, hogy letre tudjuk hozni a kapcsolatot es a linket megadjuk
    with open(betfajl, encoding="utf-8") as f:
        data = f.read()
        bs = BeautifulSoup(data, 'html.parser')

    df = pd.DataFrame()

    name_containers = bs.findAll("div", {'class': 'src-ParticipantFixtureDetailsHigher_Team'})
    #print(name_containers)

    name = []
    for i in range(len(name_containers)):
        name.append(name_containers[i].text)
    #print(name)

    points_container = bs.findAll('span', {'class': 'src-ParticipantCenteredStacked50_Handicap'})
    points_container = points_container[int(len(points_container)/2):]
    #print(points_container)

    points = []
    for i in points_container:
        #point = i.findAll("span", {'class': 'gl-ParticipantCenteredStacked_Handicap'})
        #for j in range(len(point)):
        points.append(i.text)
            #print(points)
    for i in points:
        if i[0]=='O':
            points.remove(i)

    points = [float(x.replace('U ', '')) for x in points]

    #print(points)

    home = []
    away = []

    for i in range(0,len(name),2):
        home.append(name[i])

    for i in range(1,len(name),2):
        away.append(name[i])

    #print(away)


    df['home'] = home
    df['away'] = away
    df['pts_th'] = points
    print(df)

    df.to_excel(out, index=False)

#bet_scraping("danw/danw_bet.html", "danw/bet_daily.xlsx")

def saved_results(html, outfile):

    with open(html, encoding="utf-8") as f:
        data = f.read()
        bs = BeautifulSoup(data, 'html.parser')

        home_final = []
        away_final = []
        homesc_final = []
        awaysc_final = []
        home1 = []
        home2 = []
        away1 = []
        away2 = []

        #out_filename = outfile
        #headers = "home_team,away_team,home_score,away_score\n"

        #ha kell, ezzel ki lehet egesziteni

        #f = open(out_filename, "w+")
        #f.write(headers)

        #az egyes meccsekhez tartozó információk tagekkel együtt
        containers = bs.findAll("div", id=lambda x: x and x.startswith('g_7_'))
        #felbontogatjuk további részekre és kiszedjük a szükséges információkat
        for i in range(len(containers)):
            home = containers[i].findAll("div", {'class': re.compile(r'event__participant event__participant--home')})
            away = containers[i].findAll("div", {'class': re.compile(r'event__participant event__participant--away')})
            home_sc = containers[i].findAll("div", {'class': 'event__score event__score--home'})
            away_sc = containers[i].findAll("div", {'class': 'event__score event__score--away'})
            home_1st = containers[i].findAll("div", {'class': 'event__part event__part--home event__part--1'})
            home_2nd = containers[i].findAll("div", {'class': 'event__part event__part--home event__part--2'})
            away_1st = containers[i].findAll("div", {'class': 'event__part event__part--away event__part--1'})
            away_2nd = containers[i].findAll("div", {'class': 'event__part event__part--away event__part--2'})

            #minden kiszedett információból eltávolítjuk a tageket és csak a szöveges tartalmat tartjuk meg
            home_team = home[0].text
            away_team = away[0].text
            home_score = home_sc[0].text
            away_score = away_sc[0].text

            home_final.append(home_team)
            away_final.append(away_team)
            homesc_final.append(home_score)
            awaysc_final.append(away_score)
            home1.append(home_1st[0].text)
            home2.append(home_2nd[0].text)
            away1.append(away_1st[0].text)
            away2.append(away_2nd[0].text)
            
            #fájlba kiírjuk az eredményt
            #f.write(home_team + "," + away_team + "," + home_score + "," + away_score + "\n")
            #ha kell, akkor az alabbi sort is bele lehet rakni
            '''+ "," + home_1st + ","
                    + away_1st + "," + home_2nd + "," + away_2nd + "," + home_3rd + "," + away_3rd + ","
                    + home_4th + "," + away_4th + "," + home_ot + "," + away_ot +'''
        #f.close()
        df = pd.DataFrame()
        df['home'] = home_final
        df['away'] = away_final
        df['home_goals'] = homesc_final
        df['away_goals'] = awaysc_final
        df['home_1st'] = home1
        df['home_2nd'] = home2
        df['away_1st'] = away1
        df['away_2nd'] = away2
        #print(df)
        df.to_excel(outfile, index=False)

#saved_results('danw/danw.html', 'danw/danw.xlsx')

def namechange():
    pass
    '''matches = pd.read_excel('danw/danw.xlsx')
    matches = matches.replace('Aarhus United N','Aarhus United - nők', regex=True)
    matches = matches.replace('Odense N','HC Odense - nők', regex=True)
    matches = matches.replace('Herning-Ikast N','Herning-Ikast - nők', regex=True)
    matches = matches.replace('NFH Nyk N','Nykøbing FH - nők', regex=True)
    matches = matches.replace('Esbjerg N','Team Esbjerg - nők', regex=True)
    matches = matches.replace('Silkeborg-Voel N','Silkeborg Voel - nők', regex=True)
    matches = matches.replace('Horsens N','Horsens HK - nők', regex=True)
    matches = matches.replace('Viborg N','Viborg HK - nők', regex=True)
    matches.to_excel("danw/danw_scores.xlsx", index=False)'''

#namechange()

def ou_analization(bet, matches, outfile, comp):

    matches = pd.read_excel(matches)
    #print(matches)

    bet_df = pd.read_excel(bet)
    #print(bet_df)

    #matches = pd.read_csv()

    matches["sum_goals"] = matches.home_goals + matches.away_goals
    #print(matches)
    home = bet_df['home'].tolist()
    away = bet_df['away'].tolist()
    threshold = bet_df['pts_th'].tolist()

    home_over = []
    home_match = []
    away_over = []
    away_match = []
    hodiff = []
    hudiff = []
    aodiff = []
    audiff = []

    '''repl = 8
    home = list(itertools.chain.from_iterable(itertools.repeat(x, 2*repl+1) for x in home))
    away = list(itertools.chain.from_iterable(itertools.repeat(x, 2*repl+1) for x in away))
    threshold = [x - repl for x in threshold]
    threshold = [x+i for x in threshold for i in range(2*repl+1)]'''
    '''print(threshold)
    print(home)
    print(away)'''
    for i in range(len(home)):
        home_df = matches[(matches.home==home[i])]
        home_ov = len(home_df[home_df.sum_goals>threshold[i]])
        home_over.append(home_ov)
        home_match.append(home_df.shape[0])
        #hodiff.append(statistics.mean(home_df.sum_goals-threshold[i]))
        #home_perc.append(home_over/home_df.shape[0])*100

        #print(hodiff)
    
    '''for i in range(len(home)):
        home_df = matches[(matches.home==home[i])]
        home_ov = len(home_df[home_df.sum_goals>threshold[i]])
        hodiff.append(statistics.mean(home_df.sum_goals-threshold[i]))'''
        
    #print(home_over)
    #print(home_match)

    for i in range(len(away)):
        away_df = matches[(matches.away==away[i])]
        away_ov = len(away_df[away_df.sum_goals>threshold[i]])
        away_over.append(away_ov)
        away_match.append(away_df.shape[0])
        #aodiff.append(statistics.mean(home_df.sum_goals-threshold[i]))
        #home_perc.append(home_over/home_df.shape[0])*100

        #print(aodiff)
        
    #print(away_over)
    #print(away_match)

    df_final = pd.DataFrame()
    df_final['home'] = home
    df_final['away'] = away
    df_final['pts_th'] = threshold
    df_final['home_over'] = home_over
    df_final['home_match'] = home_match
    df_final['away_over'] = away_over
    df_final['away_match'] = away_match
    df_final['home_perc'] = df_final['home_over'] / df_final['home_match'] * 100
    df_final['away_perc'] = df_final['away_over'] / df_final['away_match'] * 100
    df_final['home_perc'] = df_final['home_perc'].apply(lambda x:round(x,2))
    df_final['away_perc'] = df_final['away_perc'].apply(lambda x:round(x,2))
    df_final.insert(0, 'comp', comp)

    #df_final['hodiff'] = mean(hodiff)
    print(df_final)
    df_final.to_excel(outfile, engine='xlsxwriter', index=False)
    '''
    today = date.today()
    d4 = today.strftime("%b-%d-%Y")
    path = "../elemzes/ou/" + d4 
    isExist = os.path.exists(path)

    if not isExist:
    
    # Create a new directory because it does not exist 
        os.makedirs(path)
        path = path + "/" + outfile
        #out_df.to_excel(path, index=False)
        with pd.ExcelWriter(path) as writer:  
            df_final.to_excel(writer, sheet_name='OU Analysis', index=False)
            #out_df.to_excel(writer, sheet_name='Thresholds', index=False)
    else:
        path = path + "/" + outfile
        #out_df.to_excel(path, index=False)
        with pd.ExcelWriter(path) as writer:  
            df_final.to_excel(writer, sheet_name='OU Analysis', index=False)
            #out_df.to_excel(writer, sheet_name='Thresholds', index=False)
'''
    '''path = "../gyujto/" + outfile
    df_final.to_excel(path, engine='xlsxwriter', index=False)'''

    '''szaz = [i for i in range(0,101)]

    #df = pd.read_excel('../elemzes/kosar_ou.xlsx')
    df = pd.read_excel('elemzes/kosar_ou.xlsx')
    df = df.loc[df.comp=='Puerto Rico']
    #print(df) 

    undern = []
    undery = []
    overn = []
    overy = []

    for i in szaz:
        df_under = df[(df.home_perc<i) & (df.away_perc<i)]
        df_over = df[(df.home_perc>i) & (df.away_perc>i)]
        #print(len(df_perc[df_perc["under"]=="y"]))
        undern.append(len(df_under[df_under["under"]=="n"]))
        undery.append(len(df_under[df_under["under"]=="y"]))
        overn.append(len(df_over[df_over["over"]=="n"]))
        overy.append(len(df_over[df_over["over"]=="y"]))
        #print(df_perc)

    #print(undern)
    out_df = pd.DataFrame()
    out_df['percentage'] = szaz
    out_df['undery'] = undery
    out_df['undern'] = undern
    out_df['underperc'] = out_df['undery'] / (out_df['undern'] + out_df['undery']) * 100
    out_df['underperc'] = out_df['underperc'].apply(lambda x:round(x,2))
    out_df['overy'] = overy
    out_df['overn'] = overn
    out_df['overperc'] = out_df['overy'] / (out_df['overn'] + out_df['overy']) * 100
    out_df['overperc'] = out_df['overperc'].apply(lambda x:round(x,2))
    print(out_df)

    df_under = pd.DataFrame()
    df_under['under'] = df_final[['home_perc','away_perc']].max(axis=1).apply(np.ceil).astype(int)
    df_under['over'] = df_final[['home_perc','away_perc']].min(axis=1).apply(np.floor).astype(int)

    new_df = pd.merge(df_under, out_df,  how='inner', left_on=['under'], right_on = ['percentage'])
    new_df2 = pd.merge(df_under, out_df,  how='inner', left_on=['over'], right_on = ['percentage'])
    
    df_final['uprob'] = new_df['underperc']
    df_final['oprob'] = new_df2['overperc']
    print(df_final)

    '''

#ou_analization('danw/bet_daily.xlsx', 'danw/danw_scores.xlsx', 'danw/danw_final.xlsx', 'Dán női 1.')

def half_analization(bet, matches, outfile, comp):
    matches = pd.read_excel(matches)
    #print(matches)

    bet_df = pd.read_excel(bet)
    #print(bet_df)

    #matches = pd.read_csv()

    matches["sum_1st"] = matches.home_1st + matches.away_1st
    matches["sum_2nd"] = matches.home_2nd + matches.away_2nd
    matches["diff"] = matches.sum_1st - matches.sum_2nd
    #print(matches)
    home = bet_df['home'].tolist()
    away = bet_df['away'].tolist()

    #print(home)
    #print(away)
    
    home1 = []
    home2 = []
    homex = []
    away1 = []
    away2 = []
    awayx = []
    hdiff = []
    adiff = []
    hszor = []
    aszor = []

    for i in range(len(home)):
        home_df = matches[(matches.home==home[i])]

        conditions = [home_df['sum_1st']>home_df['sum_2nd'], home_df['sum_1st']<home_df['sum_2nd'], \
            home_df['sum_1st']==home_df['sum_2nd']]
        choices = [1, 2, 'X']
    
        home_df["half"] = np.select(conditions, choices, default=np.nan)

        home1.append(home_df[home_df.half == '1'].shape[0])
        home2.append(home_df[home_df.half == '2'].shape[0])
        homex.append(home_df[home_df.half == 'X'].shape[0])
        hdiff.append(home_df['diff'].mean())
        hszor.append(home_df['diff'].std())

        #print(hdiff)
        #print(hszor)
        #print(home_df)
    
    hdiff = [ '%.2f' % elem for elem in hdiff ]
    hszor = [ '%.2f' % elem for elem in hszor ]
    

    for i in range(len(away)):
        away_df = matches[(matches.away==away[i])]

        conditions = [away_df['sum_1st']>away_df['sum_2nd'], away_df['sum_1st']<away_df['sum_2nd'], \
            away_df['sum_1st']==away_df['sum_2nd']]
        choices = [1, 2, 'X']
    
        away_df["half"] = np.select(conditions, choices, default=np.nan)
    
        away1.append(away_df[away_df.half == '1'].shape[0])
        away2.append(away_df[away_df.half == '2'].shape[0])
        awayx.append(away_df[away_df.half == 'X'].shape[0])
        adiff.append(away_df['diff'].mean())
        aszor.append(away_df['diff'].std())
    
    adiff = [ '%.2f' % elem for elem in adiff ]
    aszor = [ '%.2f' % elem for elem in aszor ]
    #print(adiff)

    #print(away_df)
    '''print(home1)
    print(home2)
    print(homex)
    print(away1)
    print(away2)
    print(awayx)'''
    
    df_final = pd.DataFrame()
    df_final['home'] = home
    df_final['away'] = away
    df_final['home1'] = home1
    df_final['home2'] = home2
    df_final['homex'] = homex
    df_final['away1'] = away1
    df_final['away2'] = away2
    df_final['awayx'] = awayx
    df_final['h1p'] = df_final['home1']/((df_final['home1']+df_final['home2']+df_final['homex'])) *100
    df_final['h2p'] = df_final['home2']/((df_final['home1']+df_final['home2']+df_final['homex'])) *100
    df_final['hxp'] = df_final['homex']/((df_final['home1']+df_final['home2']+df_final['homex'])) *100
    df_final['h1p'] = df_final['h1p'].apply(lambda x:round(x,2))
    df_final['h2p'] = df_final['h2p'].apply(lambda x:round(x,2))
    df_final['hxp'] = df_final['hxp'].apply(lambda x:round(x,2))
    

    df_final['a1p'] = df_final['away1']/((df_final['away1']+df_final['away2']+df_final['awayx'])) *100
    df_final['a2p'] = df_final['away2']/((df_final['away1']+df_final['away2']+df_final['awayx'])) *100
    df_final['axp'] = df_final['awayx']/((df_final['away1']+df_final['away2']+df_final['awayx'])) *100
    df_final['a1p'] = df_final['a1p'].apply(lambda x:round(x,2))
    df_final['a2p'] = df_final['a2p'].apply(lambda x:round(x,2))
    df_final['axp'] = df_final['axp'].apply(lambda x:round(x,2))

    df_final['hdiff'] = hdiff
    df_final['adiff'] = adiff
    df_final['hszor'] = hszor
    df_final['aszor'] = aszor
    
    df_final.insert(0, 'comp', comp)
    print(df_final)

    today = date.today()
    d4 = today.strftime("%b-%d-%Y")
    path = "../elemzes/half/" + d4 
    isExist = os.path.exists(path)

    if not isExist:
    
    # Create a new directory because it does not exist 
        os.makedirs(path)
        path = path + "/" + outfile
        #out_df.to_excel(path, index=False)
        with pd.ExcelWriter(path) as writer:  
            df_final.to_excel(writer, sheet_name='OU Analysis', index=False)
            #out_df.to_excel(writer, sheet_name='Thresholds', index=False)
    else:
        path = path + "/" + outfile
        #out_df.to_excel(path, index=False)
        with pd.ExcelWriter(path) as writer:  
            df_final.to_excel(writer, sheet_name='OU Analysis', index=False)
            #out_df.to_excel(writer, sheet_name='Thresholds', index=False)
    
    '''
    df_final['home_perc'] = df_final['home_over'] / df_final['home_match'] * 100
    df_final['away_perc'] = df_final['away_over'] / df_final['away_match'] * 100
    df_final['home_perc'] = df_final['home_perc'].apply(lambda x:round(x,2))
    df_final['away_perc'] = df_final['away_perc'].apply(lambda x:round(x,2))
    


    print(df_final)'''
    df_final.to_excel(outfile, engine='xlsxwriter', index=False)

#half_analization('danw/bet_daily.xlsx', 'danw/danw_scores.xlsx', 'danw/danw_half_final.xlsx', 'Dán női 1.')