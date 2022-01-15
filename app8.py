# app8.py - Cryptocurrency
import streamlit as st
import pandas as pd
import yfinance as yf
import talib
from talib import abstract
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib
import datetime
import operator

import backtrader as bt
# from strategies import TestStrategy
import matplotlib.pyplot as plt

import backtesting
from backtesting import Strategy, Backtest
from backtesting.lib import crossover


def app():
    st.title('Cryptocurrency')
    st.subheader('- Algorithmic trading strategies and Backtesting')
    st.markdown("***")

    # st.text("")
    st.write('\n')
    st.subheader('1. Candlestick and Analysis Chart')

    expander_candlestick = st.expander(
        label='Select Candlestick Chart Parameters')
    with expander_candlestick:
        with st.form(key='crypto_selection'):
            # st.subheader("Plot Candlestick")
            dropdown = st.text_input(
                'Please key in Crypto Quote:', value='BTC-USD')
            # st.write('Dropdown is', dropdown)
            interval = st.multiselect('Time Interval is:', ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk',
                                                            '1mo', '3mo'], default='1d')
            start = st.date_input(
                'Start Date:', value=pd.to_datetime('2021-01-01'))
            now = datetime.datetime.now()
            end = st.date_input('End Date:', value=pd.to_datetime('now'))

            # (optional, default is '1d')

            submit = st.form_submit_button(label='Submit')

        # @st.cache
    if len(dropdown) > 0:
        # st.write('Dropdown is', dropdown)
        # st.write('Start date is', start)
        # st.write('End date is', end)
        # st.write('Interval is', interval[0])
        #!This created for Backtrader module, Adj Close is merged into Close
        data_raw = yf.download(dropdown, start, now,
                               interval=interval[0], auto_adjust=True)

        # st.write('Raw Data is', data_raw)
        # st.write('Type', type(data_raw))
        # ! Choose different interval will give different default index column name

        data = data_raw
        # data = data.reset_index()
        # data = data.rename(columns={'Date': 'Datetime'})

        # data.index.names = ['Datetime']
        # st.write('Data Raw temp is', data_raw)
        # data.reset_index(inplace=True)
        # st.write('Data processed', data_raw)
        # st.write('Actual Data', data)

    #     dfprice = pd.DataFrame()
    #     dfprice = yf.download(dropdown,start,end)['Close']

    #     dfnew = dfprice.pct_change() + 1
    #     cumret = dfnew.cumprod() - 1
    #     cumret = cumret.fillna(0)
    #     st.line_chart(cumret)

    # def relativeret(df):
    #     rel = df.pct_change()
    #     cumret = (1+rel).cumprod() - 1
    #     cumret = cumret.fillna(0)
    #     return cumret

    # df = relativeret(data['Close'])

    # #    st.bar_chart(volume)

    # Plot Candlestick Chart
    fig = make_subplots(
        rows=1, cols=1,
        #    subplot_titles=("Pricing and Volume Chart",""),
        specs=[[{"secondary_y": True}]])

    # fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            low=data['Low'],
            high=data['High'],
            close=data['Close'],
            open=data['Open'],
            increasing_line_color='green',
            decreasing_line_color='red',
            name=dropdown),
        row=1, col=1,
        secondary_y=False
    )

    # Chart 2 - Volume (Secondary Y)
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Volume'
        ),
        row=1, col=1,
        secondary_y=True
    )

    ################################################################################################################
    st.subheader('2. Choose Technical Indicators or Define Custom Indicators')

    ta_list = ['EMA20', 'EMA60', 'EMA120', 'SMA20', 'SMA60', 'SMA120', 'RSI', 'Upper',
               'Middle', 'Lower', 'Custom']
    dropdown_ta = st.multiselect(
        'Please add Indicator:', ta_list, default=None)

    # Initialization of session variable
    if 'trend_indicator' not in st.session_state:
        st.session_state.trend_indicator = ''
        st.write('Session initial value is', st.session_state.trend_indicator)
    if 'trend_period' not in st.session_state:
        st.session_state.trend_period = 0
        st.write('Trend intial value is', st.session_state.trend_period)

    if 'Custom' in dropdown_ta:
        with st.form(key='custom_indicator'):
            col1, col2 = st.columns(2)
            with col1:
                trend_indicator = st.selectbox(
                    'Please Select Indicators:', ['SMA', 'EMA'])
                trend_period = st.number_input('Period', value=10)
            submit = st.form_submit_button('Submit')

        if submit:
            # st.write(trend_indicator)
            # st.write(str(trend_period))
            # data[trend_indicator+str(trend_period)] = getattr(
            #     talib, trend_indicator(data['Close'], trend_period))
            # data[trend_indicator+str(trend_period)] = getattr(talib,
            # st.write(trend_indicator)
            # st.write(trend_period)

            # if 'trend_indicator' not in st.session_state:
            st.session_state.trend_indicator = trend_indicator
            st.write('Session value is', st.session_state.trend_indicator)

            # if 'trend_period' not in st.session_state:
            st.session_state.trend_period = trend_period
            st.write('Trend Period is', st.session_state.trend_period)

            # st.write(st.session_state.trend_indicator)
            # st.write(st.session_state.trend_period)
            data[st.session_state.trend_indicator+str(st.session_state.trend_period)] = eval(
                "getattr(abstract, f'{st.session_state.trend_indicator}')")(data.Close, st.session_state.trend_period)
            # setattr(data, f'{st.session_state.trend_indicator}{st.session_state.trend_period}, eval("getattr(abstract, f'{st.session_state.trend_indicator}')")(data.Close, st.session_state.trend_period))

            # if 'data[st.session_state.trend_indicator+str(st.session_state.trend_period)]' not in st.session_state:
            #     st.session_state.data[st.session_state.trend_indicator+str(
            #         st.session_state.trend_period)] = data[st.session_state.trend_indicator+str(st.session_state.trend_period)]
            # data[trend_indicator+str(trend_period)] = eval(
            #     "getattr(abstract, f'{trend_indicator}')")(data.Close, trend_period)

            # getattr(talib, f'{trend_indicator}'(data['Close'], trend_period))
            st.write(f'Custom indicator {trend_indicator}{trend_period} has been created successfully',
                     data[trend_indicator+str(trend_period)])
            ta_list.insert(0, f'{trend_indicator}{trend_period}')
            st.write(ta_list)
            # ta_list.insert(0, trend_indicator+str(trend_period))

    data['SMA20'] = talib.SMA(data['Close'], 20)
    data['SMA60'] = talib.SMA(data['Close'], 60)
    data['SMA120'] = talib.SMA(data['Close'], 120)
    data['EMA20'] = talib.EMA(data['Close'], 20)
    data['EMA60'] = talib.EMA(data['Close'], 60)
    data['EMA120'] = talib.EMA(data['Close'], 120)
    data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
    data['Upper'], data['Middle'], data['Lower'] = talib.BBANDS(
        data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    # st.write('Close length', len(data['Close']))
    # st.write('Lower length', len(data['Lower']))

    if 'Custom' not in dropdown_ta:
        for select_indicator in dropdown_ta:
            # st.write("Selected Indicator is " + select_indicator)
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data[select_indicator],
                    name=select_indicator
                )
            )
  ################################################################################################################
    st.subheader('3. Define Algorithmic Trading Strategy')
    ops = {
        '>': operator.gt,
        '<': operator.lt,
        '==': operator.eq,
        '>=': operator.ge,
        '<=': operator.le,
    }

    expander_criteria = st.expander(label='Buy/Sell Criteria Details')
    with expander_criteria:
        with st.form(key='indicator_selection_buy'):
            # Buy Criteria
            container1 = st.container()
            with container1:
                st.write('Please Define Buy Criteria (Container 1)')
                col1, col2, col3 = st.columns(3)

                with col1:
                    # Momentum indicator selection
                    momentum_buy = st.multiselect(
                        'Momentum Indicators:', talib.get_function_groups()['Momentum Indicators'])
                    price_buy = st.multiselect('Price:', [
                        'Close', 'Open', 'High', 'Low'])
                    trend1_buy_list = ['Close', 'Open', 'High', 'Low',
                                       'EMA20', 'EMA60', 'EMA120', 'SMA20', 'SMA60', 'SMA120']
                    if len(st.session_state.trend_indicator) > 0:
                        trend1_buy_list.insert(
                            0, f'{st.session_state.trend_indicator}{st.session_state.trend_period}')
                    trend1_buy = st.multiselect(
                        'Trend Indicators:', trend1_buy_list, key='Trend1')
                    price1_comp_buy = st.multiselect('Price:', [
                        'Close', 'Open', 'High', 'Low'], key='Price1 Compare Buy')

                with col2:
                    # Momentum indicator selection
                    operator1_buy = st.multiselect(
                        'Operator:', ['>', '<', '==', '>=', '<='], key='Operator 1')
                    operator2_buy = st.multiselect(
                        'Operator:', ['>', '<', '==', '>=', '<='], key='Operator 2')
                    operator3_buy = st.multiselect(
                        'Operator:', ['>', '<', '==', '>=', '<=', 'crossover'], key='Operator 3')
                    operator4_buy = st.multiselect(
                        'Operator:', ['>', '<', '==', '>=', '<=', 'crossover'], key='Operator 4')

                with col3:
                    # Momentum indicator selection
                    value_buy = st.text_input(
                        'Value:')
                    # value1 = st.text_input('Please enter the value:', key='Value1')
                    # indicator_volatility_list = talib.get_function_groups()[
                    #     'Volatility Indicators']
                    # indicator_volatility_list.insert(1, 'BB-Lower')
                    # indicator_volatility_list.insert(1, 'BB-Upper')
                    volatility_buy = st.multiselect(
                        'Volatility Indicators:', ['ATR', 'Upper', 'Lower', 'NATR', 'TRANGE'])
                    trend2_buy_list = ['Close', 'EMA20', 'EMA60',
                                       'EMA120', 'SMA20', 'SMA60', 'SMA120']
                    if len(st.session_state.trend_indicator) > 0:
                        trend2_buy_list.insert(
                            0, f'{st.session_state.trend_indicator}{st.session_state.trend_period}')
                    trend2_buy = st.multiselect(
                        'Trend Indicators:', trend2_buy_list, key='Trend2')
                    price2_comp_buy = st.multiselect('Previous price (1 day ago):', [
                        'Close', 'Open', 'High', 'Low'], key='Price2 Compare Buy')
            # st.write('Outsider Container 1')
            # container3 = st.container()
            # with container3:
            #     check = st.checkbox('Trend Indicator')
            #     if check:

            #         st.write('Please Define Buy Criteria (Container 3)')
            #         col1, col2, col3 = st.columns(3)
            #         with col1:
            #             trend1_buy = st.multiselect('Trend Indicators:', ['Close',
            #                                                               'EMA', 'SMA'], key='Trend1a')
            #             if trend1_buy == 'EMA':
            #                 period1 = st.text_input('Period', key='period1')

            #         with col2:
            #             operator3_buy = st.multiselect(
            #                 'Operator:', ['>', '<', '==', '>=', '<=', 'crossover'], key='Operator 3a')
            #         with col3:
            #             trend1_buy = st.multiselect('Trend Indicators:', ['Close',
            #                                                               'EMA', 'SMA'], key='Trend2a')
            #---------------------------------------------------------------------------------------------------#
            # Sell Criteria
            container2 = st.container()
            with container2:
                st.write('Please Define Sell Criteria (Container 2)')
                col1, col2, col3 = st.columns(3)
                with col1:
                    # Momentum indicator selection
                    momentum_sell = st.multiselect(
                        'Momentum Indicators:', talib.get_function_groups()['Momentum Indicators'], key='Sell')
                    # Volatility indicator selection
                    price_sell = st.multiselect('Price:', [
                        'Close', 'Open', 'High', 'Low'], key='Sell')
                    trend1_sell = st.multiselect('Trend Indicators:', [
                        'Close', 'EMA20', 'EMA60', 'EMA120', 'SMA20', 'SMA60', 'SMA120'], key='Trend1_sell')
                    price1_comp_sell = st.multiselect('Price:', [
                        'Close', 'Open', 'High', 'Low'], key='Price1 Compare Sell')

                with col2:
                    # Momentum indicator selection
                    operator1_sell = st.multiselect(
                        'Operator:', ['>', '<', '==', '>=', '<='], key='Operator 1_sell')
                    # Volatility indicator selection
                    operator2_sell = st.multiselect(
                        'Operator:', ['>', '<', '==', '>=', '<='], key='Operator 2_sell')
                    operator3_sell = st.multiselect(
                        'Operator:', ['>', '<', '==', '>=', '<=', 'crossover'], key='Operator 3_sell')
                    operator4_sell = st.multiselect(
                        'Operator:', ['>', '<', '==', '>=', '<=', 'crossover'], key='Operator 4_sell')

                with col3:
                    # Momentum indicator selection
                    value_sell = st.text_input(
                        'Value:', key='Sell')

                    # value1 = st.text_input('Please enter the value:', key='Value1')
                    # indicator_volatility_list = talib.get_function_groups()[
                    #     'Volatility Indicators']
                    # indicator_volatility_list.insert(1, 'BB-Lower')
                    # indicator_volatility_list.insert(1, 'BB-Upper')
                    # Volatility indicator selection
                    volatility_sell = st.multiselect(
                        'Volatility Indicators:', ['ATR', 'Upper', 'Lower', 'NATR', 'TRANGE'], key='Sell')
                    trend2_sell = st.multiselect(
                        'Trend Indicators:', ['Close', 'EMA20', 'EMA60', 'EMA120', 'SMA20', 'SMA60', 'SMA120'], key='Trend2_sell')
                    price2_comp_sell = st.multiselect('Previous price (1 day before):', [
                        'Close', 'Open', 'High', 'Low'], key='Price2 Compare Sell')
            # st.write('Outside the container2')
            submit = st.form_submit_button('Submit')

        if submit:
            # Buy criteria
            if len(operator1_buy) > 0 and len(momentum_buy) > 0:
                data.condition1_buy = ops[operator1_buy[0]](
                    data[momentum_buy[0]], float(value_buy))
            else:
                data.condition1_buy = False

            if len(operator2_buy) > 0 and len(price_buy) > 0 and len(volatility_buy) > 0:
                data.condition2_buy = ops[operator2_buy[0]](
                    data[price_buy[0]], data[volatility_buy[0]])
            else:
                data.condition2_buy = False

            if len(operator3_buy) > 0 and len(trend1_buy) > 0 and len(trend2_buy) > 0:
                #! Bypass the commands after that
                data.condition3_buy = False
                #! data[SMA10] needs to be defined first regardless of operator
                data[st.session_state.trend_indicator+str(st.session_state.trend_period)] = eval(
                    "getattr(abstract, f'{st.session_state.trend_indicator}')")(data.Close, st.session_state.trend_period)
                if operator3_buy[0] == 'crossover':
                    st.write('trend1_buy[0]', trend1_buy[0])
                    st.write('trend2_buy[0]', trend2_buy[0])

                    data['test'] = ''
                    for i in range(len(data)-1, 0, -1):
                        data['test'].iloc[i] = eval(
                            f'data.{trend1_buy[0]}.iloc[{i}] > data.{trend2_buy[0]}.iloc[{i}] and data.{trend1_buy[0]}.iloc[{i-1}] < data.{trend2_buy[0]}.iloc[{i-1}]')
                    # st.write('Check data frame', data)

                else:
                    data.condition3_buy = ops[operator3_buy[0]](
                        getattr(data, trend1_buy[0]), getattr(data, trend2_buy[0]))
                    st.write('trend1_buy[0] is', trend1_buy[0])
                    st.write('trend2_buy[0] is', trend2_buy[0])
                    st.write('Condition 3 is satisfied', data.condition3_buy)

            else:
                data.condition3_buy = False

            if len(operator4_buy) > 0 and len(price1_comp_buy) > 0 and len(price2_comp_buy) > 0:

                # st.write('Show Data', data)
                # st.write('Show current data',
                #          f'data.{price1_comp_buy[0]}.iloc[0]')
                # st.write('Show previous data',
                #          f'data.{price2_comp_buy[0]}.iloc[-1]')
                # st.write('Result'. eval(f'data.{price1_comp_buy[0]}.iloc[0] {operator4_buy[0]} data.{price2_comp_buy[0]}.iloc[-1]')
                # st.write(data)
                for i in range(len(data)-1, 0, -1):
                    #     st.write(data.)
                    #     # data.condition4_buy = ops[operator4_buy[0]](
                    #     #     getattr(data, price1_comp_buy[0]).iloc[i], getattr(data, price2_comp_buy[0]).iloc[i-1])
                    #     # data.Close.iloc[0] > data.High.ilco[-1]
                    # st.write('i Value', i)
                    data.condition4_buy = eval(
                        f'data.{price1_comp_buy[0]}.iloc[{i}] {operator4_buy[0]} data.{price2_comp_buy[0]}.iloc[{i-1}]')
            else:
                data.condition4_buy = False

            #! This is to cater for the situation that nothing is selected
            if type(data.condition1_buy) == bool and type(data.condition2_buy) == bool and type(data.condition3_buy) == bool and type(data.condition4_buy) == bool:
                st.write('No Buy Criteria is selected!')
            else:
                st.write('Condition 1 is', data.condition1_buy)
                st.write('Condition 2 is', data.condition2_buy)
                st.write('Condition 3 is', data.condition3_buy)
                st.write('Condition 4 is', data.condition4_buy)
                data_buy = data.loc[data.condition1_buy |
                                    data.condition2_buy | data.condition3_buy | data.condition4_buy]
                st.write(
                    f'There are total {len(data_buy)} days meet Buy Criteria, they are:', data_buy)

                # Chart 2 - Buy Signal
                fig.add_trace(
                    go.Scatter(
                        x=data_buy.index,
                        y=data_buy['Low']*0.80,
                        mode='markers',
                        name='Buy Singal',
                        marker=go.Marker(size=8,
                                         symbol="triangle-up",
                                         color="green")),
                    row=1, col=1,
                    secondary_y=False)

            # Sell Criteria
            if len(operator1_sell) == 0 or len(momentum_sell) == 0:
                data.condition1_sell = True
            else:
                data.condition1_sell = ops[operator1_sell[0]](
                    data[momentum_sell[0]], float(value_sell))
            if len(operator2_sell) == 0 or len(price_sell) == 0 or len(volatility_sell) == 0:
                data.condition2_sell = True
            else:
                data.condition2_sell = ops[operator2_sell[0]](
                    data[price_sell[0]], data[volatility_sell[0]])
            if len(operator3_sell) == 0 or len(trend1_sell) == 0 or len(trend2_sell) == 0:
                data.condition3_sell = True
            else:
                data.condition3_sell = ops[operator3_sell[0]](
                    data[trend1_sell[0]], data[trend2_sell[0]])
            # st.write(len(operator4_sell))
            # st.write(len(price1_comp_sell))
            # st.write(len(price2_comp_sell))

            if len(operator4_sell) == 0 or len(price1_comp_sell) == 0 or len(price2_comp_sell) == 0:
                data.condition4_sell = True
            else:
                for i in range(len(data)-1, 0, -1):
                    data.condition4_sell = eval(
                        f'data.{price1_comp_sell[0]}.iloc[{i}] {operator4_sell[0]} data.{price2_comp_sell[0]}.iloc[{i-1}]')

            if type(data.condition1_sell) == bool and type(data.condition2_sell) == bool and type(data.condition3_sell) == bool and type(data.condition4_sell) == bool:
                st.write('No Sell Criteria is selected!')
            else:
                data_sell = data.loc[data.condition1_sell |
                                     data.condition2_sell | data.condition3_sell | data.condition4_sell]
                st.write(
                    f'There are total {len(data_sell)} days meet Sell Criteria, they are:', data_sell)

                # Chart 2 - Sell Signal
                fig.add_trace(
                    go.Scatter(
                        x=data_sell['Datetime'],
                        y=data_sell['High']*1.10,
                        mode='markers',
                        name='Sell Singal',
                        marker=go.Marker(size=8,
                                         symbol="triangle-down",
                                         color="red")),
                    row=1, col=1,
                    secondary_y=False)

    fig.update_layout(
        # legend=dict(
        # yanchor="top",
        # y=0.99,
        # xanchor="left",
        # x=0.01),
        title='Pricing and Volume Chart',
        title_x=0.5)
    st.plotly_chart(fig)
    st.write(
        f'There are total {len(data)} trading days in the selected time period')

    # import os
    # st.write(os.getcwd())
    #################################################################################################################
    st.header('4. Conduct Backtesting')

    matplotlib.use('Agg')

    # Create Data Feed
    # data = bt.feeds.YahooFinanceCSVData(
    #    dataname='TSLA.csv',
    # Do not pass values before this date
    #    fromdate=datetime.datetime(2018, 1, 1),
    # Do not pass values after this date
    #    todate=datetime.datetime(2021, 10, 2),
    #    reverse=False)

    # data = yf.download('TSLA', '2018-01-01', '2021-12-29', auto_adjust=True)
    # data.reset_index(inplace=True) #! Need to leave the date as index, otherwise, won't be able to see date
    # data = bt.feeds.PandasData(dataname=yf.download('TSLA', '2018-01-01', '2021-10-02', auto_adjust=True))

    class Custom(Strategy):
        n1 = 20
        n2 = 120
        n3 = 14
        n4 = st.session_state.trend_period

        # def log(self, txt, dt=None):
        #     ''' Logging function for this strategy'''
        #     dt = dt or self.datas[0].datetime.date(0)
        #     print('%s, %s' % (dt.isoformat(), txt))
        # st.write('Variable is', trend1_buy[0])

        def init(self):
            # self.__dict__[momentum_buy[0]] = self.I(
            #     getattr(talib, momentum_buy[0]), self.data.Close, timeperiod=self.n3)

            self.SMA20 = self.I(talib.SMA, self.data.Close, self.n1)
            self.SMA120 = self.I(talib.SMA, self.data.Close, self.n2)
            self.RSI = self.I(talib.RSI, self.data.Close, timeperiod=self.n3)

            st.write('Total Data Length is', len(self.data.Close))
            # st.write('RSI Value', self.RSI)
            # st.write('RSI Value Length', len(self.RSI))
            self.Upper, self.Middle, self.Lower = self.I(
                talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
            self.Close = self.data.Close
            self.High = self.data.High
            indicator_name = st.session_state.trend_indicator + \
                str(st.session_state.trend_period)
            # st.write('Name of custom Indicator', indicator_name)
            if len(st.session_state.trend_indicator) > 0:
                setattr(self, indicator_name, self.I(getattr(
                    talib, f'{st.session_state.trend_indicator}'), self.data.Close, self.n4))
                st.write(
                    f'Custom Indicator {indicator_name} has been instantiated successfully')
            # setattr(self, f'{st.session_state.trend_indicator}'+f'{st.session_state.trend_period}') = self.I(getattr(
            #     talib, f'{st.session_state.trend_indicator}'), self.data.Close, st.session_state.trend_period)
            # st.write('Get attributes', getattr(
            #     self, st.session_state.trend_indicator+str(st.session_state.trend_period)))
            # getattr(self, st.session_state.trend_indicator+str(st.session_state.trend_period)) = self.I(getattr(talib, f'{trend_indicator}'))(self.data.Close, st.session_state.trend_period)

            # st.write(getattr(self, price_buy[0]))
            # st.write('Close length', len(getattr(self, price_buy[0])))
            # st.write(getattr(self, volatility_buy[0]))
            # st.write('Lower length', len(getattr(self, volatility_buy[0])))
            # st.write('Lower length direct', len(self.Lower))
            # self.__dict__[trend1_buy[0]] = self.I(
            #     getattr(talib, trend1_buy[0][0:3]), self.data.Close, self.n1)
            # self.__dict__[trend2_buy[0]] = self.I(
            #     getattr(talib, trend2_buy[0][0:3]), self.data.Close, self.n2)

            # self.sma1 = self.I(talib.SMA, self.data.Close, self.n1)
            # self.sma2 = self.I(talib.SMA, self.data.Close, self.n2)

        #   self.order = None
        #   self.buy_signal
            # st.write('Lower length before Next', len(self.Lower))

            #! Have to take the input from web interface and put all the judgement here
            # st.write('Lower length in Next', len(self.Lower))

            # condiction0 = eval('self.RSI <= 50')
            # st.write('Condiction0 Length', len(condiction0))
            # st.write('Condiction0', condiction0)
            # print('No position and I will buy now')
            # # print('met criteria', not self.position)
            # self.buy()

            if len(operator1_buy) > 0 and len(momentum_buy) > 0:
                # self.condition1_buy_bt = ops[operator1_buy[0]](
                #     getattr(self, momentum_buy[0]), float(value_buy))
                self.condition1_buy_bt = eval(
                    f'self.{momentum_buy[0]} {operator1_buy[0]} {value_buy}')
                # st.write('momentum_buy[0] value is', momentum_buy[0])
                # st.write('self.momentum_buy[0]',
                #          getattr(self, momentum_buy[0]))
                # st.write('self.momentum_buy[0] Length',
                #          len(getattr(self, momentum_buy[0])))
                # st.write('Value_buy is', float(value_buy))
                # st.write('Condition1 Operator1_buy', operator1_buy[0])
                # st.write('Condition 1', self.condition1_buy_bt)
                # st.write('Condition 1 length', len(self.condition1_buy_bt))
            else:
                self.condition1_buy_bt = True

            if len(operator2_buy) > 0 and len(price_buy) > 0 and len(volatility_buy) > 0:
                # st.write('Operator is', operator2_buy[0])
                # # st.write('Type of the Operator is',
                #          type(operator2_buy[0]))
                #! working one on operator!
                # self.condition2_buy_bt = eval(
                #     f'self.data.Close {operator2_buy[0]} self.Upper')
                self.condition2_buy_bt = eval(
                    f'self.data.{price_buy[0]} {operator2_buy[0]} self.{volatility_buy[0]}')
                # st.write('Condition 2', self.condition2_buy_bt)
                # st.write('Condition 2 length', len(self.condition2_buy_bt))
                # self.condition2_buy_bt = eval(
                #     'getattr(self, price_buy[0]) operator2_buy[0] getattr(self, volatility_buy[0])')

                # st.write(getattr(self, price_buy[0]))
                # st.write('Close length', len(getattr(self, price_buy[0])))
                # st.write(getattr(self, volatility_buy[0]))

                # st.write('Lower length', len(
                #     getattr(self, volatility_buy[0])))
                # st.write('Volatility input is', volatility_buy[0])
                # st.write('Lower length direct', len(self.Lower))
                # st.write(ops[operator2_buy[0]])
                # self.condition2_buy_bt = ops[operator2_buy[0]](
                #     getattr(self, price_buy[0]), getattr(self, volatility_buy[0]))
            else:
                self.condition2_buy_bt = True

            if len(operator3_buy) > 0 and len(trend1_buy) > 0 and len(trend2_buy) > 0:
                if operator3_buy[0] == 'crossover':
                    # st.write('Condition3 operator3_buy', operator3_buy[0])
                    # st.write('Condition3 trend1_buy', trend1_buy[0])
                    # st.write('Condition3 trend2_buy', trend2_buy[0])
                    self.condition3_buy_bt = eval(
                        f'{operator3_buy[0]}(self.data.{trend1_buy[0]}, self.{trend2_buy[0]})')

                    # st.write('Condition 3', self.condition3_buy_bt)
                else:
                    # self.condition3_buy_bt = ops[operator3_buy[0]](
                    #     getattr(self, trend1_buy[0]), getattr(self, trend2_buy[0]))
                    st.write('Condition3 trend1_buy', trend1_buy[0])
                    st.write('Condition3 trend2_buy', trend2_buy[0])
                    st.write('Condition3 Operator3_buy', operator3_buy[0])
                    st.write('Self.Close direct', self.Close)
                    st.write('Self.Close direct length', len(self.Close))
                    st.write('Self.Close', getattr(self, trend1_buy[0]))
                    st.write('Self.Close length', len(
                        getattr(self, trend1_buy[0])))
                    st.write('Self.SMA10', getattr(self, trend2_buy[0]))
                    st.write('Self.SMA10 length', len(
                        getattr(self, trend2_buy[0])))
                    # st.write('operator3_buy', operator3_buy[0])
                    # st.write('self.trend1_buy', getattr(self, trend1_buy[0]))
                    # st.write('self.trend1_buy length', len(
                    #     getattr(self, trend1_buy[0])))
                    # st.write('self.trend2_buy', getattr(self, trend2_buy[0]))
                    # st.write('self.trend2_buy length', len(
                    #     getattr(self, trend2_buy[0])))
                    self.condition3_buy_bt = eval(
                        f'self.data.{trend1_buy[0]} {operator3_buy[0]} self.{trend2_buy[0]}')
                    st.write('Condition 3', self.condition3_buy_bt)
                    # st.write('Condition 3 length', len(self.condition3_buy_bt))
                    # self.condition3_buy_bt = ops[operator3_buy[0]](
                    #     getattr(self, trend1_buy[0]), getattr(self, trend2_buy[0]))
            else:
                self.condition3_buy_bt = True

            if len(operator4_buy) > 0 and len(price1_comp_buy) > 0 and len(price2_comp_buy) > 0:
                self.condition4_buy_bt = eval(
                    f'self.{price1_comp_buy[0]}[-1] {operator4_buy[0]} self.{price2_comp_buy[-1]}[-2]')
                st.write('Condition 4', self.condition4_buy_bt)
                st.write('Condition 4 length', len(self.condition4_buy_bt))
            else:
                self.condition4_buy_bt = True

            # st.write('All condictions', condiction0 and self.condition1_buy_bt and self.condition2_buy_bt and self.condition3_buy_bt and self.condition4_buy_bt)
            # st.write('Condiction 1', condition1_buy_bt)
            # st.write('Condiction 2', condition2_buy_bt)
            # condiction0 and self.condition1_buy_bt and self.condition2_buy_bt and self.condition3_buy_bt and self.condition4_buy_bt)
            self.empty_judgement = type(self.condition1_buy_bt) == bool and type(self.condition2_buy_bt) == bool and type(
                self.condition3_buy_bt) == bool and type(self.condition4_buy_bt) == bool

            if self.empty_judgement == True:
                st.write('No Buy Criteria is selected!')

        def next(self):
            if self.empty_judgement != True and self.condition1_buy_bt and self.condition2_buy_bt and self.condition3_buy_bt and self.condition4_buy_bt:
                # if self.RSI <= 25:
                # if ops[operator3_buy[0]](self.__dict__[trend1_buy[0]], self.__dict__[trend2_buy[0]]):
                self.buy()
                # if not self.position:
                #     # print('No position and I will buy now')
                #     # print('met criteria', not self.position)
                #     self.buy()

            #------------------------------------------------------------------------------------------------#
            # Define Sell Condition
            if len(operator1_sell) == 0 or len(momentum_sell) == 0:
                self.condition1_sell_bt = True
            else:
                self.condition1_sell_bt = ops[operator1_sell[0]](
                    getattr(self, momentum_sell[0]), float(value_sell))

            if len(operator2_sell) == 0 or len(price_sell) == 0 or len(volatility_sell) == 0:
                self.condition2_sell_bt = True
            else:
                # st.write('Operator is', operator2_buy[0])
                # # st.write('Type of the Operator is',
                #          type(operator2_buy[0]))
                #! working one on operator!
                # self.condition2_buy_bt = eval(
                #     f'self.data.Close {operator2_buy[0]} self.Upper')

                self.condition2_sell_bt = eval(
                    f'self.data.{price_sell[0]} {operator2_sell[0]} self.{volatility_sell[0]}')

            if len(operator3_sell) == 0 or len(trend1_sell) == 0 or len(trend2_sell) == 0:
                self.condition3_sell_bt = True
            else:
                self.condition3_sell_bt = ops[operator3_sell[0]](
                    getattr(self, trend1_sell[0]), getattr(self, trend2_sell[0]))

            if len(operator4_sell) == 0 or len(price1_comp_sell) == 0 or len(price2_comp_sell) == 0:
                self.condition4_sell_bt = True
            else:
                self.condition4_sell_bt = eval(
                    f'self.{price1_comp_sell[0]}[0] {operator4_sell[0]} self.{price2_comp_sell[-1]}[-1]')

            # if self.condition1_sell_bt and self.condition2_sell_bt and self.condition3_sell_bt and self.condition4_sell_bt:
            #     # if ops[operator3_buy[0]](self.__dict__[trend1_buy[0]], self.__dict__[trend2_buy[0]]):
            #     self.position.close()
                # if not self.position:
                #     # print('No position and I will buy now')
                #     # print('met criteria', not self.position)
                #     self.buy()

            # if self.rsi < 30:
            #     self.buy()

            # elif self.rsi > 70:
            #     self.position.close()

            # if crossover(self.sma1, self.sma2):
            #     self.buy()

            # elif crossover(self.sma2, self.sma1):
            #     self.position.close()

    bt = Backtest(data, Custom, cash=100000,
                  commission=0, exclusive_orders=True)
    output = bt.run()
    output.to_csv('temp.csv')
    temp = pd.read_csv('temp.csv')
    temp.rename(columns={'Unnamed: 0': 'Item', '0': 'Value'}, inplace=True)
    # temp.Value.iloc[3:14] = temp.Value.iloc[3:14].astype(
    #     float).map('{:,.2f}'.format)
    # temp.Value.iloc[18:21] = temp.Value.iloc[18:21].astype(
    #     float).map('{:,.2f}'.format)
    # temp.Value.iloc[24:26] = temp.Value.iloc[24:26].astype(
    #     float).map('{:,.2f}'.format)
    temp.Value.iloc[pd.np.r_[3:14, 18:21, 24:26]] = temp.Value.iloc[pd.np.r_[3:14, 18:21, 24:26]].astype(
        float).map('{:,.2f}'.format)
    # temp.Value[ temp.Value[3:3].astype(float).map('{:,.2f}%'.format)
    # # temp.Value[18:21].astype(float).map('{:,.2f}'.format)
    # temp.Value[24:26].astype(float).map('{:,.2f}'.format)
    # st.write('Backtest Result', output.to_frame())
    st.subheader('Backtest Result')
    # temp.iloc[3:14]
    st.write(temp)
    # st.write('Trade Details', output.stats['_trades'])

    bt.plot(open_browser=False)

    # figure = bt.plot()
    # # show the plot in Streamlit
    # st.pyplot(figure)

    import streamlit.components.v1 as components

    # >>> import plotly.express as px
    # >>> fig = px.box(range(10))
    # >>> fig.write_html('test.html')

    st.subheader("Backtest Chart")

    HtmlFile = open("Custom.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    # st.write(source_code)
    components.html(source_code, height=800)

    # figure = bt.plot()[0][0]
    # #     figure = cerebro.plot(style='candle')[0][0]
    # #     # show the plot in Streamlit
    # st.pyplot(figure)
    # # %matplotlib widget
    # cerebro = bt.Cerebro()

    # # Create Data Feed
    # # data_bt = bt.feeds.YahooFinanceCSVData(
    # #    dataname='TSLA.csv',
    # # Do not pass values before this date
    # #    fromdate=datetime.datetime(2018, 1, 1),
    # # Do not pass values after this date
    # #    todate=datetime.datetime(2021, 10, 2),
    # #    reverse=False)

    # # # Use a backend that doesn't display the plot to the user
    # # we want only to display inside the Streamlit page

    # # data_temp = yf.download(
    # #     'TSLA', '2019-01-01', '2021-12-28', auto_adjust=True)
    # data_bt = bt.feeds.PandasData(dataname=data_raw)

    # # st.write('Data Temp is', data_temp)
    # # st.write('Data Raw is', data_raw)
    # # Add Data Feed
    # st.write('Data Feed is', data_bt)
    # cerebro.adddata(data_bt)

    # with st.form(key='backtest_selection'):
    #     cash = st.number_input('Initial Fund', value=100000)
    #     cerebro.broker.setcash(cash)
    #     submit = st.form_submit_button('Backtest!')

    # if submit:
    #     class MyStrategy(bt.Strategy):

    #         def log(self, txt, dt=None):
    #             ''' Logging function for this strategy'''
    #             dt = dt or self.datas[0].datetime.date(0)
    #             st.write('%s, %s' % (dt.isoformat(), txt))

    #         def __init__(self):
    #             self.rsi = bt.indicators.RelativeStrengthIndex()
    #             self.bb = bt.indicators.BollingerBands()
    #             self.ema_20 = bt.indicators.ExponentialMovingAverage(
    #                 self.data.close, period=20)
    #             self.ema_120 = bt.indicators.ExponentialMovingAverage(
    #                 self.data.close, period=120)

    #         #   self.order = None
    #         #   self.buy_signal

    #         def next(self):

    #             if self.data.close[0] < self.bb.lines.bot and self.rsi[0] < 35 and self.ema_20 > self.ema_120:
    #                 self.order = self.buy()
    #                 self.log('BUY CREATE, %.2f' % self.data.close[0])

    #             if self.data.close[0] > self.bb.lines.top and self.rsi[0] > 65 and self.ema_20 < self.ema_120 and self.position:
    #                 self.order = self.close(percents=100)
    #                 self.log('Close, %.2f' % self.data.close[0])

    #     # Add Strategy
    #     cerebro.addstrategy(MyStrategy)
    #     cerebro.addsizer(bt.sizers.PercentSizer, percents=30)

    #     before_value = cerebro.broker.getvalue()
    #     st.write('Starting Portfilo Value: ' '{0:,.2f}'.format(before_value))

    #     cerebro.run()

    #     after_value = cerebro.broker.getvalue()
    #     st.write('Final Portfilo Value: ' '{0:,.2f}'.format(after_value))
    #     profit = after_value - before_value
    #     profit_rate = (after_value - before_value)/before_value
    #     st.write('Profit amount is: '+'{0:,.2f}'.format(profit))
    #     st.write('Profit Rate is: ' + '{0:,.2f}%'.format((profit_rate)*100))
