from requests import Session, post, get, put
from random import randint, choice
from re import findall, compile
from time import sleep, time
from threading import Thread, active_count
from urllib.parse import urlencode
from datetime import date
from os import system

created = 0
proxies = []
active_proxies = 0


threads: list[Thread] = []
def check_prox(proxy: str) -> None:
    prox = {'https': f'http://{proxy}', 'http': f'http://{proxy}'}

    try: 
        res = get('https://api.flyx.cloud/otacos/app/api/Optin/GetAnonymous', proxies=prox, timeout=10).json()['data']['optins']
        proxies.append(prox) #{'http': 'http://' + proxy, 'https': 'http://' + proxy}
    except: pass

def get_prox():
    proxies1 = get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all').text.splitlines()

    proxies2 = get('https://www.proxy-list.download/api/v1/get?type=http').text.splitlines()
    proxies3 = get('https://www.proxy-list.download/api/v1/get?type=https').text.splitlines()
    proxies4 = get('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt').text.splitlines()
    """    temps_proxies = []
    res = get('https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc').json()['data']

    for element in res:
        temps_proxies.append(':'.join([element['ip'], element['port']]))

    proxies.append(temps_proxies)"""


    proxies1.extend(proxies2)
    proxies1.extend(proxies3)
    proxies1.extend(proxies4)

    for proxy in proxies1:
        th = Thread(target=check_prox, args=[proxy,],)
        threads.append(th)
        th.start()

def create_email(sess: Session, prox= None) -> str:
    if prox:
        sess.proxies.update(prox)

    res = sess.get('https://email-fake.com/').text

    email: str = findall(r'id="email_ch_text">(.*)</span>', res)[0]
    sess.cookies.update({'surl': '/'.join(email.split('@')[::-1])})

    return sess, email

    
def get_code(sess: Session) -> str:
    while True:
        try:
            res = sess.get('https://email-fake.com/').text
            sleep(3)
            return findall(r'<span id="code">(.*)</span>', res)[0]
        except:
            continue

def get_free_coins(token: str):
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": "Bearer " + token,
        "host": "api.flyx.cloud",
        "user-agent": "okhttp/4.9.1"
    }

    json_data = {
        "Gender": choice(["Male", "Female"]),
        "BirthDate": '/'.join(str(date.today()).split('-')[1:]) + f"/{randint(1980, 2000)}",
        "Country": "France",
        "ZipCode": choice(['69000', '63000']),
        "FavoriteUnits": [
            "Medium tacos",
            "Large tacos"
        ],

        "FavoriteStores": [
            292
        ]
    }

    res = put("https://api.flyx.cloud/otacos/app/api/AdvancedProfile", headers=headers, json=json_data)
    if res.text == '{"data":null,"statusCode":200,"message":"Ok"}':
            points = get('https://api.flyx.cloud/otacos/app/api/User', headers=headers).json()['data']['loyaltyCard']['points']

            while points == 0:
                points = get('https://api.flyx.cloud/otacos/app/api/User', headers=headers).json['data']['loyaltyCard']['points']

            return points
        
    else:
        print('[1] ', res.json())    


