import zkill
import esi
import fuzzworks
import rollout
import collections
from multiprocessing.dummy import Pool as ThreadPool
from functools import reduce


def monthly(name):
    corp_id = esi.get_corp_id(name)
    if corp_id:
        monthly_list = zkill.monthly(corp_id)
        total = monthly_worker(monthly_list)
        output = f"__**{name}** - ISK killed this month:__\n {f'{round(total):,}'} ISK"
        return output
    else:
        return "Corp Not Found"


def monthly_worker(kills):
    values = map(lambda kill: kill["zkb"]["totalValue"], kills)
    return reduce(lambda x, y: x + y, values)


def fleet_size(name):
    corp_id = esi.get_corp_id(name)
    if corp_id:
        kill_list = zkill.kills(corp_id)
        size = fleet_size_worker(kill_list)
        output = f"__** {name} - Fleet Size:**__\n__" \
                 f"max__: {size['max']}\n__min__: {size['min']}\n__avg__: {size['avg']}"
        return output
    else:
        "Corp Not Found"


def fleet_size_worker(kills):
    pool = ThreadPool(8)
    fleet_size_list = list(pool.map(get_no_attackers, kills))
    return {
            "max": max(fleet_size_list),
            "min": min(fleet_size_list),
            "avg": sum(fleet_size_list) / len(fleet_size_list)
            }


def fleet_comp(name):
    corp_id = esi.get_corp_id(name)
    if corp_id:
        kill_list = zkill.kills(corp_id)
        comp = fleet_comp_worker(kill_list)
        output = f"__**{name} - Fleet Comp:**__\n"
        for item in comp:
            output = output + f"__{item[0]}__: {item[1]}\n"
        return output
    else:
        "Corp Not Found"


def fleet_comp_worker(kills):
    pool = ThreadPool(8)
    ship_lists = list(pool.map(get_attackers, kills))
    flat_ship_list = []
    for l in ship_lists:
        for l2 in l:
            flat_ship_list.append(l2)
    flat_ship_list = [x for x in flat_ship_list if x != -1]
    freq_table = collections.Counter(flat_ship_list).most_common(10)
    # return freq_table
    return list(map(replace_id_with_ship_name, freq_table))


def replace_id_with_ship_name(item):
    return esi.get_ship_name(item[0]), item[1]


def get_attackers(kill):
    full_kill = esi.get_killmail(kill["killmail_id"], kill["zkb"]["hash"])
    return list(map(get_attacker_ship, full_kill["attackers"]))


def get_attacker_ship(attacker):
    if "ship_type_id" in attacker.keys():
        return attacker["ship_type_id"]
    else:
        return -1


def get_no_attackers(kill):
    full_kill = esi.get_killmail(kill["killmail_id"], kill["zkb"]["hash"])
    return len(full_kill["attackers"])


def pc(item, flag):
    data = fuzzworks.price_check(item, flag)
    buy = float(data["buy"]["max"])
    sell = float(data["sell"]["min"])
    return f"**{item}:**\n__Max Buy:__ {f'{buy:,.0f}', f'{sell:,.0f}'} ISK \n__Min Sell:__ %s ISK"


def fuel():
    output = "**Fuel Prices:**"
    data = fuzzworks.fuel_prices()
    for fuel_type in data:
        output = output + f"\n **{fuel_type['type']}:**"
        for location in fuel_type["data"]:
            buy = float(location["data"]["buy"]["max"])
            sell = float(location["data"]["sell"]["min"])
            output = output + f"\n\t__{location['location']}__:\t\t" \
                "Max Buy: {f'{buy:,.0f}'} ISK\t\tMin Sell: {f'{sell:,.0f}'} ISK"
    return output


def roll(pilot):
    rollout.rollout(pilot)
    return "%s Rolled Out" % pilot


def last_rolled():
    return rollout.last_rolled()


def intel(name):
    return f"{monthly(name)}\n\n{fleet_size(name)}\n\n{fleet_comp(name)}"


if __name__ == "__main__":
    print(intel("EPSYN"))
    print(pc("gecko", "-j"))
    print(roll("Romad"))
    print(fuel())
