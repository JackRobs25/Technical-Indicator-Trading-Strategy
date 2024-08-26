This project implements a Technical Strategy for trading stocks based on technical indicators. The strategy uses MACD, RSI, and Bollinger Bands to generate trading signals. It is compared against a Baseline Strategy to evaluate its performance.

Components

	1.	get_data(start, end, symbols, column_name="Adj Close", include_spy=True, data_folder="./data"):
	•	Fetches historical stock data for given symbols.
	•	Downloads SPY data and joins it with data for specified symbols.
	2.	TechnicalStrategy Class:
	•	train(*params, **kwparams): Placeholder method for future use; currently does nothing.
	•	test(start_date, end_date, symbol, starting_cash):
	•	Applies technical indicators (MACD, RSI, Bollinger Bands) to generate trading signals.
	•	Returns a DataFrame with trading signals and lists of long and short positions.
	3.	main() Function:
	•	Executes the technical strategy and baseline strategy.
	•	Evaluates both strategies using cumulative returns and other metrics.
	•	Plots cumulative returns and trading signals on a graph.

Technical Indicators

	•	MACD: Uses the Moving Average Convergence Divergence to generate trading signals based on MACD line crossing a signal line.
	•	RSI: Measures the relative strength index to identify overbought or oversold conditions.
	•	Bollinger Bands: Analyzes price volatility using a moving average and standard deviations.

	Trading Signals:
	•	1 for buying (LONG)
	•	0 for holding
	•	-1 for selling (SHORT)
	•	Performance Metrics:
	•	Cumulative Returns (DCR): Overall returns of the strategy.
	•	Average Daily Returns (ADR): Average returns per day.
	•	Standard Deviation (SD): Volatility of returns.
	•	Plots:
	•	Cumulative Returns: Comparison of cumulative returns between the technical strategy and baseline strategy.
	•	Trading Signals: Vertical lines indicating buy (green) and sell (red) signals.
