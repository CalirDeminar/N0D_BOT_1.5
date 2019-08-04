import requests
import esi
import json
import datetime


def kills(corp_id):
    url = append_url("w-space/corporationID/%s/finalblow-only/" % corp_id)
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.content)


def monthly(corp_id):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    url = append_url("w-space/corporationID/%s/year/%s/month/%s/finalblow-only/" % (corp_id, year, month))
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.content)


def append_url(suffix):
    return "https://zkillboard.com/api/kills/" + suffix


if __name__ == "__main__":
    corp_id = esi.get_corp_id("EPSYN")
    print(kills(corp_id))
    print(monthly(corp_id))
