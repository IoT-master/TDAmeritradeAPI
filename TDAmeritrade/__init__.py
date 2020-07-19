from TDAmeritrade.basic_async_api import ApiOperations
import ujson
from datetime import datetime, timedelta
import jwt


class TDAmeritrade(ApiOperations):
    __slot__ = ['api_key']

    def __init__(self):
        self.api_key = self.load_from_json(
            'Confidential/config.json')['ConsumerKey']
        super(TDAmeritrade, self).__init__()

    async def get_price_history(self, ticker, *params, **time_interval):
        """[This API gets the stock history based on the ticker symbol, period_value, period_unit, frequency_value, frequency_unit.
        period_unit: The type of period to show. Valid values are day, month, year, or ytd (year to date). Default is day.
        frequency_unit: The number of the frequencyType to be included in each candle. Valid frequencies by frequencyType (defaults marked with an asterisk):
        minute: 1*, 5, 10, 15, 30
        daily: 1*
        weekly: 1*
        monthly: 1*
        extended_hours: true to return extended hours data, false for regular market hours only. Default is true
        startDate: End date as milliseconds since epoch. If startDate and endDate are provided, period should not be provided. Default is previous trading day.
        endDate: Start date as milliseconds since epoch. If startDate and endDate are provided, period should not be provided.]

        Args:
            ticker ([type]): [description]

        Returns:
            [type]: [description]
        """
        ticker = ticker.upper()
        period_value, period_unit, frequency_value, frequency_unit, extended_hours = params
        param_extension = '&'.join(
            [f"{k}={v}" for k, v in time_interval.items()])
        url = f"https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory?apikey={self.api_key}&periodType={period_unit}&period={period_value}&frequency={frequency_value}&frequencyType={frequency_unit}&needExtendedHoursData={extended_hours}"
        if time_interval:
            url += f"&{param_extension}"

        resp = await self.async_get_wild(url, jsonify_data=True)
        return resp

    @staticmethod
    def is_token_valid(access_token, days_before_exp=1):
        time_stamp = jwt.decode(access_token, verify=False)['exp']
        real_time_stamp = datetime.fromtimestamp(time_stamp)
        return real_time_stamp - timedelta(days=days_before_exp) > datetime.now()

    @staticmethod
    def save_to_json_dict(filename, contents):
        with open(filename, 'w') as f:
            f.write(ujson.dumps(contents, indent=4, sort_keys=True))

    @staticmethod
    def save_to_json(filename, contents):
        with open(filename, 'w') as f:
            f.write(ujson.dumps(contents, indent=4))

    @staticmethod
    def load_from_json(filename):
        with open(filename, 'r') as f:
            return ujson.loads(f.read())
