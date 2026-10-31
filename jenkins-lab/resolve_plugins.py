import json, re, subprocess, sys, os
raw = open('/tmp/uc.json').read()
m = re.search(r'updateCenter\.post\(\s*(\{.*\})\s*\)\s*;?\s*$', raw, re.S)
data = json.loads(m.group(1) if m else raw)
plugins = data['plugins']
def ver_ok(rc):  # requiredCore like "2.479.1" must be <= 2.580.2
    try: return tuple(int(x) for x in rc.split('.')) <= (2, 580, 2)
    except Exception: return True
wanted = ['workflow-aggregator', 'git']
seen, queue = {}, list(wanted)
while queue:
    name = queue.pop()
    if name in seen: continue
    p = plugins.get(name)
    if not p: print('MISSING from catalogue:', name); continue
    if not ver_ok(p.get('requiredCore','0')): print('requires newer core, skipped:', name, p.get('requiredCore')); continue
    seen[name] = p['version']
    for d in p.get('dependencies', []):
        if not d.get('optional'): queue.append(d['name'])
print(f'closure: {len(seen)} plugins')
os.makedirs('/home/hatch/workspace/jenkins-labwork/home1/plugins', exist_ok=True)
fail = []
for name, version in sorted(seen.items()):
    dest = f'/home/hatch/workspace/jenkins-labwork/home1/plugins/{name}.jpi'
    if os.path.exists(dest): continue
    url = f'https://updates.jenkins.io/download/plugins/{name}/{version}/{name}.hpi'
    r = subprocess.run(['curl','-sL','--fail','--max-time','120','-o',dest,url], capture_output=True, text=True)
    if r.returncode != 0: fail.append((name, r.stderr.strip()[:100]))
print('downloaded:', len(seen)-len(fail), 'failed:', fail)
