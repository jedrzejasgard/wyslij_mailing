import zeep
import json
import base64
from os import listdir
from os.path import isfile, join
import collections
import datetime
import re



def show_all_grups():
    client = zeep.Client('https://redlink.pl/ws/v1/Soap/Contacts/Groups.asmx?WSDL')
    response = client.service.GetAllGroups(strUserName='asgard', strPassword='$12345Asgard')
    r_json = zeep.helpers.serialize_object(response)
    return r_json['DataArray']['GroupData']

#lista_jezykow = ['PL','EN','DE','FR']
lista_jezykow = ['DE']

def wyslij_mailing(nazwa_mailingu, temat, imie_nazwisko, mail_wysylki,content_mailingu, data_wyslania):
    mail = zeep.Client("https://redlink.pl/ws/v1/Soap/MailCampaigns/MailCampaigns.asmx?WSDL")
    data = {}
    data['Name'] = nazwa_mailingu
    data['Subject'] = temat
    data['FromName'] = imie_nazwisko
    data['FromAddress'] = mail_wysylki
    data['HtmlFromWebSiteUrl'] = content_mailingu
    data['GroupId'] = '66F3AE43-6DDC-475E-8DB6-6775EBF9030D'
    data['ScheduleTime'] = data_wyslania
    data['TrackLinks'] = True
    response =  mail.service.CreateMailCampaign(strUserName='asgard', strPassword='$12345Asgard', data = data)
    r_json = zeep.helpers.serialize_object(response)
    print(r_json)

def wyslij_test(nazwa_mailingu, temat, imie_nazwisko, mail_wysylki,content_mailingu, data_wyslania):
    mail = zeep.Client("https://redlink.pl/ws/v1/Soap/MailCampaigns/MailCampaigns.asmx?WSDL")
    data = {}
    data['Name'] = nazwa_mailingu
    data['Subject'] = temat
    data['FromName'] = imie_nazwisko
    data['FromAddress'] = mail_wysylki
    data['HtmlFromWebSiteUrl'] = content_mailingu
    data['GroupId'] = '66F3AE43-6DDC-475E-8DB6-6775EBF9030D'
    data['ScheduleTime'] = data_wyslania
    data['TrackLinks'] = True
    response =  mail.service.CreateMailCampaign(strUserName='asgard', strPassword='$12345Asgard', data = data)
    r_json = zeep.helpers.serialize_object(response)
    print(r_json)

# def main():
#     tematy_mailingu = {}


    
#     nazwa_mailingu = input('Nazwa kampanii mailingowej:')
#     tematy_mailingu['PL'] = input('Temat mailingu PL: ')
#     tematy_mailingu['EN'] = input('Temat mailingu EN: ')
#     tematy_mailingu['DE'] = input('Temat mailingu DE: ')
#     tematy_mailingu['FR'] = input('Temat mailingu FR: ')
#     #print(tematy_mailingu)
#     adres_strony_mailingu = input('Wklej link do strony')
#     data_wysylki_input = input('Enter a date in YYYY-MM-DD-HH-MM-SS format')
#     year, month, day, hour, minute, second = map(int, data_wysylki_input.split('-'))
#     data_wyslania = datetime.datetime(year, month, day, hour, minute, second)

#     listaGrupRedlink = show_all_grups()
#     for jezyk in lista_jezykow:
#         temat=tematy_mailingu[jezyk]
#         adres_strony_mailingu = adres_strony_mailingu.split('_')[0]
#         content_mailingu = f'{adres_strony_mailingu}_{jezyk.lower()}.html'
#         for itemRedlink in listaGrupRedlink:
#             if itemRedlink['GroupName'].endswith(f'{jezyk}'):
#                 imie = re.findall(r'(^[A-Z][a-z]*)',itemRedlink['GroupName'].split('_')[0])[0]
#                 nazwisko = re.findall(r'([A-Z][a-z]*$)',itemRedlink['GroupName'].split('_')[0])[0]
#                 mail_wysylki = f'{imie[0].lower()}.{nazwisko.lower()}@asgard.gifts'
#                 imie_nazwisko = f'{imie} {nazwisko}'
#                 wyslij_mailing(nazwa_mailingu, temat, imie_nazwisko, mail_wysylki,content_mailingu, data_wyslania)






