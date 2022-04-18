# coding:utf8
"""
url = "http://sqt.gtimg.cn/utf8/q=r_hk00981"

url 参数改动
股票代码 q=r_hk00981
"""


import re
import time

from . import basequotation


class FutureUS(basequotation.BaseQuotation):
    """sina免费行情获取"""

    max_num = 800
    grep_detail = re.compile(
        r"(\d+)=[^\s]([^\s,]+?)%s%s"
        % (r",([\.\d]+)" * 29, r",([-\.\d:]+)" * 2)
    )
    grep_detail_with_prefix = re.compile(
        r"(\w{2}\d+)=[^\s]([^\s,]+?)%s%s"
        % (r",([\.\d]+)" * 29, r",([-\.\d:]+)" * 2)
    )
    del_null_data_stock = re.compile(
        r"(\w{2}\d+)=\"\";"
    )

    # def _gen_stock_prefix(self, stock_codes):
    #     print(stock_codes)
    #     return ["hf_{}".format(code) for code in stock_codes]

    @property
    def stock_api(self) -> str:
        return f"http://hq.sinajs.cn/rn={int(time.time() * 1000)}&list="

    def _get_headers(self) -> dict:
        headers = super()._get_headers()
        return {
            **headers,
            'Referer': 'http://finance.sina.com.cn/'
        }

 
    def format_response_data(self, rep_data, prefix=False):
        # print(type(rep_data[0]))
        if len(rep_data) == 1:
            stocks_detail = rep_data[0]
            stocks_detail = stocks_detail.replace('var hq_str_hf_NQ="', '')
            stocks_detail = stocks_detail.replace('";\n', '')
            stock = stocks_detail.split(",")
            stock_dict = dict(
                close=float(stock[0]),
                # settle=float(stock[1]),
                bp=float(stock[2]),
                ap=float(stock[3]),
                high=float(stock[4]),
                low=float(stock[5]),
                time=(stock[6]),
                last_close=float(stock[7]),
                open=float(stock[8]),
                volume=float(stock[9]),
                bv=float(stock[10]),
                av=float(stock[11]),
                date=stock[12],
                name=stock[13],
            )

            return stock_dict
        else:
            print(rep_data)
            raise