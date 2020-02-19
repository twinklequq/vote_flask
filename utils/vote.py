# -*- coding: utf-8 -*-


import time
import os
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
from matplotlib import pyplot as plt
from matplotlib import dates as mdates


class Mongo:
    def __init__(self, host, port, db):
        self.conn = MongoClient(host, port)
        self.db = self.conn[db]
        self.root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    def get_state(self):
        return self.conn is not None and self.db is not None

    def find_today(self, collection):
        if self.get_state():
            today = self.get_today_timestatmp()
            print(today)
            condition = {'timestamp': {"$gte": today}}
            ret = self.db[collection].find(condition)
            return ret, today

    def find_yesterday(self, collection):
        if self.get_state():
            today = self.get_today_timestatmp()
            yesterday = self.get_yesterday_timestamp()
            condition = {'timestamp': {"$lt": today, "$gte": yesterday}}
            ret = self.db[collection].find(condition)
            return ret

    def find(self, collection):
        if self.get_state():
            ret = self.db[collection].find_one()['vote_info']
            return ret

    def get_today_timestatmp(self):
        today = self.get_utc_8().date().timetuple()
        return time.mktime(today)

    def get_yesterday_timestamp(self):
        yesterday = self.get_utc_8().date() + timedelta(days=-1)
        return time.mktime(yesterday.timetuple())

    def get_utc_8(self):
        dt = datetime.utcnow()
        dt = dt.replace(tzinfo=timezone.utc)
        tzutc_8 = timezone(timedelta(hours=8))
        dst_dt = dt.astimezone(tzutc_8)
        return dst_dt

    def generate_data(self, ret, name='王一博'):
        cordinate = {}
        for item in ret:
            vote_list = item['vote_info']
            for lst in vote_list:
                if lst[0] == name:
                    cordinate[item['time']] = lst[1]
        rank = sorted(cordinate.items(), key=lambda x: x[0])
        dates = [datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S") for item in rank]
        vote_number = [item[1] for item in rank]
        return dates, vote_number

    def generate_plot(self, dates, vote_number):
        pic_date = dates[0].strftime("%m_%d")
        save = os.path.join(self.root, 'static', 'image', pic_date + ".jpg")
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        hoursLoc = mdates.HourLocator(interval=2)  # 为6小时为1副刻度
        ax.xaxis.set_major_locator(hoursLoc)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        ax.plot(dates, vote_number, marker='.')
        ax.grid(True)
        plt.title(dates[0].strftime("%Y-%m-%d"))
        plt.savefig(save)
        return pic_date + ".jpg"


if __name__ == '__main__':
    mongo = Mongo('127.0.0.1', 27017, 'vote')
    ret, timestamp = mongo.find_today('vote_stats')
    print(timestamp)
    for item in ret:
        print(item)
