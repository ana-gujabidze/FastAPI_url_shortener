# REST URL Shortener API

This project follows material from `www.realpython.com` - [Build a URL Shortener With FastAPI and Python](https://realpython.com/build-a-python-url-shortener-with-fastapi/). There are some variations compared to the instructions as custom URL key and URL deletion automatically after some time have been added.

## Common Usage
The app allows to:
- create a random URL, which has fixed size (9 chars + len(url));
- provide custom name as key for shertened URL, but if it isn't, then random generated key is used;
- validate autimatically provided target URL and check that it is a correct URL and size is below 250 characters;
- count automatically number of times each shortened URL has been visitsed, check this feature in created DB or in `/url` and in `/admin/{secret_key}` endpoints;
- delete URLs automatically after certain period of time (30 days).

---
## Prerequisities
- Python 3.10.5
- Git
---

## Common setup
Clone the repo and install the dependencies.
``` 
git clone https://github.com/ana-gujabidze/FastAPI_url_shortener.git
cd FastAPI_url_shortener/src/
```
The app is connected to Sqlite Database so in order to run this app, create `.env` file similar to `.env_sample` file and specify all environmental variables.

---

## Run locally

In order to run this project first install ***requirements.txt***

```
pip3 install -r requirements.txt
```

Then in the terminal run the command python main.py and it will start running of the server. To check the API endpoint, open http://127.0.0.1:8000 in the browser.

There are 4 different API endpoints available, which can be accessed through this link [here](http://127.0.0.1:8000/docs):

| Endpoint | Action |
| --- | --- |
| / | Return HTML file |
| /url | Show created key with other information from schema |
| /{url_key} | Forward to the target URL |
| /admin/{secret_key} | Show administrative information |
