#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
交易日历处理 TQ_CHINESE_HOLIDAY_URL
 https://files.shinnytech.com/shinny_chinese_holiday.json
 start_dt=2003-01-01
 end_dt=2022-10-07
"""

import os
from datetime import date, datetime
from typing import Union, List

import pandas as pd
import requests

rest_days_df = None
chinese_holidays_range = None


def _init_chinese_rest_days(headers=None):
    global rest_days_df, chinese_holidays_range
    if rest_days_df is None:
        url = os.getenv("TQ_CHINESE_HOLIDAY_URL", "https://files.shinnytech.com/shinny_chinese_holiday.json")
        rsp = requests.get(url, timeout=30, headers=headers)
        chinese_holidays = rsp.json()
        _first_day = date(int(chinese_holidays[0].split('-')[0]), 1, 1)  # 首个日期所在年份的第一天
        _last_day = date(int(chinese_holidays[-1].split('-')[0]), 12, 31)  # 截止日期所在年份的最后一天
        chinese_holidays_range = (_first_day, _last_day)
        rest_days_df = pd.DataFrame(data={'date': pd.Series(pd.to_datetime(chinese_holidays, format='%Y-%m-%d'))})
        rest_days_df['trading_restdays'] = False  # 节假日为 False
    return chinese_holidays_range


def _get_trading_calendar(start_dt: date, end_dt: date, headers=None):
    """
    获取一段时间内，每天是否是交易日

    :return: DataFrame
        date  trading
    2019-12-05  True
    2019-12-06  True
    2019-12-07  False
    2019-12-08  False
    2019-12-09  True
    """
    _init_chinese_rest_days(headers=headers)
    df = pd.DataFrame()
    df['date'] = pd.Series(pd.date_range(start=start_dt, end=end_dt, freq="D"))
    df['trading'] = df['date'].dt.dayofweek.lt(5)
    result = pd.merge(rest_days_df, df, sort=True, how="right", on="date")
    result.fillna(True, inplace=True)
    df['trading'] = result['trading'] & result['trading_restdays']
    return df

def get_tradeDate(start_dt,end_dt,headers=None):
    df = _get_trading_calendar(start_dt,end_dt,headers=headers)
    temp_df = df.loc[df.trading, ['date']]
    tradeDt = pd.Series(pd.to_datetime(temp_df['date'],format='%Y-%m-%d'))
    return tradeDt.values



if __name__ == "__main__":
    start = '2022-04-01'
    end = '2022-05-07'
    print(_init_chinese_rest_days())
    print(_get_trading_calendar(start,end))
    print(get_tradeDate(start,end))
    pass
