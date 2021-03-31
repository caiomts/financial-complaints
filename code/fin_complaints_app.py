import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('../raw_data/shortlist.zip', index_col='date_received', parse_dates=True)

'''
# Insight on Financial Complaints
The Consumer Financial Protection Bureau maintain a public dataset with complaints ("complaint_database").
Below we presented a short report that intended raise some insights for an imaginary company that deals with customer 
complaints and offers its service to companies in the financial sector and is looking for new customers.
'''

df_plot1 = df[['complaint_id']].resample('M').count()

# Plot: Complaints per month
fig = px.line(df_plot1.reset_index(), x='date_received', y='complaint_id',
              title='Monthly Complaints', labels={
                                                  'date_received': 'Date',
                                                  'complaint_id': 'Complaints'
                                                  }, height=500, template='simple_white')

st.plotly_chart(fig, use_container_width=True)

'''
As complaints skyrocketed after the coronavirus outbreak, this trend is analyzed per company previously selected. 
'''

# Looking that trend by companies
compl_p_month = df[['complaint_id', 'company_name']].groupby(['company_name']) \
.resample('M').count()['complaint_id'].reset_index()

# Plot: Complaints per month
fig = px.line(compl_p_month, x='date_received', y='complaint_id', color='company_name',
              labels={'company_name': 'Companies',
                      'date_received': 'Date',
                      'complaint_id': 'Complaints'
                      }, height=700, template='simple_white')

fig.update_layout(legend=dict(title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"))

st.plotly_chart(fig, use_container_width=True)


'''
Considering the amount of monthly complaints per company we applied a non-parametric test to slit the companies into 
groups that are statistically similar. Below are presented a boxplot with the first six groups. 
'''

df_bplot = pd.read_json('../tidy_data/df_bpolt.json')

fig = px.box(df_bplot, x='company_name', y='complaint_id', color='group',
             title='Boxplot - Monthly Complaints per Companies', labels={'company_name': 'Companies',
                                                                         'complaint_id': 'Monthly complaints',
                                                                         'group': 'Groups'},
             category_orders={'group': [1, 2, 3, 4, 5, 6]},
             height=700, template='simple_white')

fig.update_layout(legend=dict(title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"))

st.plotly_chart(fig, use_container_width=True)

'''
Now it is clear which companies have the most monthly complaints. But how do these companies deal with due dates?
'''

df_sub7_bplot = pd.read_json('../tidy_data/df_sub7_bplot.json')

df_sub7_bplot['group'] = df_sub7_bplot['group'].astype(str)

fig = px.bar(df_sub7_bplot, x='company_name', y='complaint_id', color='group',
             category_orders={'company_name': df_sub7_bplot.company_name},
             title='Complaints with untimely response per month', labels={'company_name': 'Companies',
                                                                          'complaint_id': 'Monthly complaints',
                                                                          'group': 'Groups'},
             width=800, height=600, template='simple_white')

st.plotly_chart(fig, use_container_width=True)

'''
The list below combines companies that received the most complaints, the most complaints this year, the most complaints 
in which the status is "In progress" or "Untimely response" and finally the companies with the most recurring issues by 
type. 
'''

complaints_per_year = pd.read_csv('../tidy_data/fc_per_y.zip', index_col='company_name')

st.dataframe(complaints_per_year, height=300)

'''
The following is the number of complaints per month of the pre-selected companies.
'''

shortlist_1 = pd.read_csv('../raw_data/shortlist.zip', index_col='date_received', parse_dates=True)

df = shortlist_1.loc[shortlist_1.company_name.isin(complaints_per_year.index.to_list())] \
    .groupby(['company_name']).resample('M').count()['complaint_id'].reset_index()

fig = px.line(df, x='date_received', y='complaint_id', color='company_name',
              labels={'company_name': 'Companies',
                      'date_received': 'Date',
                      'complaint_id': 'Complaints'
                      }, height=700, template='simple_white')

fig.update_layout(legend=dict(title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"))

st.plotly_chart(fig, use_container_width=True)

'''
Three companies are by fair the winners of complaints received and it is clear that, after the coronavirus upheaval, 
their number of complaints skyrocketed.

### What is the average monthly complaints per company? Are these numbers statistically different between companies?
There isn't interest in compare all 31 companies presented so far, due to this we first extracted a subset of companies 
for which the monthly median is bigger than 200 complaints. After that, we pair compared the companies sorted 
by the median and grouped it always when the null hypothesis that two related paired samples come from 
the same distribution was rejected.
'''

df_avg_id = df.groupby(['company_name']).describe().sort_values(by=[('complaint_id',  'mean')], ascending=False)

# subset: only if median > 200 complaints per month
ls = df_avg_id.loc[df_avg_id[('complaint_id',  '50%')] > 200].index.to_list()

conditions = [
    (df['company_name'].isin(ls[0:3])),
    (df['company_name'].isin(ls[3:6])),
    (df['company_name'].isin(ls[6:8])),
    (df['company_name'].isin([ls[8]])),
    (df['company_name'].isin(ls[9:]))
]

groups = list(range(1, 6, 1))

df['group'] = np.select(conditions, groups)

fig = make_subplots(rows=1, cols=2)
fig = px.box(df[df['company_name'].isin(ls[0:8])], x='company_name', y='complaint_id', color='group',
             title='Boxplot - Monthly Complaints per Companies', labels={'company_name': 'Companies',
                                                                         'complaint_id': 'Monthly complaints',
                                                                         'group': 'Groups'},
             category_orders={'company_name': ls[0:8], 'group': [1, 2, 3]},
             width=800, height=600, template='simple_white')

fig.update_layout(legend=dict(title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"))

st.plotly_chart(fig, use_container_width=True)
