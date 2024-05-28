# UNIVARIATE
def univariate(df):
  import pandas as pd
  import seaborn as sns
  import matplotlib.pyplot as plt

  df_output = pd.DataFrame(columns=['type', 'missing', 'unique', 'min', 'q1', 'median',
                                    'q3', 'max', 'mode', 'mean', 'std', 'skew', 'kurt'])

  for col in df:
    # Features that apply to all dtypes
    missing = df[col].isna().sum()
    unique = df[col].nunique()
    mode = df[col].mode()[0]
    if pd.api.types.is_numeric_dtype(df[col]):
      # Features for numeric only
      min = df[col].min()
      q1 = df[col].quantile(0.25)
      median = df[col].median()
      q3 = df[col].quantile(0.75)
      max = df[col].max()
      mean = df[col].mean()
      std = df[col].std()
      skew = df[col].skew()
      kurt = df[col].kurt()
      df_output.loc[col] = ["numeric", missing, unique, min, q1, median, q3, max, mode,
                            round(mean, 2), round(std, 2), round(skew, 2), round(kurt, 2)]
      sns.histplot(data=df, x=col)
      plt.show()
    else:
      df_output.loc[col] = ["categorical", missing, unique, '-', '-', '-', '-', '-',
                            mode, '-', '-', '-', '-']
      sns.countplot(data=df, x=col)
      plt.show()
  return df_output