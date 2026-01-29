[![Streamlit App](https://img.shields.io/badge/Live%20App-Streamlit-brightgreen)](https://stock-strategy-analyzer-d2ydkg7lkpkslrflktp8qc.streamlit.app/)

🔗 **Live App:** https://stock-strategy-analyzer-d2ydkg7lkpkslrflktp8qc.streamlit.app/


📊 Stock Strategy Analyzer
A Smarter Way to Read Markets
Look, I built this because I got tired of the same old story: someone builds a fancy ML model, backtests show amazing returns, then it completely falls apart in live trading. Sound familiar?
The problem isn't the models or the data—it's that markets change. What works in a bull run gets destroyed in a choppy sideways market. Instead of fighting this reality, I decided to work with it.

🤔 What's Different Here?
This isn't another "predict tomorrow's closing price" project. Those rarely work, and here's why:

Markets shift between different behavioral states
What worked last month might be suicide this month
Most systems don't know when to just... stop trading

So I built something different:

Instead of predicting prices, understand the game you're playing.

This system figures out what kind of market we're in right now, tells you which strategies make sense, and—most importantly—warns you when the smart move is to sit on your hands.

🎯 The Three Market Personalities
Think of markets like weather patterns. You don't wear the same clothes in summer and winter, right? Same logic here:
What's HappeningWhat It MeansWhat Works🟢 TrendingMarket's got momentum and directionRide the wave, follow the trend🟡 MixedMarket can't make up its mindBe cautious, maybe sit this one out🔴 Mean-RevertingBouncing around in a rangeBuy low, sell high (the classic)
The system uses unsupervised learning to figure out which personality the market is showing based on actual behavior patterns—not just price movement.

🔧 Under the Hood
Here's the workflow:

Pull real NIFTY 50 data (because fake data teaches you nothing)
Calculate features that actually matter—volatility, trend strength, trading ranges
Let clustering algorithms find natural patterns in market behavior
Translate those patterns into practical strategy guidance
Show you the regime history so you can see transitions coming
Package it all into a clean report
Make it interactive through a Streamlit dashboard

This is meant to be a thinking tool, not a magic button that spits out trade signals.

💻 The Dashboard
Built a simple Streamlit interface that shows you:

What regime we're in right now
How confident the system is about that call
Historical regime changes (so you can see patterns)
Which strategies fit the current environment
Honest explanations of why other approaches won't work right now
A downloadable report for your records

I deliberately kept it conservative. No flashy "BUY NOW" buttons. Just clear-headed analysis.

🛠️ Built With

Python (obviously)
Pandas & NumPy for data wrangling
Scikit-learn for the ML pieces
Matplotlib for visualizations
Streamlit for the web interface
yfinance to grab real market data


⚠️ Real Talk
This is an educational project. I built it to learn and share what I learned.
It's not giving you financial advice. It's not predicting the future. It's a framework for thinking more clearly about market conditions. Use it to learn, experiment, understand—but make your own decisions with your own money.

👋 About Me
Pranit Mehta
I like making sense of messy data, especially when it comes to markets. This project sits at the intersection of data science, market behavior, and practical ML—three things I find genuinely interesting.
If you've got questions or ideas, feel free to reach out.





