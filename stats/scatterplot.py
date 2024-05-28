# SCATTERPLOT
def scatterplot(df, feature, label, roundto=4, linecolor='darkorange'):
  import pandas as pd
  import matplotlib.pyplot as plt
  import seaborn as sns
  from scipy import stats

  # Create the plot
  sns.regplot(x=df[feature], y=df[label], line_kws={"color":linecolor})

  # Calculate the regression line
  m, b, r, p, err = stats.linregress(df[feature], df[label])
  tau, tp = stats.kendalltau(df[feature], df[label])
  rho, rp = stats.spearmanr(df[feature], df[label])
  fskew = round(df[feature].skew(), roundto)
  lskew = round(df[label].skew(), roundto)

  # Add all of those values into the plot
  textstr = f'y = {round(m, roundto)}x + {round(b, roundto)}\n'
  textstr += f'r = {round(r, roundto)}, p = {round(p, roundto)}\n'
  textstr += f'τ = {round(tau, roundto)}, p = {round(tp, roundto)}\n'
  textstr += f'ρ = {round(rho, roundto)}, p = {round(rp, roundto)}\n'
  textstr += f'{feature} skew = {round(fskew, roundto)}\n'
  textstr += f'{label} skew = {round(lskew, roundto)}'

  plt.text(.95, 0.2, textstr, fontsize=12, transform=plt.gcf().transFigure)
  plt.show()