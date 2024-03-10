import datetime
import os
from functools import reduce

from flask import Flask, request,jsonify, send_from_directory
from logger.logging_config import logger
from flask_cors import CORS
from waitress import serve

import pandas as pd
import akshare as ak
app = Flask(__name__)
# import tushare as ts
# ts.set_token('xxx')

# CORS(app, allow_origin="https://chat.openai.com")
CORS(app, resources={r"*": {"origins": "*"}})


# #设置代理
# import os
# os.environ['http_proxy'] = 'http://127.0.0.1:10809'
# os.environ['https_proxy'] = 'http://127.0.0.1:10809'


@app.get('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.well-known',
                               'ai-plugin.json',
                               mimetype='application/json')

@app.get('/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')

@app.get('/logo.png')
def serve_logo_png():
    return send_from_directory('.', 'logo.png', mimetype='image/png')

# @app.get('/zh_stock_basic')
# def serve_zh_stock_basic():
#     text = request.args.get('text')
#     logger.info(f"->text:{text}")
#     zh_stock_basic_data=_find_zh_stock_basic(text)
#     zh_stock_basic_data = zh_stock_basic_data.to_json(force_ascii=False,orient='records')
#     logger.info(f"->zh_stock_basic_data:{zh_stock_basic_data}")
#     return zh_stock_basic_data

@app.get('/zh_stock_history_data')
def serve_zh_stock_history_data():
    symbol = request.args.get('symbol')
    period = request.args.get('period')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    adjust = request.args.get('adjust') if len(request.args.get('adjust'))<3 else ''
    logger.info(f"->symbol:{symbol},period:{period},start_date:{start_date},end_date:{end_date},adjust:{adjust}")
    zh_stock_history_data = ak.stock_zh_a_hist(symbol=symbol,period=period,start_date=start_date,end_date=end_date,adjust=adjust)
    zh_stock_history_data = zh_stock_history_data.to_json(force_ascii=False,orient='records')

    logger.info(f"->zh_stock_history_data:{zh_stock_history_data}")
    return zh_stock_history_data

@app.get('/zh_stock_yjbb_em_data')
def serve_zh_stock_yjbb_em_data():
    symbol = request.args.get('symbol')
    date = request.args.get('date')
    logger.info(f"symbol:{symbol},date:{date}")
    zh_stock_yjbb_em_data = ak.stock_yjbb_em(date=date)
    zh_stock_yjbb_em_data = zh_stock_yjbb_em_data.loc[zh_stock_yjbb_em_data['股票代码']==symbol]
    zh_stock_yjbb_em_data = zh_stock_yjbb_em_data.to_json(force_ascii=False,orient='records')

    logger.info(f"zh_stock_yjbb_em_data:{zh_stock_yjbb_em_data}")
    return jsonify({"data":zh_stock_yjbb_em_data})

@app.get('/zh_stock_news_em_data')
def serve_zh_stock_news_em_data():
    symbol = request.args.get('symbol')
    limit = int(request.args.get('limit'))
    logger.info(f"symbol:{symbol},limit:{limit}")
    stock_news_em_df = ak.stock_news_em(symbol=symbol)
    stock_news_em_df = stock_news_em_df[['新闻标题', '新闻内容', '发布时间', '文章来源']]
    zh_stock_news_em_data = stock_news_em_df.head(limit)
    zh_stock_news_em_data = zh_stock_news_em_data.to_json(force_ascii=False,orient='records')


    logger.info(f"zh_stock_news_em_data:{zh_stock_news_em_data}")
    return jsonify({"data":zh_stock_news_em_data})

@app.get('/zh_stock_jgdy_tj_em_data')
def serve_zh_stock_jgdy_tj_em_data():
    date = request.args.get('date')
    limit = int(request.args.get('limit'))
    logger.info(f"date:{date},limit:{limit}")
    zh_stock_jgdy_tj_em_data = _find_zh_stock_jgdy_tj_em(date)
    zh_stock_jgdy_tj_em_data = zh_stock_jgdy_tj_em_data.sort_values(by=['接待机构数量','接待日期'],ascending=False)
    zh_stock_jgdy_tj_em_data = zh_stock_jgdy_tj_em_data.head(limit)
    zh_stock_jgdy_tj_em_data = zh_stock_jgdy_tj_em_data.to_json(force_ascii=False,orient='records')

    logger.info(f"zh_stock_jgdy_tj_em_data:{zh_stock_jgdy_tj_em_data}")
    return zh_stock_jgdy_tj_em_data