def create_account(sess: Session, mail_sess: Session, email: str, pwd: str):
    sess.headers.update({
        "accept": "application/json, text/plain, */*",
        'accept-encoding': "gzip",
        "authorization": "",
        "host": "api.flyx.cloud",
        "connection": "keep-alive",
        "content-type": "application/json",
        "user-agent": "okhttp/4.9.1"
    })

    #optins = sess.get('https://api.flyx.cloud/otacos/app/api/Optin/GetAnonymous').json()['data']['optins']

    json_data = {
        "firstName": "Plati",
        "lastName": "Nows",
        "email": email,
        "password": pwd,
        "confirmPassword": pwd,
        "acceptPushNotifications": "true",
        "isAdvanced": "false",
        "isTwoFactorEnabled": "false",
        "language": "fr-FR",
        "optins": [
            {
                "translationKey": "optins.cc.cgu.sales",
                "moduleId": 2,
                "module": {
                "title": "C&C",
                "key": "null",
                "id": 2,
                "creationDate": "2022-03-16T14:48:51.043069",
                "lastModificationDate": "2022-03-16T14:48:51.043069"
                },
                "isActive": "false",
                "isChecked": "false",
                "isMandatory": "false",
                "hasChanged": "false",
                "legalTextIds": [
                7,
                5
                ],
                "id": 1,
                "creationDate": "0001-01-01T00:00:00",
                "lastModificationDate": "0001-01-01T00:00:00"
            },
            {
                "translationKey": "optins.loyalty.privacy.cgu.sales",
                "moduleId": 1,
                "module": {
                "title": "Loyalty",
                "key": "null",
                "id": 1,
                "creationDate": "2022-03-16T14:48:51.04306",
                "lastModificationDate": "2022-03-16T14:48:51.04306"
                },
                "isActive": "false",
                "isChecked": "false",
                "isMandatory": "false",
                "hasChanged": "false",
                "legalTextIds": [
                2,
                8,
                5
                ],
                "id": 2,
                "creationDate": "0001-01-01T00:00:00",
                "lastModificationDate": "0001-01-01T00:00:00"
            },
            {
                "translationKey": "optins.core.marketing.privacy",
                "moduleId": 4,
                "module": {
                "title": "Core",
                "key": "null",
                "id": 4,
                "creationDate": "2022-03-16T14:48:51.043071",
                "lastModificationDate": "2022-03-16T14:48:51.043071"
                },
                "isActive": "false",
                "isChecked": "false",
                "isMandatory": "false",
                "hasChanged": "false",
                "legalTextIds": [
                2
                ],
                "id": 3,
                "creationDate": "0001-01-01T00:00:00",
                "lastModificationDate": "0001-01-01T00:00:00"
            },
            {
                "translationKey": "optins.core.tracking",
                "moduleId": 4,
                "module": {
                "title": "Core",
                "key": "null",
                "id": 4,
                "creationDate": "2022-03-16T14:48:51.043071",
                "lastModificationDate": "2022-03-16T14:48:51.043071"
                },
                "isActive": "false",
                "isChecked": "false",
                "isMandatory": "false",
                "hasChanged": "false",
                "legalTextIds": [
                2
                ],
                "id": 4,
                "creationDate": "0001-01-01T00:00:00",
                "lastModificationDate": "0001-01-01T00:00:00"
            }
            ],
        }
    
    sess.headers.update({'content-length': str(len(str(json_data).replace(' ', '')))})

    res = sess.post('https://api.flyx.cloud/otacos/app/api/User', json=json_data)

    #print(res.text)

    data = {
        'grant_type': 'password',
        'username': email,
        'password': pwd,
        'client_id': 'app',
        'client_secret': '1QQ2CRDBOHVTSK5R6ZLFWJ7WQUCCM',
        'scope': 'ordering_api app_api identity_api payment_api offline_access openid',
        'language': 'fr-FR'
    }

    sess.headers.update({'content-type':'application/x-www-form-urlencoded'})

    res = sess.post(f'https://api.flyx.cloud/otacos/app/Connect/Token', data=urlencode(data))

    #print(res.text)

    code = get_code(mail_sess)

    #print('Code: ', code, '\n\n')

    res_token = sess.post(f'https://api.flyx.cloud/otacos/app/Connect/Token', data=urlencode(data | {'code': code})).json()

    #print(res_token)

    #print('\n\n')

    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": "Bearer " + res_token['access_token'],
        "host": "api.flyx.cloud",
        "user-agent": "okhttp/4.9.1"
    }

    get('https://api.flyx.cloud/otacos/app/api/User', headers=headers)

    return res_token['access_token']

def create(proxy=None):
    global created, active_proxies, num_thread, ip

    sess = Session()
    connection = True

    if proxy:
        sess.proxies.update({'http': proxy['http']})
        try:
            resp = get('http://ip-api.com/json/', proxies={'http': proxy['http'], 'https': proxy['https']}).json()['query']
            if resp == ip:
                connection = False
        except: connection = False

    while connection:
        try:
            mail_sess, mail = create_email(Session(), proxy)

            #print('\nTrying with', mail, '\n')

            pwd = f'PlatiGen{randint(100, 999)}@{randint(100, 999)}!'

            auth_token = create_account(sess, mail_sess, mail, pwd)

            res = get_free_coins(auth_token)

            if res:
                print(f'[!] Created {res} points | {mail}:{pwd}', f'| {proxy["http"]}' if proxy else '')

                
                with open('accounts.txt', 'a+') as file:
                    file.write(f'| {int(res)} | {mail}:{pwd}:{auth_token}\n')
                    created += 1
            else:
                pass#print(f"[!] Error {mail}:{pwd}")
        
        except:
            connection = False

    if proxy:
        active_proxies -= 1/num_thread

def title_loop():
    global created, active_proxies, num_thread
    times = 1

    while len(threads):
        system(f"title O'Tacos Acccount Creator ~ Stats [ Checking Proxies ~ Threads: {active_count() - num_thread - 1} ~ Checked: {len(proxies)} ]")


    start = time()
    sleep(1)
    while True:
        times = int(time() - start)
        system(f"title O'Tacos Acccount Creator ~ Stats [ Threads: {active_count()} ~ Proxies: {round(active_proxies)} ~ Accounts: {created} ~ Per Second: {round(created/times, 1)} ~ timestamp: {times}]")
        

if __name__ == '__main__':
    system('cls')

    system(f"title O'Tacos Acccount Creator ~ Stats [ Waiting ]")

    prox = input('Use Proxies (y/n) > ').lower()

    if prox == 'y':
        Thread(target=get_prox).start() 

        ip = get('http://ip-api.com/json/').json()['query']

    num_thread = int(input('\nThreads > '))

    Thread(target=title_loop).start()

    for _ in range(num_thread):
        Thread(target=create).start()


    if prox == 'y':
        for thread in threads:
            thread.join()

        threads.clear()

        try:
            for proxy in proxies:
                active_proxies += 1

                sleep(0.5)
                for _ in range(num_thread):
                    Thread(target=create, args=[proxy,],).start()
                    sleep(0.2)
        except:
            pass
