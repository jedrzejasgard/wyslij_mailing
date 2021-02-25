from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import kampania_redlink
import configparser
import requests
import zeep
import datetime
import json
import re

config = configparser.ConfigParser()
configFilePath = 'C:/Users/asgard_48/Documents/Skrypty/BAZA TESTOWA - WGRYWANIE WD/baza mail/redlink.ini'
config.read(configFilePath)

usr = config.get('redlink','redlink_API_user')
passw = config.get('redlink','redlink_API_pass')

def index(request):
    return render(request,'wyslijmailing.html')


def blad_nazwy(request):
    return render(request,'blad_nazwy.html')



def szczegoly_kampanii_redlink(id_kampanii,data_wyslania):
    try:
        redlink_kampania = zeep.Client('https://redlink.pl/ws/v1/Soap/MailCampaigns/MailCampaigns.asmx?WSDL')
        client = zeep.Client('https://redlink.pl/ws/v1/Soap/Contacts/Groups.asmx?WSDL')
        responseBounce = redlink_kampania.service.GetMailCampaignBouncesReport(strUserName=usr, strPassword=passw, strCampaignId = id_kampanii, dateFrom = str(data_wyslania),
                        dateTo = str(datetime.date.today()), offset = 0, limit = 10000 )
        responseCtr = redlink_kampania.service.GetMailCampaignCtrReport(strUserName=usr, strPassword=passw, strCampaignId = id_kampanii, dateFrom = str(data_wyslania),
        dateTo = str(datetime.date.today()), offset = 0, limit = 10000  )
        responseData = redlink_kampania.service.GetMailCampaignData(strUserName=usr, strPassword=passw, strCampaignId = id_kampanii)
        responseOr = redlink_kampania.service.GetMailCampaignOrReport(strUserName=usr, strPassword=passw, strCampaignId = id_kampanii, dateFrom = str(data_wyslania),
        dateTo = str(datetime.date.today()), offset = 0, limit = 10000  )
        responseUnSub = redlink_kampania.service.GetMailCampaignUnregistrationsReport(strUserName=usr, strPassword=passw, strCampaignId = id_kampanii, dateFrom = str(data_wyslania),
        dateTo = str(datetime.date.today()), offset = 0, limit = 10000  )
        r_json_Bounce = zeep.helpers.serialize_object(responseBounce)
        r_json_Ctr = zeep.helpers.serialize_object(responseCtr)
        r_json_Data = zeep.helpers.serialize_object(responseData)
        r_json_Or = zeep.helpers.serialize_object(responseOr)
        group_id = r_json_Data['Data']['GroupId']
        responseGroupCount = client.service.GetGroupContactsCount(strUserName=usr, strPassword=passw, strGroupId = group_id)
        r_json_GroupCount = zeep.helpers.serialize_object(responseGroupCount)
        r_json_UnSub = zeep.helpers.serialize_object(responseUnSub)
        try:
            un_sub = len(r_json_UnSub['Results'])
        except:
            un_sub = 0
        clicks = 0
        for item in r_json_Ctr['Results']['MailCampaignCtrData']:
            clicks+=int(item['Count'])
        bounces = len(r_json_Bounce['Results']['MailCampaignBounceData'])
        otwarte_maile = len(r_json_Or['Results']['MailCampaignOrData'])
        dostarczone_wiadomosci = int(r_json_GroupCount['Data']) - int(bounces)
        ctr = round(clicks*100/dostarczone_wiadomosci,2)
        open_rate = round(otwarte_maile*100/dostarczone_wiadomosci,2)
        dane = [ctr, open_rate, dostarczone_wiadomosci, un_sub]
    except:
        dane = ['blad', 'blad', 'blad','blad']
    return dane
    


def zestawienie_kampanii(request):
    kampanie_model = kampania_redlink.objects.all().values()
    return render(request,'zestawienie_kampanii.html',{'kampanie':kampanie_model})


def detale_kampanii(request):
    if request.method == "POST":
        id_kampanii = (request.POST['form_id_kampanii'])
        kampanie_model = kampania_redlink.objects.filter(id = str(id_kampanii)).values()  
        mailing_dane = {}      
        for kampania in kampanie_model:            
            data_wyslania = str(kampania['kiedy_wyslany'].split(' ')[0])
            for item in kampania:
                item2 = item.split('_')
                if item2[0] == 'redlink':
                    id_redlink =kampania[item]
                    mailing_dane[id_redlink] = (szczegoly_kampanii_redlink(id_redlink,data_wyslania))
        
    return render(request,'detale_kampanii.html',{'szczegoly': kampanie_model , 'dict_mailingi_szczegoly': mailing_dane})


