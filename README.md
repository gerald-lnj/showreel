# showreel

## Introduction

A POC project to generate Reels, which are collections of Clips. Clips and Reels have attributes such as Definition and Standard. Reels can only be comprised of Clips with the same attributes.

Each Clip also has a timestamp duration in the format hh:mm:ss:ff (Hours, Minutes, Seconds, Frames). A Reel's Timestamp duration will be the sum of its Clip's timestamps.

## Stack

This repo contains two folders, one for the Flask server and one for the Vue UI.

This project uses:

- Python 3.8.0
- Node 16.10.0

## Flask server

```bash
cd showreel_server
pip install poetry
poetry install
poetry run flask run --cert=cert.pem --key=key.pem
```

We use self-signed certs to enable https. The certs are included in this repo, or you can generate them with:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

## Vue UI

```bash
cd showreel_ui
npm i
npm run serve
```

Access via Chrome with insecure localhost flag enabled.

## Tests

Units tests are done with pytest.

```bash
cd showreel_server
poetry run pytest
```

## Assumptions

Some assumptions I made:

- Clips can be added to a reel multiple times
- Reels have no need to be saved and retrieved

## Caveats

I faced a bunch of issues in starting MongoDB due to brew and Big Sur, so I used a JSON file to store clips and reels instead.

I was intending to set up a MongoDB database with a validation schema on the for clips and reels, and a migration scipt to populate clips.
