import json
import os
import time

structure = {
    "last": None,
    "totals": {}
}

path = "rollout.json"


def init_file():
    if not (os.path.isfile(path)):
        f = open(path, "w")
        f.write(json.dumps(structure))


def write_file(data):
    f = open(path, "w")
    f.write(json.dumps(data))


def read_file():
    f = open(path)
    data = f.read()
    return json.loads(data)


def rollout(pilot):
    init_file()
    data = read_file()
    data["last"] = time.time()
    if pilot in data["totals"]:
        data["totals"][pilot] = data["totals"][pilot] + 1
    else:
        data["totals"][pilot] = 1
    write_file(data)


def last_rolled():
    then = read_file()["last"]
    now = time.time()
    diff = (now - then)
    print(diff)
    if diff < 60:
        return "%s seconds ago" % f"{diff:.0f}"
    elif diff < 3_600:
        return "%s minutes ago" % f"{(diff / 60):,.0f}"
    elif diff < 86_400:
        return "%s hours ago" % f"{(diff / 3_600):,.0f}"
    else:
        return "%s days ago" % f"{(diff / 86_400):,.0f}"


if __name__ == "__main__":
    init_file()
    #print(read_file())
    #rollout("Urb")
    #print(read_file())
    print(last_rolled())
