py -3 -m mpremote mkdir :/apps/pacman
py -3 -m mpremote cp `
    '__init__.py' `
    'metadata.json' `
    'app.py' `
    :/apps/pacman/

Write-Host "Deployed. Press the reboop button on the badge."
