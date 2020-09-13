#Below package needed to access Google Sheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def read_gsheet_to_sent_ticket():
    scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheetRegisteredUser = client.open("List of registered user").sheet1
    RegisteredUsers_FullNames = sheetRegisteredUser.col_values(2)
    RegisteredUsers_Emails = sheetRegisteredUser.col_values(5)
    RegisteredUsers_Codes = sheetRegisteredUser.col_values(7)
    RegisteredUsers_Paid = sheetRegisteredUser.col_values(9)
    RegisteredUsers_SentTicket = sheetRegisteredUser.col_values(10)
    print(len(sheetRegisteredUser.col_values(2)))
    

    for i in range(1,10) : 
        user_info = sheetRegisteredUser.row_values(i)
        print(user_info) 

    # lst = []
    # i = 1
    # try:
    #     for RegisteredUsers_FullName in RegisteredUsers_FullNames:
    #         sEmail = RegisteredUsers_Emails[i]
    #         sCode = RegisteredUsers_Codes[i]
    #         sPaid = RegisteredUsers_Paid[i]
    #         sSentTicket = RegisteredUsers_SentTicket[i]
    #         i = i + 1
    #         lst.append([sCode, sEmail, RegisteredUsers_FullName, sPaid, sSentTicket])
    # except Exception as e:
    #     print(e)
    # finally:
    #     return lst          # lst consist of users have all fields filled.

# use creds to create a client to interact with the Google Drive API


def read(): # list user to send - pail = YES and send_ticket = NO
    scope = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
        ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheetRegisteredUser = client.open("List of registered user").sheet1


    lst = []
    # for i in range(1,10) : 
    n=2
    while n < 168 : 
        # user_info = sheetRegisteredUser.row_values(n)
        # print(user_info) 
        # n+=1 
        user_info = sheetRegisteredUser.row_values(n)
        RegisteredUsers_Paid = user_info[8]
        RegisteredUsers_SentTicket = user_info[9] 
        # print(RegisteredUsers_Paid, RegisteredUsers_SentTicket)
        if RegisteredUsers_Paid == "Y" and  RegisteredUsers_SentTicket == "N" and len(user_info) == 10 : 
            RegisteredUsers_FullNames = user_info[1]
            RegisteredUsers_Emails = user_info[4]
            RegisteredUsers_Codes = user_info[5]  
            RegisteredUsers_Full_Codes = user_info[6]
            print(RegisteredUsers_Codes + " --- " + RegisteredUsers_Emails + " --- " + RegisteredUsers_FullNames + " --- " + RegisteredUsers_Full_Codes)
            # lst.append([RegisteredUsers_Codes, RegisteredUsers_Emails, RegisteredUsers_FullNames, RegisteredUsers_Full_Codes])
        n +=1 

MagicList = read()

# print(MagicList)