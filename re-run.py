import json, urllib3
from time import sleep
import argparse

a = argparse.ArgumentParser("aria2c Re-Run Stopped(by Error) Downloads")
a.add_argument('--host', '-u', type=str, required=True)
a.add_argument('--port', '-p', type=int, default=6800)
a.add_argument('--secret', '-s', type=str, default="")
args = a.parse_args()


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
    downloadState = len(aria2caller('tellActive')) == 0
    stoppedOnes = aria2caller('tellStopped', 0, 1000)
    if stoppedOnes:
        for stoppedOne in stoppedOnes:
            files = aria2caller('getFiles', stoppedOne['gid'])
            aria2caller('removeDownloadResult', stoppedOne['gid'])
            aria2caller('addUri', [stoppedOne['files'][0]['uris'][0]['uri']], {"always-resume":"true", "continue":"true", "dir":stoppedOne['dir'], "pause":"true" if downloadState == True else "false"})
    
    sleep(60)

# scenario
# we get stopped list
# we get all info about stopped ones (url, options)
# we delete stop ones and start them again with gathered options! (restart)
# *** UNTIL dawn! 7am

# 1. getFiles (gid)
# 2. removeDownloadResult (gid) < ['OK']
# 3. addUri (URI, allow-overwrite:false, allow-piece-length-change:false,
#   always-resume:true, async-dns:true, auto-file-renaming:true, continue:true,
#   dir:"...")