import streamlit as st
import datetime as dt
import dateutil.relativedelta as du
import yfinance as yf
import plotly.graph_objects as go
from PIL import Image


def main():

	# app logos
	header = Image.open('header.jpeg')
	st.sidebar.image(header, use_column_width=True)

	# default values to period filter
	today = dt.datetime.today()
	month_before = today - du.relativedelta(months=3)
	dtinit = st.sidebar.date_input('start:', month_before)
	dtend = st.sidebar.date_input('end', today, max_value=today)

	# load tickers list
	tickers_sel = st.sidebar.multiselect("Choose the tickets:", get_tickers_list())

	# source credits
	st.sidebar.markdown('<p> powered by: <a target="_blank" rel="noopener noreferrer" href="http://www.streamlit.io">streamlit.io</a></p>', unsafe_allow_html=True)
	st.sidebar.markdown('<p> source: <a target="_blank" rel="noopener noreferrer" href="https://finance.yahoo.  com">yahoo finance</a></p>', unsafe_allow_html=True)

	if len(tickers_sel) > 0:
		stock_data = load_stock_data(tickers_sel, dtinit, dtend, 'scatter')

		if not stock_data.empty:
			chart_fig = get_chart_fig(stock_data, tickers_sel, "Stock Performance", 'scatter')
			st.plotly_chart(chart_fig)
		else:
			st.write('no data available!')


def load_stock_data(tickers, start, end, kind='scatter'):
	if kind == 'scatter':
		df = yf.download(tickers, start=start, end=end)
	elif kind == 'candle':
		df = yf.download(tickers, start=start, end=end)

	return df.reset_index()


def get_tickers_list():
	tickers = ["PETR4.SA","BRKM5.SA",'LAME4.SA','ABEV3.SA','VALE5.SA','VALE3.SA',
	           'OIBR4.SA','BBDC4.SA','MRVE3.SA','ITUB4.SA','EMBR3.SA','CYRE3.SA',
	           'BTOW3.SA','BRKM5.SA','USIM3.SA','BBDC3.SA','PRML3.SA','MRFG3.SA',
	           'JBSS3.SA','DTEX3.SA','CPLE6.SA','CPFE3.SA','CGAS5.SA','USIM5.SA',
	           'TAEE11.SA','RSID3.SA','PFRM3.SA','PCAR4.SA','CESP6.SA','BBAS3.SA',
	           'VLID3.SA']

	tickers.sort()

	return tickers


def     get_chart_fig(df, tickers, title, kind='scatter'):

	x_axis = df.index

	if kind == 'scatter':
		fig = go.Figure()

		for ix in range(len(tickers)):
			if len(tickers) > 1:
				fig.add_trace(go.Scatter(
					name=tickers[ix],
					x=x_axis,
					y=df["Close", tickers[ix]],
					#line=dict(color='#17BECF'),
					opacity=0.8
				)
				)
			else:
				fig.add_trace(go.Scatter(
					name=tickers[ix],
					x=x_axis,
					y=df['Close'],
					#line=dict(color='#17BECF'),
					opacity=0.8
				)
				)
	elif kind == 'candle':
		fig = go.Figure(
			data=[go.Candlestick(
				x=x_axis,
				open=df['Open'],
				high=df['High'],
				low=df['Low'],
				close=df['Close'])])

	fig.update_layout(
		dict(
			title=title,
			title_x=0.5,
			height=500,
			width=800,
			legend_title_text='Tickers',
			showlegend=True,
			legend_orientation="h"
		)
	)

	return fig


if __name__ == "__main__":
	main()

