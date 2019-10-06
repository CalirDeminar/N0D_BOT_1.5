import json
import requests
import esi

HUB = {"-j": "60003760",
       "-a": "60008494",
       "-d": "60011866",
       "-r": "60004588",
       "-h": "60005686"}

hub_names = {"-j": "Jita", "-a": "Amarr", "-d": "Dodixie", "-r": "Rens", "-h": "Hek"}

fuel = {"Helium Fuel Block": 4247,
        "Oxygen Fuel Block": 4312,
        "Nitrogen Fuel Block": 4051,
        "Hydrogen Fuel Block": 4246}


def get_price(item, flag):
    url = 'https://market.fuzzwork.co.uk/aggregates/?' + \
          'station=' + HUB[flag] +\
          '&types=' + str(item)
    response = requests.get(url).content
    data = json.loads(response)[str(item)]
    return data


def price_check(item, hub):
    item_id = esi.get_item_id(item)
    if item_id:
        if hub in HUB:
            return get_price(item_id, hub)
        else:
            return "Hub Flag Not Found"
    else:
        return "Item Not Found"


# fuel
def fuel_prices():
    output = []
    for fuel_type in fuel:
        to_put = {"type": fuel_type, "data": []}
        for hub in HUB:
            to_put["data"].append({"location": hub_names[hub], "data": get_price(fuel[fuel_type], hub)})
        output.append(to_put)
    return output


if __name__ == "__main__":
    print(price_check("gecko", "-j"))
    print(price_check("nonsense", "-j"))
    print(fuel_prices())
