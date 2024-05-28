# BIVARIATE
def bivariate(df, label, roundto=4):
  import pandas as pd
  from scipy import stats
  from stats.scatterplot import scatterplot
  from stats.bar_chart import bar_chart
  from stats.crosstab import crosstab

  output_df = pd.DataFrame(columns=['missing %', 'skew', 'type', 'unique', 'p', 'r', 'τ', 'ρ', 'y = m(x) + b', 'F', 'X2'])

  for feature in df:

    if feature != label:
      # Calculate stats that apply to all data types
      df_temp = df[[feature, label]].copy()
      df_temp = df_temp.dropna().copy()
      missing = round((df.shape[0] - df_temp.shape[0]) / df.shape[0], roundto) * 100
      dtype = df_temp[feature].dtype
      unique = df_temp[feature].nunique()

      if pd.api.types.is_numeric_dtype(df[feature]) and pd.api.types.is_numeric_dtype(df[label]):
        # Process N2N relationships
        m, b, r, p, err = stats.linregress(df_temp[feature], df_temp[label])
        tau, tp = stats.kendalltau(df_temp[feature], df_temp[label])
        rho, rp = stats.spearmanr(df_temp[feature], df_temp[label])
        skew = round(df[feature].skew(), roundto)
        output_df.loc[feature] = [f'{missing}%', skew, dtype, unique, round(p, roundto), round(r, roundto), round(tau, roundto),
                                  round(rho, roundto), f"y = {round(m, roundto)}x + {round(b, roundto)}", '-', '-']
        scatterplot(df_temp, feature, label)

      elif not pd.api.types.is_numeric_dtype(df_temp[feature]) and not pd.api.types.is_numeric_dtype(df_temp[label]):
        # Process C2C relationships
        contingency_table = pd.crosstab(df_temp[feature], df_temp[label])
        X2, p, dof, expected = stats.chi2_contingency(contingency_table)
        output_df.loc[feature] = [f'{missing}%', '-', dtype, unique, p, '-', '-', '-', '-', '-', X2]
        crosstab(df_temp, feature, label)

      else:
        # Process C2N and N2C relationships
        if pd.api.types.is_numeric_dtype(df_temp[feature]):
          skew = round(df[feature].skew(), roundto)
          num = feature
          cat = label
        else:
          skew = '-'
          num = label
          cat = feature

        groups = df_temp[cat].unique()
        group_lists = []
        for g in groups:
          group_lists.append(df_temp[df_temp[cat] == g][num])

        f, p = stats.f_oneway(*group_lists)
        output_df.loc[feature] = [f'{missing}%', skew, dtype, unique, round(p, roundto), '-', '-', '-', '-', round(f, roundto), '-']
        bar_chart(df_temp, cat, num)

  return output_df.sort_values(by=['p'], ascending=True)