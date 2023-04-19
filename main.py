import requests
import json

class user:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def GetUsername(self):
        return self.username

    def GetPassword(self):
        return self.password

def GetAuthDetails():
    with open("auth.txt", "r") as file:
        line = file.readline()
        u = user(line.split(",")[0], line.split(",")[1])
    return u

def main():
    u = GetAuthDetails()
    r = requests.get('https://api.rtt.io/api/v1/json/search/SPT', auth=(u.GetUsername(), u.GetPassword()))
    data = r.json()

    services = data.get("services")

    for train in services:
        arrival = train.get("locationDetail").get("gbttBookedArrival")
        if arrival == None:
            arrival = train.get("locationDetail").get("gbttBookedDeparture")

        platform = train.get("locationDetail").get("platform")
        company = train.get("atocCode")
        destination = train.get("locationDetail").get("destination")[-1].get("description")
        origin = train.get("locationDetail").get("origin")[0].get("description")

        print(f"AT: {arrival}, Rail {company}, Platform {platform}, Start {origin}, Des: {origin}")

    with open('data.json', 'w+') as f:
        json.dump(data.get("services")[0], f)

main()