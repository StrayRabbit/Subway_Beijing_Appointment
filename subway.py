import time
import requests
import json
import urllib3

from exception import AsstException
from config import global_config
from log import logger
from timer import Timer
from messenger import Messenger
from util import(
    parse_json,
    DEFAULT_HEADER
)

BASE_URL="https://webapi.mybti.cn"

class Subway(object):
    def __init__(self):
        self.header = DEFAULT_HEADER
        self.send_message = global_config.getboolean('messenger', 'enable')
        self.messenger = Messenger(global_config.get('messenger', 'sckey')) if self.send_message else None

    def make_reserve_by_time(self,lineName,stationName,enterDate,timeSlot,begin_time,retry=2,interval=2):
        """预约地铁。
        :param lineName: 几号线（昌平线）
        :param stationName: 地铁站名（沙河站）
        :param enterDate: 预约日期
        :param timeSlot: 时间段（0730-0740）
        :param begin_time: 开始执行时间
        :return:
        """
        t = Timer(begin_time=begin_time)
        t.start()

        for count in range(1, retry + 1):
            logger.info('第[%s/%s]次尝试定时预约', count, retry)
            if self.make_reserve(lineName=lineName,stationName=stationName, enterDate=enterDate,timeSlot=timeSlot):
                 break
            logger.info('休息%ss', interval)
            time.sleep(interval)
        else:
            logger.info('执行结束，预约失败！')
    def make_reserve(self,lineName,stationName,enterDate,timeSlot):
        """地铁预约
        :param lineName: 几号线（昌平线）
        :param stationName: 地铁站名（沙河站）
        :param enterDate: 预约日期
        :param timeSlot: 时间段（0730-0740）
        :return:bool
        """
        url = BASE_URL+"/Appointment/CreateAppointment"
        data = {"lineName": lineName, "snapshotWeekOffset": 0, "stationName": stationName, "enterDate": enterDate,
            "snapshotTimeSlot": "0630-0930", "timeSlot": timeSlot}
        result = requests.post(url, json=data, headers=self.header,verify=False)
        resp_json =parse_json(result.text)
        if(resp_json['balance']<0):
            logger.error(result.text)
            self.messenger.send(text='预约失败：%s' % result.text)
            return False
        logger.info(result.text)
        self.messenger.send(text='预约成功：%s' % result.text)
        return True

    def get_info(self):
        url=BASE_URL+"/User/GetUserInfoByUserId"
        result=requests.get(url,headers=self.header,verify=False)
        print(result.text)

    def get_auth(self):
        url=BASE_URL+"/User/GetWXUserInfoAndUpdate"
        result=requests.get(url,headers=self.header,verify=False)
        print(result.text)

    def test(self):
        url="/EasyToPass/CheckOpenid"
        result=requests.get(url)
        print(result.text)
        # self.messenger.send(text='预约结果：%s' % '测试')