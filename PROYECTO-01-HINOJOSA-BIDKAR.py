# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 13:35:39 2021
@author: Bidkar Hinojosa Leal
"""

from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches
import pandas as pd 

#Sección de LogIn

"""
Establecí un nombre de usuario y contraseña unica para que se pueda correr el programa. 
Usuario = emtech123
Contraseña = proyectofinal
El código va a correr hasta que el usuario Y contraseña sean correctos

"""

user = None
password = None

"""
Se utilizo un if statement para mostrar si el usuario se equivocó en valores
de ingreso.
"""
while user != "emtech123" and password != "proyectofinal":
    user = input("Ingrese su usuario:")
    password = input("Ingrese su contraseña:")
    if user != "emtech123" or password != "proyectofinal":
     print("El nombre de usuario y/o contraseña son incorrectos. Intente de nuevo")
    else: 
     print("Su usuario y contraseña son correctos. Bienvenido.")


#Sección 1

""""
Transformar listas en data frames para simplicidad de cálculos
Se utilizaron data frames de pandas para utilizar funciones de 
groupby que se asemejan a SQL y R 
"""
df_products = pd.DataFrame(lifestore_products, columns = ['id_product', 'name', 'price', 'category', 'stock'])
df_sales = pd.DataFrame(lifestore_sales, columns = ['id_sale', 'id_product', 'score', 'date', 'refund'])
df_searches = pd.DataFrame(lifestore_searches, columns = ['id_search', 'id_product'])

df_products.dtypes
df_sales.dtypes
df_searches.dtypes

"Agregar columnas de nombre y categoria a ventas y busquedas para próximos calculos"
df_sales = pd.merge(df_sales, df_products[['id_product', 'name', 'category']], on = 'id_product', how= 'left')
df_searches = pd.merge(df_searches, df_products[['id_product', 'name', 'category']], on = 'id_product', how= 'left')

"Hacer agrupamiento y organiza data frame para mostrar productos con mas ventas"
sales_per_product = df_sales.groupby(['id_product','name'])['id_product'].count().reset_index(name = 'total_sales').sort_values(by = 'total_sales', ascending = False)

"Ingresar número de elementos a imprimir"
n_sales=int(input("Ingresa el número de productos con mayores ventas que desea observar:"))

print(sales_per_product.head(n_sales))


"Hacer agrupamiento por producto para obtener busquedas totales y ordenar de mayor a menor"
searches_per_product = df_searches.groupby(['id_product','name'])['id_product'].count().reset_index(name = 'total_searches').sort_values(by = 'total_searches', ascending = False)

"Ingresar número de elementos a mostrar"
n_searches = int(input("Ingresa el número de productos con mayores busquedas que desea observar:"))
print(searches_per_product.head(n_searches))


"Agrupar categorias y productos con su cuenta de ventas"
sales_per_category_product =   df_sales.groupby(['id_product', 'category'])['id_product'].count().reset_index(name = 'total_sales').sort_values(by = 'total_sales', ascending = False)

"Input para ingresar valores a filtrar por categoria"
n_sales_category = int(input("Ingresa número de productos por grupo a observar:"))

"Mostrar 5 menores productos vendidos por categoria"
sales_per_category_product2= sales_per_category_product.sort_values(['category', 'total_sales'], ascending = True).groupby('category').head(n_sales_category)
print("Aquí se muestran los Top 5 productos por categoria con menos ventas:")
print(sales_per_category_product2)

"Hacer agrupamiento por producto y categoria y contar busquedas"
searches_per_category_product =   df_searches.groupby(['id_product', 'category'])['id_product'].count().reset_index(name = 'total_searches').sort_values(by = 'total_searches', ascending = True)

"Input para ingresar numeros de productos por categoria a observar"
n_searches_category = int(input("Ingresa número de productos por grupo a observar:"))

"Mostrar 10 menores productos buscados por categoria"
searches_per_category_product2 = searches_per_category_product.sort_values(['category', 'total_searches'], ascending = True).groupby('category').head(n_searches_category)
print("Aquí se muestran los Top 5 productos por categoria con mas ventas:")
print(searches_per_category_product2)

#Sección 2

"Filtrar procutos sin reseña"
df_sales_filtered = df_sales.loc[df_sales['score'] != 0]

"Obtener promedios de cada producto"
score_per_product = pd.DataFrame(df_sales_filtered.groupby(['id_product', 'name'])['score'].mean())
score_per_product = score_per_product.round({'score' : 2})

"Ingresar número de productos con mejor valoración a observar"
n_highest_score = int(input("Ingresa número de productos por grupo a observar:"))

"Mostrar los productos con mejor reseña"
print("Aqui se muestran los productos con mejor valoración:")
print(score_per_product.sort_values(by= 'score', ascending = False).head(n_highest_score))

"Ingresar número de productos con menor valoración a observar"
n_lowest_score = int(input("Ingresa número de productos por grupo a observar:"))
print("Aqui se muestran los productos con peor valoración:")
print(score_per_product.sort_values(by= 'score', ascending = True).head(n_lowest_score))

#Sección 3

"Agregar nuevas columnas con el mes y año que fueron realizadas las ventas."

df_sales_new = df_sales
df_sales_new['date'] = pd.to_datetime(df_sales_new['date'])
df_sales_new['month']= pd.DatetimeIndex(df_sales_new['date']).month
df_sales_new['year']= pd.DatetimeIndex(df_sales_new['date']).year

"Obtener promedio mensual de número de ventas"

average_sales = round(len(df_sales_new) / 12, 2)
print("El numero de ventas por mes es de:", average_sales)

"Hacer un join para obtener precio del producto vendido"
df_sales_new = pd.merge(df_sales_new, df_products[['id_product','price']], on = 'id_product', how= 'left')

"Obtener promedio mensual de número de ingresos"
average_income = round(df_sales_new['price'].sum() / 12, 2)
print("El ingreso promedio por mes es de: ", average_income)

"Obtener total de ingresos y ventas del año"
total_sales = len(df_sales_new)
total_income = df_sales_new['price'].sum()
print("El total de ventas del año fue de: ", total_sales, "\nEl total de ingresos del año fue de: ", total_income)

"Agrupar por numero de ventas"
months_sales = df_sales_new.groupby(['month'])['month'].count().reset_index(name = 'no_sales').sort_values(by = 'no_sales', ascending = False)

"Mostrar meses con mas ventas"
n_months = int(input("Ingresar número de meses a observar con más ventas: "))
months_sales = months_sales.head(n_months)
print("Los meses con más ventas son: \n", months_sales)









