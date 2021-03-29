import streamlit as st
import pandas as pd
import plotly.express as px

'''
# Financial Complaint Winners
The Consumer Financial Protection Bureau maintain a public dataset with complaints ("complaint_database").
Below we presented a short report that intended raise some insights for an imaginary company that deals with customer 
complaints and offers its services to companies in the financial sector.

## Potential customers
The list below combines companies that received the most complaints, the most complaints this year, the most complaints 
in which the status is "In progress" or "Untimely response" and finally the companies with the most recurring issues by 
type. 
'''

complaints_per_year = pd.read_csv('../tidy_data/fc_per_y.zip', index_col='company_name')

st.dataframe(complaints_per_year, height=300)

'''
The following is the number of complaints per month of the first ten pre-selected companies.
'''

shortlist_1 = pd.read_csv('../raw_data/shortlist.zip', index_col='date_received', parse_dates=True)

df = shortlist_1.loc[shortlist_1.company_name.isin(complaints_per_year.head(10).index.to_list())] \
    .groupby(['company_name']).resample('M').count()['complaint_id']

fig = px.line(df.reset_index(), x='date_received', y='complaint_id', color='company_name',
              title='Monthly Complaints', labels={'company_name': 'Companies',
                                                  'date_received': 'Date',
                                                  'complaint_id': 'Complaints'
                                                  }, width=800, height=600, template='simple_white')

fig.update_layout(legend=dict(title=None, orientation="h", y=1, yanchor="bottom", x=0.7, xanchor="center"))

st.plotly_chart(fig, use_container_width=True)

'''
Three companies are by fair the winners of complaints received and it is clear that, after the coronavirus upheaval, 
their number of complaints skyrocketed.
'''