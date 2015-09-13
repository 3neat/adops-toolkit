import requests
import json

class TTD(object):
    root = "https://api.thetradedesk.com/v3/"

    def __init__(self, token, path=""):
        self.token = token
        self.auth = {'Content-Type': 'application/json', "TTD-Auth": self.token}
        self.all_advertisers = None

    def get_advertisers(self):
        if not self.all_advertisers:
            self.r = requests.get("https://api.thetradedesk.com/v3/overview/partner/o6cpbgu", headers=self.auth)
            self.rsp = self.r.json()
            self.all_advertisers = []

            for advertiser in self.rsp["Advertisers"]:
                #print "Advertiser: ", "\t", advertiser["AdvertiserId"], "\t", advertiser['AdvertiserName']
                self.all_advertisers.append(advertiser["AdvertiserId"])

        return self.all_advertisers





