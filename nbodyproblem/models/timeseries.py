import pandas as pd

columns = ['time', 'body', 'x', 'y','vx','vy',"ax","ay"]

# Create an empty DataFrame with the predefined columns
sim_dataseries = pd.DataFrame(columns=columns)
