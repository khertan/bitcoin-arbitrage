import logging
import config
from observer import Observer
from private_markets import mtgox
from private_markets import bitcoincentral
from traderbot import TraderBot, SpecializedTraderBot
import json
import config


class MockMarket(object):
    def __init__(self, name, fee=0.05, eur_balance=40.,
                 btc_balance=1., persistent=True):
        self.name = name
        self.filename = "traderbot-sim-" + name + ".json"
        self.eur_balance = eur_balance
        self.btc_balance = btc_balance
        self.fee = fee
        self.persistent = persistent
        if self.persistent:
            try:
                self.load()
            except IOError:
                pass

    def buy(self, volume, price):
        logging.info("execute buy %f BTC @ %f on %s"
                     % (volume, price, self.name))
        self.eur_balance -= price * volume
        self.btc_balance += volume - volume * self.fee
        if self.persistent:
            self.save()

    def sell(self, volume, price):
        logging.info("execute sell %f BTC @ %f on %s"
                     % (volume, price, self.name))
        self.btc_balance -= volume
        self.eur_balance += price * volume - price * volume * self.fee
        if self.persistent:
            self.save()

    def load(self):
        data = json.load(open(self.filename, "r"))
        self.eur_balance = data["eur"]
        self.btc_balance = data["btc"]

    def save(self):
        data = {'eur': self.eur_balance, 'btc': self.btc_balance}
        json.dump(data, open(self.filename, "w"))

    def balance_total(self, price):
        return self.eur_balance + self.btc_balance * price

    def get_info(self):
        pass


class SpecializedTraderBotSim(SpecializedTraderBot):
    def __init__(self):
        SpecializedTraderBot.__init__(self)

    def total_balance(self, price):
        market_balances = [i.balance_total(price)
                           for i in set(self.clients.values())]
        return sum(market_balances)

    def execute_trade(self, volume, kask, kbid,
                      weighted_buyprice, weighted_sellprice):
        self.clients[kask].buy(volume, weighted_buyprice)
        self.clients[kbid].sell(volume, weighted_sellprice)

if __name__ == "__main__":
    t = SpecializedTraderBotSim()
    print t.total_balance(33)

