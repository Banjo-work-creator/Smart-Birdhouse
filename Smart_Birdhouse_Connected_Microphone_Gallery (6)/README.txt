SMART BIRDHOUSE — CONNECTED BIRDNET + MICROPHONE GALLERY

This package contains the existing Smart Birdhouse design and an automated
GitHub Pages build that downloads the official BirdNET Live open-source code,
adds a message bridge, and publishes both pages on the SAME HTTPS origin.

The microphone uses BirdNET itself; no screen recording is involved.
When a qualifying detection is received, the gallery stores its species,
date/time and model score, and can show additional bird information.
Gallery data stays in this browser's local storage.

SETUP:
1. Create a public GitHub repository (e.g. smart-birdhouse).
2. Upload Smart_Birdhouse.html, build_smart_birdhouse.py, and
   .github/workflows/deploy.yml (keep the folders).
3. Open repository Settings > Pages and select GitHub Actions.
4. Push files to main; the workflow should build and deploy automatically.
5. Open the HTTPS GitHub Pages URL. Open Microphone, start BirdNET, and
   grant microphone access. Check for Connected status. Then test outdoors
   with a bird call and check Microphone Gallery.

IMPORTANT LIMITATIONS:
- Downloading/opening Smart_Birdhouse.html alone does not bridge public
  BirdNET predictions. Publication of the combined build is essential.
- The included build checks upstream BirdNET source code and may fail if
  the source has changed; inspect the GitHub Actions logs if that happens.
- Do not use the sample-bird button to conclude live recognition works.
- The model predictions and score are estimates, not certainty.
- Bird-name/score transfer is not yet verified in a real deployed site.
- Lake Cathie is the spelling (pronounced Lake Caddai). The local likelihood
  lookup stays unavailable until location-based records are verified.
- This kit does not connect your Arduino; its existing placeholders remain.
- Test on your own phone and browser after publishing.

Upstream BirdNET: https://github.com/birdnet-team/real-time-pwa
