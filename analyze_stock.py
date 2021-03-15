from analyze_figure_1 import figure_1
from analyze_figure_2 import figure_2
from analyze_figure_3 import figure_3
from analyze_metrics import metrics


# pick the stock that you want to analyze
ticker = "CRSP"

# if you want to save the file locally, change this to True
save = False

figure_1(stock = ticker, save = save)

figure_2(stock = ticker, save = save)

figure_3(stock = ticker, save = save)

metrics_df = metrics(stock = ticker, save = save)