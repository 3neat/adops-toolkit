import requests
import json

class TTDConnection(object):
    root = "https://api.thetradedesk.com/v3/"

    def __init__(self, token):
        self.token = token
        self.auth = {'Content-Type': 'application/json', "TTD-Auth": self.token}
        self.all_advertisers = None
        self.all_advertisers = self.get_advertisers()


    def get_advertisers(self):
        if not self.all_advertisers:
            self.r = requests.get("https://api.thetradedesk.com/v3/overview/partner/o6cpbgu", headers=self.auth)
            self.rsp = self.r.json()
            self.all_advertisers = []

            for advertiser in self.rsp["Advertisers"]:
                #print "Advertiser: ", "\t", advertiser["AdvertiserId"], "\t", advertiser['AdvertiserName']
                self.all_advertisers.append(advertiser["AdvertiserId"])

        return self.all_advertisers

    def get_reports(self, time):
        self.all_reports = []

        for advertiser in self.all_advertisers:
            payload = {"AdvertiserID": advertiser.encode('ascii','ignore'), "ReportDateUTC": time}
            self.all_reports.append(requests.post("https://api.thetradedesk.com/v3/hdreports",
                                                  headers=self.auth,
                                                  json=payload))
        return self.all_reports








