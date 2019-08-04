import requests
import urllib
import json


def get_corp_id(name):
    url_suffix = "search/?categories=corporation" + \
                 "&datasource=tranquility" + \
                 "&language=en-us" + \
                 "&search=" + urllib.parse.quote(name) + \
                 "&strict=true"
    url = append_url(url_suffix)
    response = requests.get(url)
    response.raise_for_status()
    return_dict = json.loads(response.content)
    return return_dict["corporation"][0]


def get_ship_name(ship_id):
    body = "[%s]" % ship_id
    url = append_url("universe/names/")
    response = requests.post(url, body)
    response.raise_for_status()
    return_dict = json.loads(response.content)
    return return_dict[0]["name"]


def get_ship_names(ship_ids):
    body = str(ship_ids)
    url = append_url("universe/names/")
    response = requests.post(url, body)
    response.raise_for_status()
    return_dict = json.loads(response.content)
    return list(map(lambda item: item["name"], return_dict))

def get_item_id(name):
    enc_name = urllib.parse.quote(name)
    url_suffix = "search/?" + \
                 "categories=inventory_type" + \
                 "&datasource=tranquility" + \
                 "&language=en-us" + \
                 "&search=" + enc_name + \
                 "&strict=true"
    url = append_url(url_suffix)
    response = requests.get(url)
    response.raise_for_status()
    return_dict = json.loads(response.content)
    return return_dict["inventory_type"][0]


def append_url(suffix):
    return ("https://esi.evetech.net/latest/" + suffix)


if __name__ == "__main__":
    print(get_corp_id("EPSYN"))
    print(get_ship_name(634))
    print(get_ship_names([29984, 29986, 29988, 29990]))
    print(get_item_id("Tengu"))
