import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
### streamlit run app.py ###
st.set_page_config(
    page_title="Electoral Bonds Analysis",
    page_icon="🐼",
    layout="wide",
    initial_sidebar_state="expanded")

# alt.themes.enable("latimes")


df = pd.read_csv('After_ECI.csv')
df['date_of_purchase'] = pd.to_datetime(df['date_of_purchase'], format = 'mixed')
df['date_of_encashment'] = pd.to_datetime(df['date_of_encashment'], format = 'mixed')

def load_home():
    st.title('Hi There, My name is Ark ✨ Welcome you to my website')
    st.subheader("""This Website shows you a Quick Analysis of Electoral Bond Data
released by SBI on the order of Hon'ble Supreme Court""")
    st.image(r'https://images.thequint.com/thequint%2F2019-03%2F53a894ad-faf7-4548-9120-552ec5691831%2Fhero.jpg?rect=0%2C0%2C2000%2C1125&auto=format%2Ccompress&fmt=webp&width=720')
    st.text('If you was living under the rock here is a quick explainer for you')
    st.page_link('https://youtu.be/RJfqzUWZ0Bw?feature=shared',label='YT Video - Click Me !')

def load_pp():
    spc_part_Tfund = df[df['standardised_political_party_name'] == selected_pp]['amount'].sum()
    st.header(f'''A Quick Analysis of {selected_pp}''')

    col1, col2 = st.columns(2)

    with col1:
        labels = selected_pp, 'Others'
        sizes = [spc_part_Tfund, total_funds-spc_part_Tfund]
        explode = (0.1, 0)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)

        st.text(f'{(spc_part_Tfund/total_funds)*100} %')

    with col2:
        st.subheader('Total amount of bond bought')
        st.text(f'{total_funds//10000000} Cr.')

        st.subheader('Money Recived')
        st.text(f'by {selected_pp}')
        st.text(f'{spc_part_Tfund//10000000} Cr.')

    st.divider()
    st.subheader('Top Donar')

    col21, col22 = st.columns((1,1.5),vertical_alignment='center')

    with col21:

        Top10 = df[df['standardised_political_party_name'] == selected_pp].groupby('standardised_purchaser_name')['amount'].sum().sort_values(ascending=False)
        st.dataframe(Top10)

    with col22:
            fig, ax = plt.subplots()
            # ax.bar(Top10.index,Top10.values)
            ax.barh(Top10.head(10).index,Top10.head(10).values)

            st.pyplot(fig)

    st.divider()

    col41, col42, col43, col44 = st.columns(4,vertical_alignment='top')
    with col41:
        data1 = df[df['standardised_political_party_name'] == selected_pp][['date_of_purchase','amount']].groupby('date_of_purchase')['amount'].sum().sort_index()
        st.dataframe(data1)

    with col42:
        st.subheader('Date V/S Amount - Graph')
        st.text('''The bar char represents total amount of bond
    purchased on a specific day''')
        fig2, ax2 = plt.subplots()
        # ax.bar(Top10.index,Top10.values)
        ax2.bar(data1.index.astype(str),data1.values)

        st.pyplot(fig2)

    with col43:
        data2 = df[df['standardised_political_party_name'] == selected_pp][['date_of_purchase','amount']].groupby('date_of_purchase')['amount'].count().sort_index()
        st.dataframe(data2)

    with col44:
        st.subheader('Date V/S No. of Bond - Graph')
        st.text('''The bar char represents total number of bond
    purchased on a specific day''')
        fig3, ax3 = plt.subplots()
        # ax.bar(Top10.index,Top10.values)
        ax3.bar(data2.index.astype(str),data2.values)

        st.pyplot(fig3)

    st.divider()

    col51,col52,col53 = st.columns((2,3,1))

    with col51:
        st.title('Althogh the purpose of this graph is to show the distribution of data but i dont think that its the best way to showcase 🥲')
    with col52:
        dis = df[df['standardised_political_party_name'] == selected_pp].groupby('standardised_purchaser_name')['amount'].sum().quantile([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])

        fig5, ax5 = plt.subplots()
        # ax.bar(Top10.index,Top10.values)
        ax5.bar(dis.index.astype(str),dis.values.round().astype(int).astype(str))
        st.pyplot(fig5)
    with col53:
        st.dataframe(dis)

    st.divider()

    col61,col62,= st.columns((2),vertical_alignment='top')

    with col61:
        st.subheader('Branch where bond was issued')
        st.dataframe(df[df['standardised_political_party_name']==selected_pp].groupby('issue_branch_city')['amount'].count().sort_values(ascending=False))

    with col62:
        st.subheader('Branch where it was rosted')
        st.dataframe(df[df['standardised_political_party_name']==selected_pp].groupby('pay_branch_ciy')['amount'].count())
        i = (df[df['standardised_political_party_name']==selected_pp].groupby('organisation_or_individual')['bond_number'].count()).loc['Individual']
        j = (df[df['standardised_political_party_name']==selected_pp].groupby('organisation_or_individual')['bond_number'].count()).loc['Organisation']
        jj= (df[df['standardised_political_party_name']==selected_pp].groupby('status')['bond_number'].count()).loc['Paid']

        st.subheader(f'Number of bond bought by individual {i}')
        st.subheader(f'Number of bond bought by organisation {j}')
        st.subheader(f'Total number of bonds {jj}')

    st.divider()
