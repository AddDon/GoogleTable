import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet():
    def __init__(self):
        scope = ['https://www.googleapis.com/auth/drive']

        creds = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)
        client = gspread.authorize(creds)

        sheet = client.open('SheetsTest')
        self.contacts = sheet.worksheet('Contacts')

    def getRowLength(self):
        return len(self.contacts.get_all_values()[0])


    def sendData(self, item):
    
        id_num = self.getRowLength()
        list = [id_num]
        list.extend(item)
        print(list)
        for i in range(len(list)):
            if '.' in str(list[i]):
                list[i] = float(list[i])
            else:
                list[i] = int(list[i])
        print(list)
        list1 = []
        list1.append(list)
        list1.append([])
        print(list1)
        self.contacts.insert_cols(list1, id_num + 1)
