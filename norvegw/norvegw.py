import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('auto_handball.py'))))
from auto_handball import *

bet_scraping("norvegw_bet.html", "bet_daily.xlsx")

saved_results('norvegw.html', 'norvegw.xlsx')

def namechange():
    matches = pd.read_excel('norvegw.xlsx')
    matches = matches.replace('Fredrikstad N','Fredrikstad - nők', regex=True)
    matches = matches.replace('Aker N','Aker - nők', regex=True)
    matches = matches.replace('Flint N','Flint Tonsberg - nők', regex=True)
    matches = matches.replace('Molde N','Molde - nők', regex=True)
    matches = matches.replace('Byåsen N','Byasen - nők', regex=True)
    matches = matches.replace('Romerike Ravens N','Romerike Ravens - nők', regex=True)
    matches = matches.replace('Kristiansand N','Vipers Kristiansand - nők', regex=True)
    matches = matches.replace('Tertnes N','Tertnes - nők', regex=True)
    matches = matches.replace('Sola N','Sola - nők', regex=True)
    matches = matches.replace('Fana N','Fana - nők', regex=True)
    matches = matches.replace('Storhamar N','Storhamar - nők', regex=True)
    matches = matches.replace('Oppsal N','Oppsal - nők', regex=True)
    matches = matches.replace('Larvik N','Larvik - nők', regex=True)
    matches = matches.replace('Follo N','Follo HK - nők', regex=True)
    matches.to_excel("norvegw_scores.xlsx", index=False)

namechange()

ou_analization('bet_daily.xlsx', 'norvegw_scores.xlsx', 'norvegw_ou_final.xlsx', 'Norvég 1.')

half_analization('bet_daily.xlsx', 'norvegw_scores.xlsx', 'norveg_half_final.xlsx', 'Norvég női 1.')