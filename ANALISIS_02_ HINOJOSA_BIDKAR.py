# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 11:23:35 2021

@author: Bidkar Hinojosa
"""
#Section 1

""""
Agregar modulos a utilizar durante la ejecución del código
Add modules to be used during the execution of the code

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

"""
Abrir la base de datos con la funcion read.csv de pandas para tener un data frame
Open the database with read.csv from pandas to obtain a data frame variable
"""
df = pd.read_csv("C:/Users/101357781/Documents/synergy_logistics_database.csv")

"""
Realizar una columna concatenada para crear la ruta entre origen y destino en un mismo string
Y utilizar la función agg para separar los strings por un '-' 
Realizar nueva columna de mes

Create a concatenated column between origin and destination in the same string
And use agg() to separate the strings with a '-'
Create new column with month info
"""

df["route"] = df[['origin', 'destination', 'transport_mode']].agg('-'.join, axis = 1)
df['date'] = pd.to_datetime(df['date'])
df['month']= pd.DatetimeIndex(df['date']).month

"Filtrar dos datasets uno para importaciones y otro para exportaciones"
"Create two datasets filtered out by imports and exports"

df_import = df[df['direction']== 'Imports']
df_export = df[df['direction']== 'Exports']

"""
Utilizar la función group by para crear dos dataframes: uno con la cuenta de 
cuantas veces se llevó a cabo la ruta y otro con la suma de la columna total_values
y así con la función merge agregar con left join el valor de totales al primer 
data frame con base en la columna route para cada data frame

Utilize the groupby function to create two data frames: One with the count of 
times the route was travelled and another one with the sum of all values of the
route. Then the use merge function to add the total value per route
to the first data frame to have the count and total value per route for bothimports and exports.
"""

df_routes_import = df_import.groupby(['origin','destination','direction', 'route', 'transport_mode'])['route'].count().reset_index(name = 'times_taken').sort_values(by = 'times_taken', ascending = False)
df_routes_value_import = df_import.groupby(['direction','route'])['total_value'].sum().reset_index(name = 'total_value_per_route').sort_values(by = 'total_value_per_route', ascending = False)

df_routes_import_summary = pd.merge(df_routes_import, df_routes_value_import[['route','total_value_per_route']], on = 'route', how= 'left')
df_routes_import_summary = df_routes_import_summary.sort_values(by = 'total_value_per_route', ascending = False)
df_routes_import_summary['cumulative_percentage'] = 100*(df_routes_import_summary.total_value_per_route.cumsum()/ df_routes_import_summary.total_value_per_route.sum())

df_routes_export = df_export.groupby(['origin','destination','direction', 'route', 'transport_mode'])['route'].count().reset_index(name = 'times_taken').sort_values(by = 'times_taken', ascending = False)
df_routes_value_export = df_export.groupby(['direction','route'])['total_value'].sum().reset_index(name = 'total_value_per_route').sort_values(by = 'total_value_per_route', ascending = False)

df_routes_export_summary = pd.merge(df_routes_export, df_routes_value_export[['route','total_value_per_route']], on = 'route', how= 'left')
df_routes_export_summary = df_routes_export_summary.sort_values(by = 'total_value_per_route', ascending = False)
df_routes_export_summary['cumulative_percentage'] = 100*(df_routes_export_summary.total_value_per_route.cumsum()/ df_routes_export_summary.total_value_per_route.sum())

n_routes= 10 

print("These are the Import top routes by appearance: \n", df_routes_import_summary.sort_values(by = 'times_taken', ascending = False)[['route', 'times_taken', 'total_value_per_route']].head(n_routes))

print("These are the Import top routes by value: \n", df_routes_import_summary[['route', 'times_taken', 'total_value_per_route']].head(n_routes))

print("These are the Export top routes by appearance: \n", df_routes_export_summary.sort_values(by = 'times_taken', ascending = False)[['route', 'times_taken', 'total_value_per_route']].head(n_routes))

print("These are the Export top routes by value: \n", df_routes_export_summary[['route', 'times_taken', 'total_value_per_route']].head(n_routes))


#Section 2
"""
Utilizar función group by para crear un data frame con el valor sumado por 
metodo de transporte para importaciones y exportaciones

Utilize group by function to sum total value column per transport mode and 
get top 3 modes printed for imports and exports

"""
df_transport_import = df_import.groupby(['transport_mode'])['total_value'].sum().reset_index(name= 'total_value_per_transport').sort_values(by= 'total_value_per_transport', ascending = False)

df_transport_export = df_export.groupby(['transport_mode'])['total_value'].sum().reset_index(name= 'total_value_per_transport').sort_values(by= 'total_value_per_transport', ascending = False)

print("Top 3 transport modes for Imports: \n", df_transport_import.head(3))

print("Top 3 transport modes for Exports: \n", df_transport_export.head(3))


"""
Graficar para observar tendecias por año de cada transporte
Graph to observe tendecies over the years

"""
df_transport_import_date = df_import.groupby(['year', 'transport_mode'])['total_value'].sum()
df_transport_import_date = df_transport_import_date.to_frame()

sns.lineplot(data = df_transport_import_date, x= 'year', y = 'total_value', hue= 'transport_mode')

df_transport_export_date = df_export.groupby(['year', 'transport_mode'])['total_value'].sum()
df_transport_export_date = df_transport_export_date.to_frame()

sns.lineplot(data = df_transport_export_date, x= 'year', y = 'total_value', hue= 'transport_mode')
plt.show()

#Section 3

"Agrupar por pais de origen y obtener su valor total durante los años y obtener porcentaje cumulativo"
"Group by origin country and its total over all the years with its cumulative percentage"

df_import_country = df_import.groupby(['origin'])['total_value'].sum().reset_index(name = 'total').sort_values(by = 'total', ascending = False)
df_import_country['cumulative_percentage'] = 100*(df_import_country.total.cumsum()/ df_import_country.total.sum())

df_export_country = df_export.groupby(['origin'])['total_value'].sum().reset_index(name = 'total').sort_values(by = 'total', ascending = False)
df_export_country['cumulative_percentage'] = 100*(df_export_country.total.cumsum()/ df_export_country.total.sum())

"Filtrar valores que sean igual o menor a 80% en porcentaje cumulativo"
"Filter values until the 80% mark is met"

df_import_country_80 = df_import_country[df_import_country['cumulative_percentage'] <= 80] 
df_export_country_80 = df_export_country[df_export_country['cumulative_percentage'] <= 80] 

print("The top 80% countries that have more value in Imports are: \n", df_import_country_80)

fig, ax1 = plt.subplots(figsize = (10,6))
ax1 = sns.barplot(x = 'origin', y = 'total', data = df_import_country, palette ='summer')
ax2 = ax1.twinx()
ax2 = sns.lineplot(x = 'origin', y= 'cumulative_percentage', data= df_import_country, color= 'tab:red')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation= 45, horizontalalignment = 'right')
ax2.tick_params(axis = 'y', color= 'tab:red')
ax1.axvline(6.00)
plt.show()

print("The top 80% countries that have more value in Exports are: \n", df_export_country_80)
fig, ax3 = plt.subplots(figsize = (10,6))
ax3 = sns.barplot(x = 'origin', y = 'total', data = df_export_country, palette ='summer')
ax4 = ax3.twinx()
ax4 = sns.lineplot(x = 'origin', y= 'cumulative_percentage', data= df_export_country, color= 'tab:red')
ax3.set_xticklabels(ax3.get_xticklabels(), rotation= 45, horizontalalignment = 'right')
ax3.tick_params(axis = 'y', color= 'tab:red')
ax3.axvline(6.00)
plt.show()