def load_donar():
    st.header(f'A Quick Analysis of {selected_donar}')
    d_amount = df.groupby('standardised_purchaser_name')['amount'].sum().loc[selected_donar]
    colb1, colb2 = st.columns(2)

    with colb1:
        labels2 = selected_donar, 'Others'
        sizes = [d_amount, total_funds-d_amount]
        explode = (0.1, 0)

        figb1, axb1 = plt.subplots()
        axb1.pie(sizes, explode=explode, labels=labels2, autopct='%1.1f%%', startangle=90)
        axb1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(figb1)
    with colb2:
        st.subheader('Total amount of bond bought')
        st.text(f'{total_funds//10000000} Cr.')

        st.subheader('Total worth of bond bought')
        st.text(f'by {selected_donar}')
        st.text(f'{d_amount//10000000} Cr.')
    st.divider()
    colb3, colb4 = st.columns(2)
    kkdf = df[df['standardised_purchaser_name'] == selected_donar][['standardised_political_party_name','amount']].groupby('standardised_political_party_name').sum().sort_values(by='amount',ascending=False)
    with colb3:
        st.dataframe(kkdf)
    with colb4:
        fige, axe = plt.subplots()
        axe.barh(kkdf.index,kkdf['amount'])

        st.pyplot(fige)
        
    pass
def load_Overall():
    colc3, colc4 = st.columns(2)
    with colc3:
        doi =df[df['organisation_or_individual']=='Individual'].groupby('standardised_purchaser_name')['amount'].sum().sort_values(ascending=False)
        doo = df[df['organisation_or_individual']=='Organisation'].groupby('standardised_purchaser_name')['amount'].sum().sort_values(ascending=False)
        st.dataframe(doi)
        figc3, axc3 = plt.subplots()
        axc3.barh(doi.head(10).index,doi.head(10).values)

        st.pyplot(figc3)
    with colc4:
        figc2, axc2 = plt.subplots()
        axc2.barh(doo.head(10).index,doo.head(10).values)

        st.pyplot(figc2)
        st.dataframe(doo)
    pass

#####

with st.sidebar:
    st.title('Electoral Bond Data Analysis')
    
    total_funds = df['amount'].sum()
    option = st.selectbox('Choose one of them', ['Select','Overall Analysis','Political Parties','Bond Purchaser'])
if option == 'Select':
    load_home()
elif option == 'Political Parties':
    pp = list(df['standardised_political_party_name'].unique())
    selected_pp = st.sidebar.selectbox('Political Parties', pp)
    load_pp()
    
elif option == 'Bond Purchaser':
    Donar = list(df.groupby('standardised_purchaser_name')['amount'].sum().sort_values(ascending=False).index)
    selected_donar = st.sidebar.selectbox('Bond Purchaser', Donar)
    load_donar()

elif option == 'Overall Analysis':
    load_Overall()


