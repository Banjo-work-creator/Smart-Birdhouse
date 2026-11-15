#!/usr/bin/env python3
# Build Smart Birdhouse with same-origin BirdNET gallery bridge.
# Requires public real-time-pwa at ./birdnet-source and Python 3 / Node 22 / npm.
import os,pathlib,shutil,subprocess
base=pathlib.Path(__file__).resolve().parent
up=base/'birdnet-source'
js=up/'public/js/app.js'
cfg=up/'.eleventy.js'
if not js.is_file() or not cfg.is_file():
    raise SystemExit('Missing birdnet-source. Fetch BirdNET Live from its official public GitHub repo.')
s=js.read_text()
needle='  const top = afterAudio.sort((a, b) => b.confidence - a.confidence).slice(0, 20);'
bridge='''
  // Send the ACTUAL BirdNET acoustic predictions to this site's parent page.
  if (isListening && window.parent !== window && top.length) {
    window.parent.postMessage({
      type: 'birdhouse-birdnet-detections-v1',
      detections: top.slice(0, 1).map(p => ({
        scientificName: p.scientificName || '',
        commonName: p.commonNameI18n || p.commonName || '',
        confidence: p.confidence
      }))
    }, window.location.origin);
  }
'''
if 'birdhouse-birdnet-detections-v1' not in s:
    if needle not in s:raise SystemExit('BirdNET source changed: expected prediction code not found; stopped safely.')
    s=s.replace(needle,needle+bridge,1)
    s=s.replace('    isListening = true;','''    isListening = true;
    if (window.parent !== window) window.parent.postMessage({type:'birdhouse-birdnet-state-v1',state:'listening'},window.location.origin);''',1)
    s=s.replace('  isListening = false;\n  releaseWakeLock();','''  isListening = false;
  if (window.parent !== window) window.parent.postMessage({type:'birdhouse-birdnet-state-v1',state:'stopped'},window.location.origin);
  releaseWakeLock();''',1)
    # Ready is emitted only on model fully loaded, not before.
    s=s.replace('        workerReady = true;','''        workerReady = true;
        if (window.parent !== window) window.parent.postMessage({type:'birdhouse-birdnet-state-v1',state:'ready'},window.location.origin);''',1)
    js.write_text(s)
c=cfg.read_text()
old='pathPrefix: "/real-time-pwa/",'
if old in c:
    c=c.replace(old,'pathPrefix: process.env.BIRDHOUSE_BIRDNET_PREFIX || "/birdnet/",',1)
    cfg.write_text(c)
elif 'BIRDHOUSE_BIRDNET_PREFIX' not in c:raise SystemExit('BirdNET pathPrefix changed; stopped safely.')
prefix=os.getenv('BIRDHOUSE_BIRDNET_PREFIX','/birdnet/')
if not prefix.startswith('/') or not prefix.endswith('/') or '//' in prefix:raise SystemExit('Bad prefix')
subprocess.run(['npm','ci','--no-audit','--no-fund'],cwd=up,check=True)
subprocess.run(['npm','run','build'],cwd=up,env=dict(os.environ,BIRDHOUSE_BIRDNET_PREFIX=prefix),check=True)
site=base/'site';site.mkdir(exist_ok=True)
shutil.copy2(base/'Smart_Birdhouse.html',site/'index.html')
remote=site/'birdnet'
if remote.exists():shutil.rmtree(remote)
shutil.copytree(up/'_site',remote)
print('Built site/index.html and site/birdnet/')
