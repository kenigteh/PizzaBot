import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

def pretty(sheet):
    data = sheet.get_all_values()
    keys = data[0]
    result = []
    for row in data[1:]:
        a = {}
        for i in range(len(keys)):
            a.update({keys[i]: row[i]})
        result.append(a.copy())
        a.clear()
    return result

def get_food():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_server.json', scope)
    client = gspread.authorize(creds)

    count = len(client.open('pizza_bot').worksheets())
    print(count)
    sheets = {}
    for i in range(0, count):
        sheet = client.open('pizza_bot').get_worksheet(i)
        name = sheet.title
        sheets.update({name: pretty(sheet)})

    #all shenanigans below

    return sheets