def show_all_grups():
    client = zeep.Client('https://redlink.pl/ws/v1/Soap/Contacts/Groups.asmx?WSDL')
    response = client.service.GetAllGroups(strUserName=usr, strPassword=passw)
    r_json = zeep.helpers.serialize_object(response)
    return r_json['DataArray']['GroupData']


def wyslij_test_redlink(nazwa_mailingu, temat, imie_nazwisko, mail_wysylki,content_mailingu):
    mail = zeep.Client("https://redlink.pl/ws/v1/Soap/MailCampaigns/MailCampaigns.asmx?WSDL")
    data = {}
    data['Name'] = nazwa_mailingu
    data['Subject'] = '   TEST   '+temat
    data['FromName'] = imie_nazwisko
    data['FromAddress'] = mail_wysylki
    data['HtmlFromWebSiteUrl'] = content_mailingu
    data['GroupId'] = '66F3AE43-6DDC-475E-8DB6-6775EBF9030D'
    data['TrackLinks'] = True
    #print(data)
    response =  mail.service.CreateMailCampaign(strUserName=usr, strPassword=passw, data = data)
    r_json = zeep.helpers.serialize_object(response)
    #print(r_json)
    print(r_json['Data'])

def wyslij_do_asgardian_redlink(nazwa_mailingu, temat, imie_nazwisko, mail_wysylki,content_mailingu,data_wyslania):
    mail = zeep.Client("https://redlink.pl/ws/v1/Soap/MailCampaigns/MailCampaigns.asmx?WSDL")
    data = {}
    data['Name'] = nazwa_mailingu
    data['Subject'] = temat
    data['FromName'] = imie_nazwisko
    data['FromAddress'] = mail_wysylki
    data['HtmlFromWebSiteUrl'] = content_mailingu
    data['GroupId'] = '28514C29-8294-41F6-82EB-0E1335B8C5B1'
    data['ScheduleTime'] = data_wyslania
    data['TrackLinks'] = True
    #print(data)
    response =  mail.service.CreateMailCampaign(strUserName=usr, strPassword=passw, data = data)
    r_json = zeep.helpers.serialize_object(response)
    #print(r_json)
    #print(r_json['Data'])

def wyslij_do_handlowcow_redlink(nazwa_mailingu, temat, imie_nazwisko, mail_wysylki,content_mailingu,data_wyslania):
    mail = zeep.Client("https://redlink.pl/ws/v1/Soap/MailCampaigns/MailCampaigns.asmx?WSDL")
    data = {}
    data['Name'] = nazwa_mailingu
    data['Subject'] = f'Wysyłka: {data_wyslania}, Temat: {temat}'
    data['FromName'] = imie_nazwisko
    data['FromAddress'] = mail_wysylki
    data['HtmlFromWebSiteUrl'] = content_mailingu
    data['GroupId'] = 'FAE0FBDB-67E7-47A4-BA0E-7D4C3E650639'
    data['TrackLinks'] = True
    #print(data)
    response =  mail.service.CreateMailCampaign(strUserName=usr, strPassword=passw, data = data)
    r_json = zeep.helpers.serialize_object(response)
    #print(r_json)
    #print(r_json['Data'])


def wyslij_mailing_redlink(nazwa_mailingu, temat, imie_nazwisko, mail_wysylki,content_mailingu,data_wyslania,grup_id):
    mail = zeep.Client("https://redlink.pl/ws/v1/Soap/MailCampaigns/MailCampaigns.asmx?WSDL")
    data = {}
    data['Name'] = nazwa_mailingu
    data['Subject'] = temat
    
    data['FromName'] = imie_nazwisko
    data['FromAddress'] = mail_wysylki
    data['HtmlFromWebSiteUrl'] = content_mailingu
    data['GroupId'] = grup_id
    data['ScheduleTime'] = data_wyslania
    data['TrackLinks'] = True
    #print(data_wyslania)
    response =  mail.service.CreateMailCampaign(strUserName=usr, strPassword=passw, data = data)
    r_json = zeep.helpers.serialize_object(response)
    #print(r_json)
    return str(r_json['Data'])

