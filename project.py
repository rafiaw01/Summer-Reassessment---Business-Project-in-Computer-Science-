import pandas as pd
import streamlit as st
import plotly.express as px
import os
import warnings 
warnings.filterwarnings('default')


# The initial task is to Setup the Page Title of the Web App

st.set_page_config(page_title="Euro Bike Sale", page_icon=":office_worker:",layout="wide")

# The next step is to assign title 

st.title(" :office_worker: Euro Bike")

# The app needs to be tailored using HTML and CSS the following code adds the functionality

st.markdown('<style>div.block-container{padding-top: 1rem;padding-bottom: 0rm;margin-top: 1rem}</style>',unsafe_allow_html=True)

# A tab has to be created so that the user can upload the Sales Data CSV File 

f1  = st.file_uploader(":door: Kindly Uplaod File here",type = (["csv","xlsx"]))

if f1 is not None:
    data_file = f1.name
    st.write(data_file)
    df = pd.read_csv(data_file)
    

#The next step isto utilize the data to create a dashboard
    
col1, col2 = st.columns((2))
df["Date"] = pd.to_datetime(df["Date"])

# The next step is to arrange the data using max and min dates 

Starting_Date = pd.to_datetime(df["Date"]).min()
End_Date = pd.to_datetime(df["Date"]).max()

# The columns have to be assigned with a value now

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date",Starting_Date))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", End_Date))

df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()


# Once the Intial Design of Web app has been established next is using the data 
# A sidebar has to be created for categroized data analysis

st.sidebar.header("Kindly chose your filter: ")

# Once Sidebar has been created additional conditions have to be implemented 


# Creating a filter for Country 

Country = st.sidebar.multiselect("Kindly Pick your Country", df["Country"].unique())
if not Country:
    df2 = df.copy()
else:
    df2 = df[df["Country"].isin(Country)]


# Creating a filter for State 

State = st.sidebar.multiselect("Kindly Pick your State", df2["State"].unique())
if not State:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(State)]

# Creating a filter for Gender
Gender = st.sidebar.multiselect("Kindly Pick your Gender", df3["Customer_Gender"].unique())
if not Gender:
    df4 = df3.copy()
else:
    df4 = df3[df3["Customer_Gender"].isin(Gender)]
    

# Once Selection has been made the data has to be categorized further 
#Country State Gender
#Region State City
if not Country and not State and not Gender:
    selected_df = df
elif not State and not Gender:
    selected_df = df[df["Country"].isin(Country)]
elif not Country and not Gender:
    selected_df = df[df["State"].isin(State)]
elif State and Gender:
    selected_df = df3[df["State"].isin(State) & df3["Customer_Gender"].isin(Gender)]
elif Country and Gender:
    selected_df = df3[df["Country"].isin(Country) & df3["Customer_Gender"].isin(Gender)]
elif Country and State:
    selected_df = df3[df["Country"].isin(Country) & df3["State"].isin(State)]
elif Gender:
    selected_df = df3[df3["Customer_Gender"].isin(Gender)]
else:
    selected_df = df3[df3["Country"].isin(Country) & df3["State"].isin(State) & df3["City"].isin(Gender)]

chosen_df = selected_df.groupby(by = ["Sub_Category"], as_index = False)["Revenue"].sum()

with col1:
    st.subheader("Category and Revenue")
    figure = px.bar(chosen_df, x = "Sub_Category" , y = "Revenue", text = ['${:,.2f}'.format(x) for x in chosen_df["Revenue"]],
                    template="seaborn")
    st.plotly_chart(figure,use_container_width=True, height = 200)


    
cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("View_Data"):
        st.write(chosen_df.style.background_gradient(cmap="Blues"))
        csv = chosen_df.to_csv(index = False).encode('utf-8')
        st.download_button("Click to Download Data", data = csv, file_name= "chosen_df.csv",mime ="text/csv", help = " Click to download file ")


# Scatter Plot Revenue-Profit-Order_Quantity
scttr_plot = px.scatter(df, x = "Revenue", y = "Profit", size = "Order_Quantity")
scttr_plot['layout'].update(title="Plot for Revenue-Profit & Order-Quantity",
                       titlefont = dict(size=20),xaxis = dict(title="Revenue",titlefont=dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(scttr_plot,use_container_width=True)

# Scatter Plot Revenue-Profit-Unit_Cost
scttr_plot = px.scatter(df, x = "Revenue", y = "Profit", size = "Unit_Cost")
scttr_plot['layout'].update(title="Plot for Revenue-Profit & Unit-Cost",
                       titlefont = dict(size=20),xaxis = dict(title="Revenue",titlefont=dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(scttr_plot,use_container_width=True)




# Creating a Tree Map
st.subheader("Revenue Tree Map")
tree_map = px.treemap(df, path = ["Country","State","Sub_Category"], values = "Revenue",hover_data = ["Revenue"],
                  color = "Sub_Category")
tree_map.update_layout(width = 900, height = 700)
st.plotly_chart(tree_map, use_container_width=True)