@app.get('/zh_fund_report_stock_cninfo_data')
def serve_zh_fund_report_stock_cninfo_data():
    symbol = request.args.get('symbol')
    date = request.args.get('date')
    logger.info(f"date:{date},symbol:{symbol}")
    fund_report_stock_cninfo_df = ak.fund_report_stock_cninfo(date=date)
    zh_fund_report_stock_cninfo_data = fund_report_stock_cninfo_df[fund_report_stock_cninfo_df['股票代码'] == symbol]
    zh_fund_report_stock_cninfo_data = zh_fund_report_stock_cninfo_data.to_json(force_ascii=False,orient='records')

    logger.info(f"zh_stock_jgdy_tj_em_data:{zh_fund_report_stock_cninfo_data}")
    return zh_fund_report_stock_cninfo_data
@app.get('/zh_macro_china_data')
def serve_zh_macro_china_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    logger.info(f"start_date:{start_date},end_date:{end_date}")
    zh_macro_china_data =_find_zh_macro_china(start_date,end_date)
    zh_macro_china_data = zh_macro_china_data.to_json(force_ascii=False,orient='records')

    logger.info(f"zh_macro_china_data:{zh_macro_china_data}")
    return zh_macro_china_data
@app.get('/zh_stock_zh_a_hist_min_em_data')
def serve_zh_stock_zh_a_hist_min_em_data():
    symbol = request.args.get('symbol')
    period = request.args.get('period')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    adjust = request.args.get('adjust') if len(request.args.get('adjust')) < 3 else ''
    logger.info(f"->symbol:{symbol},period:{period},start_date:{start_date},end_date:{end_date},adjust:{adjust}")
    zh_stock_zh_a_hist_min_em_data = ak.stock_zh_a_hist_min_em(symbol=symbol, period=period, start_date=start_date, end_date=end_date,
                                               adjust=adjust)
    zh_stock_zh_a_hist_min_em_data = zh_stock_zh_a_hist_min_em_data.to_json(force_ascii=False,orient='records')

    logger.info(f"zh_stock_zh_a_hist_min_em_data:{zh_stock_zh_a_hist_min_em_data}")
    return zh_stock_zh_a_hist_min_em_data
@app.get('/zh_stock_sse_summary_data')
def serve_stock_sse_summary_data():
    stock_sse_summary_df = ak.stock_sse_summary()
    zh_stock_sse_summary_data = stock_sse_summary_df.to_json(force_ascii=False)
    logger.info(f"zh_stock_sse_summary_data:{zh_stock_sse_summary_data}")
    return jsonify({'data':zh_stock_sse_summary_data})

@app.get('/zh_stock_szse_summary_data')
def serve_stock_szse_summary_data():
    date = request.args.get('date')
    logger.info(f"->date:{date}")
    stock_szse_summary_df = ak.stock_szse_summary(date=date)
    zh_stock_szse_summary_data = stock_szse_summary_df.to_json(force_ascii=False)

    logger.info(f"zh_stock_szse_summary_data:{zh_stock_szse_summary_data}")
    return jsonify({'data':zh_stock_szse_summary_data})
@app.get('/zh_stock_board_industry_name_em_data')
def serve_stock_board_industry_name_em_list_data():
    logger.info("get:zh_stock_board_industry_name_em_data")
    stock_board_industry_name_em = pd.DataFrame()
    stock_board_industry_name_em['板块名称'] = ak.stock_board_industry_name_em()['板块名称']
    zh_stock_board_industry_name_em_data = stock_board_industry_name_em.to_json(force_ascii=False)
    logger.info(f"zh_stock_board_industry_name_em_data:{zh_stock_board_industry_name_em_data}")
    return jsonify({'data':zh_stock_board_industry_name_em_data})

@app.post('/zh_stock_board_industry_name_em_data')
def serve_stock_board_industry_name_em_data():
    symbol = request.args.get('symbol')
    start_rank = request.args.get('start_rank')
    end_rank = request.args.get('end_rank')
    logger.info(f"->symbol:{symbol} start_rank:{start_rank} end_rank:{end_rank}")
    stock_board_industry_name_em = _find_zh_stock_board_industry_name_em()
    if symbol is not None:
        stock_board_industry_name_em = stock_board_industry_name_em.query('板块名称==@symbol')
    else:
        start_rank = int(start_rank)
        end_rank = int(end_rank)
        stock_board_industry_name_em = stock_board_industry_name_em.query('排名>=@start_rank and 排名<=@end_rank')

    zh_stock_board_industry_name_em_data = stock_board_industry_name_em.to_json(force_ascii=False,orient='records')
    logger.info(f"zh_stock_board_industry_name_em_data:{zh_stock_board_industry_name_em_data}")
    if len(stock_board_industry_name_em)<1:
        zh_stock_board_industry_name_em_data = 'symbol不在行业名称列表中，请去serve_stock_board_industry_name_em_list_data中查找最接近的symbol，再来查找'
    return jsonify({'data':zh_stock_board_industry_name_em_data})

