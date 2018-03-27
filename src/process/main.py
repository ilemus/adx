from src.data.spy import spy
from src.retrieve.iextrading import IexData
import time


def start():
    ret = IexData()
    # print(ret.get_quote(spy[0]))
    # Data should be closing prices, not JSON object
    for i in range(len(spy)):
        json = ret.get_chart(spy[i], "2y")
        print(spy[i],)
        data = []
        for index in json:
            data.append(index["close"])
        if len(data) > 0:
            adx_analysis(data, 15, 5)
        time.sleep(0.5)

def get_dec_total(data):
    total = 0
    for i in range(1, len(data)):
        if (data[i] < data[i - 1]):
            total += (data[i - 1] - data[i]) / data[i - 1] * 100
        # End if
    # End for
    return total

def get_adv_total(data):
    total = 0
    for i in range(1, len(data)):
        if (data[i] > data[i - 1]):
            total += (data[i] - data[i - 1]) / data[i - 1] * 100
        # End if
    # End for
    return total

# By each period of 20, get 15 day advances/declines
# for 5 days SMA that value to get adx
# Check causality by low abs change to high abs change (over three weeks)
def adx_analysis(data, r, l):
    # 0, 1, 2, 3, 4, 5, 6, 7
    # -, -, -, -, 1, 1, 1, 1
    adx = [0] * r
    data_dec = [0] * r
    data_inc = [0] * r
    buff = [0] * (l + r)
    count = 0
    for i in range(r, len(data)):
        count += 1
        # Range 5, index 2
        # 0, 1, 2, 3, 4, 5, 6
        # X, X, -, -, -, -, 1
        dec = get_dec_total(data[i - r: i])
        inc = get_adv_total(data[i - r: i])
        data_dec.append(dec)
        data_inc.append(inc)

        # CQueue would be more optimal
        buff.pop(0)
        buff.append(dec + inc)

        # Moving average
        adx.append(sum(buff)/l)
        # End for
    # End for
    # print(adx)
    # print("data: " + str(len(data)) + ", data_inc: " + str(len(data_inc)) + ", data_dec: " + str(len(data_dec)) + ", adx: " + str(len(adx)))
    analysis(data, data_inc, data_dec, adx, l + r)


def analysis(data, adv, dec, adx, offset):
    s = sorted(adx)
    median = 0
    if len(s) % 2 == 0:
        median = adx[len(s) / 2]
    else:
        median = adx[(len(s) - 1) / 2]

    upIsTrend = 0.0
    upTrendCount = 0
    downIsTrend = 0.0
    downTrendCount = 0

    trendCount = 0.0

    isUp = False
    isDown = False

    for i in range(offset, len(adx)):
        if adx[i] > median:
            if dec[i] > adv[i]:
                if isDown:
                    downIsTrend += 1.0
                elif isUp:
                    isUp = False
                else:
                    isDown = True
                    downTrendCount += 1
                    downIsTrend += 1.0
            elif adv[i] > dec[i]:
                if isUp:
                    upIsTrend += 1.0
                elif isDown:
                    isDown = False
                else:
                    isUp = True
                    upTrendCount += 1
                    upIsTrend += 1.0
            else:
                isDown = False
                isUp = False
            # End ifs
        # End adx trending
    # End for loop

    if upIsTrend > 0:
        upIsTrend /= upTrendCount
    if downIsTrend > 0:
        downIsTrend /= downIsTrend
    print("Up average: " + str(upIsTrend) + ", Down average:  " + str(downIsTrend))


start()
