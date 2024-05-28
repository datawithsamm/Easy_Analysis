# BAR CHART
def bar_chart(df, feature, label, roundto=4, p_threshold=0.05, sig_ttest_only=True):
  import pandas as pd
  import matplotlib.pyplot as plt
  import seaborn as sns
  from scipy import stats

  # Make sure that the feature is categorical and label is numeric
  if pd.api.types.is_numeric_dtype(df[feature]):
    num = feature
    cat = label
  else:
    num = label
    cat = feature

  # Create the bar chart
  sns.barplot(x=df[cat], y=df[num])

  # Create the numeric lists needed to calcualte the ANOVA
  groups = df[cat].unique()
  group_lists = []
  for g in groups:
    group_lists.append(df[df[cat] == g][num])

  f, p = stats.f_oneway(*group_lists) # <- same as (group_lists[0], group_lists[1], ..., group_lists[n])

  # Calculate individual pairwise t-test for each pair of groups
  ttests = []
  for i1, g1 in enumerate(groups):
    for i2, g2 in enumerate(groups):
      if i2 > i1:
        list1 = df[df[cat]==g1][num]
        list2 = df[df[cat]==g2][num]
        t, tp = stats.ttest_ind(list1, list2)
        ttests.append([f'{g1} - {g2}', round(t, roundto), round(tp, roundto)])

  # Make a Bonferroni correction -> adjust the p-value threshold to be 0.05 / n of ttests
  bonferroni = p_threshold / len(ttests)

  # Create textstr to add statistics to chart
  textstr = f'F: {round(f, roundto)}\n'
  textstr += f'p: {round(p, roundto)}\n'
  textstr += f'Bonferroni p: {round(bonferroni, roundto)}'
  for ttest in ttests:
    if sig_ttest_only:
      if ttest[2] <= bonferroni:
        textstr +=f'\n{ttest[0]}: t:{ttest[1]}, p:{ttest[2]}'
    else:
      textstr +=f'\n{ttest[0]}: t:{ttest[1]}, p:{ttest[2]}'

  # If there are too many feature groups, print x labels vertically
  if df[feature].nunique() > 7:
    plt.xticks(rotation=90)

  plt.text(.95, 0.10, textstr, fontsize=12, transform=plt.gcf().transFigure)
  plt.show()