@app.get('/zh_stock_board_concept_name_em_data')
def serve_stock_board_concept_name_em_data():
    start_rank = int(request.args.get('start_rank'))
    end_rank = int(request.args.get('end_rank'))
    logger.info(f"->start_rank:{start_rank} end_rank:{end_rank}")
    stock_board_concept_name_em = _find_zh_stock_board_industry_name_em()
    stock_board_concept_name_em = stock_board_concept_name_em.query('排名>=@start_rank and 排名<=@end_rank')
    zh_stock_board_concept_name_em_data = stock_board_concept_name_em.to_json(force_ascii=False,orient='records')

    logger.info(f"zh_stock_board_concept_name_em_data:{zh_stock_board_concept_name_em_data}")
    return jsonify({'data':zh_stock_board_concept_name_em_data})

@app.get('/zh_stock_hot_tgb_data')
def serve_stock_hot_tgb_data():
    stock_hot_tgb = ak.stock_hot_tgb()
    del stock_hot_tgb['个股代码']
    zh_stock_hot_tgb_data = stock_hot_tgb.to_json(force_ascii=False)
    logger.info(f"zh_stock_hot_tgb_data:{zh_stock_hot_tgb_data}")
    return jsonify({'data':zh_stock_hot_tgb_data})

@app.get('/zh_stock_hot_rank_em_data')
def serve_stock_hot_rank_em_data():
    stock_hot_rank_em = ak.stock_hot_rank_em()
    stock_hot_rank_em = stock_hot_rank_em['股票名称']
    zh_stock_hot_rank_em_data = stock_hot_rank_em.to_json(force_ascii=False)
    logger.info(f"zh_stock_hot_rank_em_data:{zh_stock_hot_rank_em_data}")
    return jsonify({'zh_stock_hot_rank_em_data':zh_stock_hot_rank_em_data})

@app.get('/zh_stock_individual_fund_flow_rank_data')
def serve_zh_stock_individual_fund_flow_rank_data():
    symbol = request.args.get('symbol')
    period = request.args.get('period')
    zh_stock_individual_fund_flow_rank_data = _find_zh_stock_individual_fund_flow_rank(symbol,period)
    zh_stock_individual_fund_flow_rank_data = zh_stock_individual_fund_flow_rank_data.to_json(force_ascii=False,orient='records')
    logger.info(f"->symbol:{symbol} period:{period}")
    logger.info(f"zh_stock_individual_fund_flow_rank_data:{zh_stock_individual_fund_flow_rank_data}")
    return jsonify({'data':zh_stock_individual_fund_flow_rank_data})

@app.get('/zh_stock_market_fund_flow_data')
def serve_zh_stock_market_fund_flow_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    stock_market_fund_flow_df = ak.stock_market_fund_flow()
    stock_market_fund_flow_df = stock_market_fund_flow_df.astype(str)
    stock_market_fund_flow_df = stock_market_fund_flow_df.query('日期>=@start_date and 日期<=@end_date')
    zh_stock_market_fund_flow_data = stock_market_fund_flow_df
    zh_stock_market_fund_flow_data = zh_stock_market_fund_flow_data.to_json(force_ascii=False,orient='records')
    logger.info(f"->start_data:{start_date} end_date:{end_date}")
    logger.info(f"zh_stock_market_fund_flow_data:{zh_stock_market_fund_flow_data}")
    return jsonify({'data':zh_stock_market_fund_flow_data})
@app.get('/zh_stock_sector_fund_flow_rank_data')
def serve_zh_stock_sector_fund_flow_rank_data():
    sector_type = request.args.get('sector_type')
    period = request.args.get('period')
    stock_sector_fund_flow_rank_df = ak.stock_sector_fund_flow_rank(indicator=period, sector_type=sector_type)
    zh_stock_sector_fund_flow_rank_data = stock_sector_fund_flow_rank_df.to_json(force_ascii=False)
    logger.info(f"->sector_type:{sector_type} period:{period}")
    logger.info(f"zh_stock_sector_fund_flow_rank_data:{zh_stock_sector_fund_flow_rank_data}")
    return jsonify({'data':zh_stock_sector_fund_flow_rank_data})
