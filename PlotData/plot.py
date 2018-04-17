import pandas as pd 
import matplotlib.pyplot as plt
import glob 
import os
import numpy as np

base = '/Users/' # change if using a different computer
folder_base = base + 'yeyilin/desktop/URAP/POS/Data'  # change if using a different computer
allFiles = glob.glob(os.path.join(folder_base, "*.csv"))
df_from_each_file = (pd.read_csv(f) for f in allFiles)
concatenated_df  = pd.concat(df_from_each_file, ignore_index=True)
colors = np.where(concatenated_df.POS > 1, 'r', 'g')
concatenated_df.plot(kind='scatter', x='id', y='POS', s=100, c=colors)
plt.xlabel( "Number of debit cards")
plt.ylabel( "Number of businesses with POS terminal")
plt.show()
