import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
data=pd.read_csv("Sample-Superstore.csv", encoding="latin1")
columns=data.columns
index=data.index
new_columns=[]
for column in columns:
    column=column.lower().replace(' ','_')
    new_columns.append(column)
data.columns=new_columns
data["order_date"]=pd.to_datetime(data["order_date"])
data["ship_date"]=pd.to_datetime(data["ship_date"])
data["ship_days"]=(data["ship_date"]-data["order_date"]).dt.days

connection=sqlite3.connect("superstore.db")
data.to_sql("orders", connection, if_exists="replace",index=False)
cursor=connection.cursor()
three_most_profitable_products="select * from( select category,product_name,sum(profit) as total_profit, RANK() over(partition by category order by sum(profit) desc) as product_rank from orders group by category,product_name) where product_rank<=3"
running_total="select order_date,sales,sum(sales) over(order by order_date) as running_total from orders group by order_date order by order_date"
average_sale_category="select category,round(avg(sales),2) as average_sale from orders group by category"


df_3_most_profitable=pd.read_sql(three_most_profitable_products,connection)
df_running_total=pd.read_sql(running_total,connection)
df_running_total['order_date']=pd.to_datetime(df_running_total['order_date'])
df_average_sale_category=pd.read_sql(average_sale_category,connection)
connection.close()

df_running_total.plot(kind="line",title="running total",x="order_date",y="running_total",figsize=(12,6))

categories2=df_average_sale_category["category"].unique()
colors2=["blue","green","orange"]
color_map2=dict(zip(categories2,colors2))
bar_colors2=df_average_sale_category["category"].map(color_map2)
df_average_sale_category.plot(kind="barh",title="average sale category",x="category",y="average_sale", color=bar_colors2)

categories=df_3_most_profitable["category"].unique()
colors=["blue","green","orange"]
color_map=dict(zip(categories,colors))
bar_colors=df_3_most_profitable["category"].map(color_map)
df_3_most_profitable.plot(kind="barh",title="3 most profitable products per category",x="product_name",y="total_profit",color=bar_colors)
plt.show()