def wyslij_przypomnienie_redlink(nazwa_mailingu, temat, imie_nazwisko, mail_wysylki,data_wyslania_przypomnienie):
    mail = zeep.Client("https://redlink.pl/ws/v1/Soap/MailCampaigns/MailCampaigns.asmx?WSDL")
    data = {}
    data['Name'] = nazwa_mailingu
    data['Subject'] = f'Sprawdź statystyki: {nazwa_mailingu}'
    data['FromName'] = 'Przypomnienie'
    data['FromAddress'] = mail_wysylki
    data['HtmlFromWebSiteUrl'] = "https://asgard.gifts/www/mailing/przypomnienieTemplet.html";
    data['Mails'] = 'marketing@asgard.gifts'
    data['ScheduleTime'] = data_wyslania_przypomnienie
    data['TrackLinks'] = True
    #print(data_wyslania)
    response =  mail.service.CreateMailCampaign(strUserName=usr, strPassword=passw, data = data)
    r_json = zeep.helpers.serialize_object(response)
    #print(r_json)
    return str(r_json['Data'])

def wyslij_test(request):
    if request.method == "POST":
        dane_mailing_post = request.POST['formMailingTest']
        dane_mailing = json.loads(dane_mailing_post)
        dane_na_strone ={}
        dane_na_strone['nazwa_mailingu'] = dane_mailing['nazwa_mailingu']
        dane_na_strone['temat_PL'] = dane_mailing['temat_PL'].replace(' ','_')
        dane_na_strone['temat_DE'] = dane_mailing['temat_DE'].replace(' ','_')
        dane_na_strone['temat_EN'] = dane_mailing['temat_EN'].replace(' ','_')
        dane_na_strone['temat_FR'] = dane_mailing['temat_FR'].replace(' ','_')
        dane_na_strone['adres_strony_mailingu'] = dane_mailing['adres_strony_mailingu']
        wyslij_test_redlink(dane_mailing['nazwa_mailingu'],dane_mailing['temat_PL'],'Marketing ASGARD','marketing@asgard.gifts',dane_mailing['adres_strony_mailingu'])
        return render(request,'wyslijmailing.html',{'dane': dane_na_strone })
        

