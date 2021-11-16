import sys

sys.path.insert(0, r"C:\Users\SafarPeter\.vscode\projects\handball")
from auto_handball import *

bet_scraping("dan_bet.html", "bet_daily.xlsx")

url = 'https://www.eredmenyek.com/kezilabda/dania/herre-handbold-ligaen/eredmenyek/'

saved_results(url, 'dan.xlsx')

def namechange():
    matches = pd.read_excel('dan.xlsx')
    matches = matches.replace('Ringsted','TMS Ringsted', regex=True)
    matches = matches.replace('Ribe-Esbjerg','Ribe Esbjerg HH', regex=True)
    matches = matches.replace('Holstebro','Team Tvis Holstebro', regex=True)
    matches = matches.replace('Kolding','KIF Kolding', regex=True)
    matches = matches.replace('Sønderjyske','SønderjyskE', regex=True)
    matches = matches.replace('Skive','Skive FH', regex=True)
    matches = matches.replace('Lemvig','Lemvig-Thyborøn', regex=True)
    matches = matches.replace('Mors','Mors Thy Håndbold', regex=True)
    matches = matches.replace('Nordsjælland','Nordsjælland Håndbold', regex=True)
    matches = matches.replace('Bjerringbro/Silkeborg','Bjerringbro-Silkeborg', regex=True)
    matches = matches.replace('Skanderborg Aarhus','Skanderborg Håndbold', regex=True)
    matches = matches.replace('Skjern','Skjern Håndbold', regex=True)
    matches = matches.replace('Aalborg','Aalborg Håndbold', regex=True)
    matches = matches.replace('Fredericia','Fredericia HK', regex=True)
    matches.to_excel("dan_scores.xlsx", index=False)

namechange()

ou_analization('bet_daily.xlsx', 'dan_scores.xlsx', 'dan_ou_final.xlsx', 'Dán 1.')

half_analization('bet_daily.xlsx', 'dan_scores.xlsx', 'dan_half_final.xlsx', 'Dán 1.')