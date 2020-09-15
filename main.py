#获取token https://webui.mybti.cn/?rd=06091633/#/home/appoint

from subway import Subway

if __name__ == '__main__':
    sub=Subway()
    lineName="昌平线"
    stationName="沙河站"

    enterDate="20200916"    # 设置日期
    timeSlot="0750-0800"    # 设置时间段
    begin_time='2020-09-15 12:00:02.500'    #设置开抢时间
    sub.make_reserve_by_time(lineName,stationName,enterDate,timeSlot,begin_time)
    