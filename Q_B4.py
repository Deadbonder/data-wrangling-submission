import matplotlib.pyplot as plt
import pandas as pd

region_units = pd.DataFrame({'region': ['North', 'South', 'East'], 'units': [15, 9, 10]})

plt.bar(region_units['region'], region_units['units'])
plt.title('Units Sold by Region')
plt.xlabel('Region')
plt.ylabel('Units')
plt.show()