@app.get('/zh_stock_sector_fund_flow_summary_data')
def serve_zh_stock_sector_fund_flow_summary_data():
    sector_type = request.args.get('sector_type')
    period = request.args.get('period')
    logger.info(f"->sector_type:{sector_type} period:{period}")

    if sector_type not in _find_zh_stock_board_industry_name_em()['板块名称'].tolist():
        return jsonify({'data': 'sector_type不在行业名称列表中，请去serve_stock_board_industry_name_em_list_data中查找最接近的sector_type，再来查找'})
    stock_sector_fund_flow_summary =  ak.stock_sector_fund_flow_summary(symbol=sector_type, indicator=period)
    stock_sector_fund_flow_summary = stock_sector_fund_flow_summary.head(20)
    zh_stock_sector_fund_flow_summary_data = stock_sector_fund_flow_summary.to_json(force_ascii=False,orient='records')

    logger.info(f"zh_stock_sector_fund_flow_summary_data:{zh_stock_sector_fund_flow_summary_data}")
    return jsonify({'data':zh_stock_sector_fund_flow_summary_data})

@app.get('/zh_stock_sector_fund_flow_hist_data')
def serve_zh_stock_sector_fund_flow_hist_data():
    sector_type = request.args.get('sector_type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    logger.info(f"->sector_type:{sector_type} start_date:{start_date} end_date:{end_date}")
    if sector_type not in _find_zh_stock_board_industry_name_em()['板块名称'].tolist():
        return jsonify({'data': 'sector_type不在行业名称列表中，请去serve_stock_board_industry_name_em_list_data中查找最接近的sector_type，再来查找'})
    stock_sector_fund_flow_hist =  ak.stock_sector_fund_flow_hist(symbol=sector_type)
    stock_sector_fund_flow_hist['日期'] = stock_sector_fund_flow_hist['日期'].astype(str)
    stock_sector_fund_flow_hist = stock_sector_fund_flow_hist.query('日期>=@start_date and 日期<=@end_date').head(30)
    zh_stock_sector_fund_flow_hist_data = stock_sector_fund_flow_hist.to_json(force_ascii=False,orient='records')

    logger.info(f"zh_stock_sector_fund_flow_hist_data:{zh_stock_sector_fund_flow_hist_data}")
    return jsonify({'data':zh_stock_sector_fund_flow_hist_data})

def _find_zh_stock_board_industry_name_em():
    today_date = datetime.datetime.today().strftime('%Y%m%d')
    root_path = os.path.join(os.path.dirname(__file__), 'cache')
    file_name = "zh_stock_board_industry_cons_em" + today_date + ".csv"
    file_path = os.path.join(root_path, file_name)
    if os.path.exists(file_path):
        zh_stock_board_industry_name_em = pd.read_csv(file_path, dtype=str)
    else:
        zh_stock_board_industry_name_em = ak.stock_board_industry_name_em()
        if len(zh_stock_board_industry_name_em) < 1000:
            yesterday_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
            yesterday_root_path = os.path.join(os.path.dirname(__file__), 'cache')
            yesterday_file_name = "zh_stock_board_industry_name_em" + yesterday_date + ".csv"
            yesterday_file_path = os.path.join(yesterday_root_path, yesterday_file_name)
            i = 0
            while os.path.exists(yesterday_file_path):
                i += 1
                yesterday_date = (datetime.datetime.today() - datetime.timedelta(days=i)).strftime('%Y%m%d')
                yesterday_file_name = "zh_stock_board_industry_name_em" + yesterday_date + ".csv"
                yesterday_file_path = os.path.join(yesterday_root_path, yesterday_file_name)

            if os.path.exists(yesterday_file_path):
                zh_stock_board_industry_name_em = pd.read_csv(yesterday_file_path, dtype=str)
        zh_stock_board_industry_name_em.to_csv(file_path)
        zh_stock_board_industry_name_em = zh_stock_board_industry_name_em.astype(str)
    find_data = zh_stock_board_industry_name_em
    return find_data
def _find_zh_stock_individual_fund_flow_rank(symbol,period):
    stock_individual_fund_flow_rank_df = ak.stock_individual_fund_flow_rank(indicator=period)
    stock_individual_fund_flow_rank_df = stock_individual_fund_flow_rank_df.query('代码==@symbol')
    return stock_individual_fund_flow_rank_df
def _find_zh_macro_china(start_date,end_date):
    # 获取宏观数据
    macro_china_qyspjg_df = ak.macro_china_qyspjg()
    macro_china_qyspjg_df['月份'] = pd.to_datetime(macro_china_qyspjg_df['月份'], format='%Y年%m月份').apply(
        lambda x: x.strftime('%Y%m'))
    macro_china_qyspjg_df = macro_china_qyspjg_df.query('月份>=@start_date and 月份<=@end_date')

    macro_china_fdi_df = ak.macro_china_fdi()
    macro_china_fdi_df['月份'] = pd.to_datetime(macro_china_fdi_df['月份'], format='%Y年%m月份').apply(
        lambda x: x.strftime('%Y%m'))
    macro_china_fdi_df = macro_china_fdi_df.query('月份>=@start_date and 月份<=@end_date')

    macro_china_shrzgm_df = ak.macro_china_shrzgm()
    macro_china_shrzgm_df = macro_china_shrzgm_df.query('月份>=@start_date and 月份<=@end_date')

    dataframes = [macro_china_qyspjg_df, macro_china_fdi_df, macro_china_shrzgm_df]
    def merge_dataframes(df1, df2):
        return pd.merge(df1, df2, on='月份',how='outer')
    all_df = reduce(merge_dataframes, dataframes)
    return all_df
def _find_zh_stock_jgdy_tj_em(date):
    date = date
    today_date = datetime.datetime.today().strftime('%Y%m%d')
    root_path = os.path.join(os.path.dirname(__file__), 'cache')
    file_name = "zh_stock_jgdy_tj_em_" + today_date + ".csv"
    file_path = os.path.join(root_path, file_name)
    if os.path.exists(file_path):
        zh_stock_jgdy_tj_em_data = pd.read_csv(file_path, dtype=str)
    else:
        zh_stock_jgdy_tj_em_data = ak.stock_jgdy_tj_em()
        if len(zh_stock_jgdy_tj_em_data) < 1000:
            yesterday_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
            yesterday_root_path = os.path.join(os.path.dirname(__file__), 'cache')
            yesterday_file_name = "zh_stock_jgdy_tj_em_" + yesterday_date + ".csv"
            yesterday_file_path = os.path.join(yesterday_root_path, yesterday_file_name)
            i = 0
            while os.path.exists(yesterday_file_path):
                i += 1
                yesterday_date = (datetime.datetime.today() - datetime.timedelta(days=i)).strftime('%Y%m%d')
                yesterday_file_name = "zh_stock_jgdy_tj_em_" + yesterday_date + ".csv"
                yesterday_file_path = os.path.join(yesterday_root_path, yesterday_file_name)

            if os.path.exists(yesterday_file_path):
                zh_stock_jgdy_tj_em_data = pd.read_csv(yesterday_file_path, dtype=str)
        zh_stock_jgdy_tj_em_data.to_csv(file_path)
        zh_stock_jgdy_tj_em_data = zh_stock_jgdy_tj_em_data.astype(str)
    find_data = zh_stock_jgdy_tj_em_data.query('公告日期 >= @date')
    return find_data
def _find_zh_stock_basic(text):
    today_date = datetime.datetime.today().strftime('%Y%m%d')
    root_path = os.path.join(os.path.dirname(__file__), 'cache')
    file_name = "zh_stock_basic_" + today_date + ".csv"
    file_path = os.path.join(root_path, file_name)
    if os.path.exists(file_path):
        zh_stock_basic_data = pd.read_csv(file_path, dtype=str)
    else:
        pro = ts.pro_api()
        zh_stock_basic_data = pro.stock_basic(exchange='', list_status='L',
                                              fields='symbol,name,area,industry,fullname,enname,cnspell,market,exchange,list_status,list_date,delist_date')
        if len(zh_stock_basic_data) < 1000:
            yesterday_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
            yesterday_root_path = os.path.join(os.path.dirname(__file__), 'cache')
            yesterday_file_name = "zh_stock_basic_" + yesterday_date + ".csv"
            yesterday_file_path = os.path.join(yesterday_root_path, yesterday_file_name)
            i = 0
            while os.path.exists(yesterday_file_path):
                i += 1
                yesterday_date = (datetime.datetime.today() - datetime.timedelta(days=i)).strftime('%Y%m%d')
                yesterday_file_name = "zh_stock_basic_" + yesterday_date + ".csv"
                yesterday_file_path = os.path.join(yesterday_root_path, yesterday_file_name)

            if os.path.exists(yesterday_file_path):
                zh_stock_basic_data = pd.read_csv(yesterday_file_path, dtype=str)
        zh_stock_basic_data.to_csv(file_path)
        zh_stock_basic_data = zh_stock_basic_data.astype(str)
    find_data = zh_stock_basic_data.loc[(zh_stock_basic_data['symbol'] == text) | (zh_stock_basic_data['name'] == text) | (zh_stock_basic_data['fullname'] == text) | (zh_stock_basic_data['enname'] == text) | (zh_stock_basic_data['cnspell'] == text)]
    return find_data




if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5003)