def wyslij_mailing(request):
    if request.method == "POST":
        lista_jezykow = ['PL','EN','DE','FR']
        #lista_jezykow = ['DE']
        dane_mailing_post = request.POST['formMailing']
        dane_mailing = json.loads(dane_mailing_post)
        
        tematy_mailingu = {}    
        nazwa_mailingu = dane_mailing['nazwa_mailingu']
        try:
            print(kampania_redlink.objects.filter(nazwa_kampanii = nazwa_mailingu).values())
            len(kampania_redlink.objects.filter(nazwa_kampanii = nazwa_mailingu).values()[0])
            return redirect('http://127.0.0.1:8000/blad_nazwy')
        except:
            print('wysyłam nowy mailing')
            tematy_mailingu['PL'] = dane_mailing['temat_PL'].replace('_',' ')
            tematy_mailingu['EN'] = dane_mailing['temat_EN'].replace('_',' ')
            tematy_mailingu['DE'] = dane_mailing['temat_DE'].replace('_',' ')
            tematy_mailingu['FR'] = dane_mailing['temat_FR'].replace('_',' ')
            #print(tematy_mailingu)
            adres_strony_mailingu = dane_mailing['adres_strony_mailingu']
            data_wysylki_input = dane_mailing['data_wysylki_input'].replace(':','-')
            year, month, day, hour, minute, second = map(int, data_wysylki_input.split('-'))
            data_wyslania = datetime.datetime(year, month, day, hour, minute, second)
            #data_wyslania_przypomnienie = datetime.datetime(year, month, day+2, hour, minute, second)
            #print(data_wyslania_przypomnienie)

            wyslij_do_asgardian_redlink(dane_mailing['nazwa_mailingu'],tematy_mailingu['PL'],'Marketing ASGARD','marketing@asgard.gifts',dane_mailing['adres_strony_mailingu'],data_wyslania)
            wyslij_do_handlowcow_redlink(dane_mailing['nazwa_mailingu'],dane_mailing['temat_PL'],'Marketing ASGARD','marketing@asgard.gifts',dane_mailing['adres_strony_mailingu'],data_wyslania)
            
            listaGrupRedlink = show_all_grups()
            handlowcy_id_kampanii = {}
    
            for jezyk in lista_jezykow:
                if len(tematy_mailingu[jezyk])>1:
                    temat=tematy_mailingu[jezyk]
                    adres_strony_mailingu = adres_strony_mailingu.split('_')[0]
                    content_mailingu = f'{adres_strony_mailingu}_{jezyk.lower()}.html'
                    for itemRedlink in listaGrupRedlink:
                        grup_id = itemRedlink['GroupId']
                        if itemRedlink['GroupName'].endswith(f'{jezyk}'):
                            imie = re.findall(r'(^[A-Z][a-z]*)',itemRedlink['GroupName'].split('_')[0])[0]
                            nazwisko = re.findall(r'([A-Z][a-z]*$)',itemRedlink['GroupName'].split('_')[0])[0]
                            mail_wysylki = f'{imie[0].lower()}.{nazwisko.lower()}@asgard.gifts'
                            redlink_handlowiec_model = f'redlink_id_{imie[0].lower()}_{nazwisko.lower()}_{jezyk.lower()}'
                            imie_nazwisko = f'{imie} {nazwisko}'
                            handlowcy_id_kampanii[redlink_handlowiec_model] = wyslij_mailing_redlink(nazwa_mailingu, temat, imie_nazwisko, mail_wysylki,content_mailingu, data_wyslania,grup_id,)
                            #print(nazwa_mailingu, temat, imie_nazwisko, mail_wysylki,content_mailingu, data_wyslania,grup_id,)
                            
                else:
                    for itemRedlink in listaGrupRedlink:
                        grup_id = itemRedlink['GroupId']
                        if itemRedlink['GroupName'].endswith(f'{jezyk}'):
                            imie = re.findall(r'(^[A-Z][a-z]*)',itemRedlink['GroupName'].split('_')[0])[0]
                            nazwisko = re.findall(r'([A-Z][a-z]*$)',itemRedlink['GroupName'].split('_')[0])[0]
                            redlink_handlowiec_model = f'redlink_id_{imie[0].lower()}_{nazwisko.lower()}_{jezyk.lower()}'
                            handlowcy_id_kampanii[redlink_handlowiec_model]='brak'
            kampania_redlink.objects.create(nazwa_kampanii = nazwa_mailingu ,kiedy_wyslany = data_wyslania,
                temat_mailingu_pl = tematy_mailingu['PL'],
                temat_mailingu_en = tematy_mailingu['EN'],
                temat_mailingu_de = tematy_mailingu['DE'],
                temat_mailingu_fr = tematy_mailingu['FR'],
                redlink_id_a_sitek_pl = handlowcy_id_kampanii['redlink_id_a_sitek_pl'],
                redlink_id_c_idziak_pl = handlowcy_id_kampanii['redlink_id_c_idziak_pl'],
                redlink_id_m_mikolajczyk_pl = handlowcy_id_kampanii['redlink_id_m_mikolajczyk_pl'],
                redlink_id_m_kluszczynska_pl = handlowcy_id_kampanii['redlink_id_m_kluszczynska_pl'],
                redlink_id_t_piszczola_pl = handlowcy_id_kampanii['redlink_id_t_piszczola_pl'],
                redlink_id_a_biegajlo_en = handlowcy_id_kampanii['redlink_id_a_biegajlo_en'],
                redlink_id_j_nieglos_en = handlowcy_id_kampanii['redlink_id_j_nieglos_en'],
                redlink_id_l_urbanczyk_en = handlowcy_id_kampanii['redlink_id_l_urbanczyk_en'],
                redlink_id_m_prange_en = handlowcy_id_kampanii['redlink_id_m_prange_en'],
                redlink_id_m_bujakowska_en = handlowcy_id_kampanii['redlink_id_m_bujakowska_en'],
                redlink_id_p_strzelecki_en = handlowcy_id_kampanii['redlink_id_p_strzelecki_en'],
                redlink_id_l_urbanczyk_de = handlowcy_id_kampanii['redlink_id_l_urbanczyk_de'],
                redlink_id_m_prange_de = handlowcy_id_kampanii['redlink_id_m_prange_de'],
                redlink_id_m_bujakowska_de = handlowcy_id_kampanii['redlink_id_m_bujakowska_de'],
                redlink_id_a_biegajlo_fr = handlowcy_id_kampanii['redlink_id_a_biegajlo_fr'],
                redlink_id_m_prange_fr = handlowcy_id_kampanii['redlink_id_m_prange_fr'],
                redlink_id_m_sobaszek_en = handlowcy_id_kampanii['redlink_id_m_sobaszek_en'],
                link_content = adres_strony_mailingu)
            #print(handlowcy_id_kampanii)

            return redirect('http://127.0.0.1:8000/')
        

# dodaj jeśli responde jest 'OrderedDict([('Code', 0), ('Description', 'OK'), ('Data', '1ED451C1-E416-41F4-A193-1F2A69145DB9'), ('InvalidNumbers', None)])'
# jest 0 to mailing poszedł (popup z informacją zabierający na strone z historią mailingów)
