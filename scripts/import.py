import json, os, pathlib, time, urllib.request, urllib.parse
root = pathlib.Path("data")
root.mkdir(exist_ok=True)
key = os.environ["RA_API_KEY"]
def api(endpoint, **params):
    for attempt in range(4):
        try:
            url = "https://retroachievements.org/API/API_" + endpoint + ".php?" + urllib.parse.urlencode(dict(params,y=key))
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"RA-set-checker/1.0"}), timeout=120) as response:
                data = json.load(response)
            if not isinstance(data,list): raise ValueError("Invalid API response")
            return data
        except Exception:
            if attempt == 3: raise SystemExit("RetroAchievements request failed; cached data retained")
            time.sleep(15 * (attempt+1))
def write(path,data):
    temp=path.with_suffix(".tmp")
    temp.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
    temp.replace(path)
systems=api("GetConsoleIDs",a=1,g=1)
systems=[{"ID":int(s["ID"]),"Name":s["Name"]} for s in systems]
write(root/"consoles.json",systems)
target=os.environ.get("CONSOLE_ID","").strip()
for s in systems:
    if target and str(s["ID"])!=target: continue
    path=root/(str(s["ID"])+".json")
    if not target and path.exists() and os.environ.get("REFRESH")!="true": continue
    print("Importing",s["Name"],flush=True)
    games=api("GetGameList",i=s["ID"],f=1,h=1)
    rows=[{k:g[k] for k in ("ID","Title","ImageIcon","NumAchievements","Hashes")} for g in games if g["NumAchievements"]>0]
    # Mark additions relative to the previous successful console snapshot.
    if path.exists():
        previous = {g["ID"]:g for g in json.loads(path.read_text(encoding="utf-8"))}
        for row in rows:
            row["NewSet"] = row["ID"] not in previous
    else:
        for row in rows:
            row["NewSet"] = False
    write(path,rows)
    time.sleep(5)
