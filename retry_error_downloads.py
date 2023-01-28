import json, urllib3
from time import sleep
import argparse

parser = argparse.ArgumentParser("aria2c ReTry Stopped(by Error) Downloads")
parser.add_argument('--host', '-u', type=str, required=False, help="Host address")
parser.add_argument('--port', '-p', type=int, default=6800, help="Port to connect to aria2 RPC interface (default=6800)")
parser.add_argument('--secret', '-s', type=str, default="", help="If you set secret, provide it here")
parser.add_argument('--delay', '-d', type=int, default=60, help="Delay time between checks (default=60)")
parser.add_argument('--paused', action='store_true', help="Make all retried downloads in pause state")
args = parser.parse_args()

class aria2rpc():
    secret = None
    server_ip = None
    def __init__(self, server_ip:str, secret:str=None) -> None:
        self.server_ip = server_ip
        self.secret = secret

    def __call__(self, *args: str, **kwds: str):
        params = [f'token:{self.secret}'] if self.secret else []
        params += args[1:]
        jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                      'method':'aria2.'+args[0],
                      'params':params})
        http = urllib3.PoolManager()
        r = http.request('POST', f'http://{self.server_ip}/jsonrpc', body=jsonreq, headers={'Content-Type': 'application/json'})

        rr = json.loads(r.data)
        if r.status == 200:
            return rr['result']
        else:
            print(f"ERROR{rr['error']['code']}: {rr['error']['message']}")
            return None

aria2caller = aria2rpc(f"{args.host}:{args.port}", args.secret)

while True:
    stopped = aria2caller('tellStopped', 0, 1000)
    if stopped:
        print(f'Found {len(stopped)} stopped downloads, ', end='')
        for download in stopped:
            started = 0
            if download['status'] == 'error': # cause of stop
                files = aria2caller('getFiles', download['gid'])
                aria2caller('removeDownloadResult', download['gid'])
                aria2caller('addUri', [download['files'][0]['uris'][0]['uri']], {"always-resume":"true", "continue":"true", "dir":download['dir'], "pause":"true" if args.paused == True else "false"})
                started += 1
        print(f", {started} of them caused by error and started again")
    else:
        print('\rNo stopped downloads found', end='')

    sleep(args.delay)
