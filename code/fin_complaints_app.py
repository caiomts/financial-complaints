import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('../raw_data/shortlist.zip', index_col='date_received', parse_dates=True)

'''
# Insights on Financial Complaints
The Consumer Financial Protection Bureau maintain a public dataset with complaints ("complaint_database").
Below we presented a short report that intended to raise some insights for an imaginary company that deals with customer 
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
As complaints skyrocketed after the coronavirus outbreak, this trend is analyzed per company (Those companies were first
shortlisted as the union of the following subsets: 
20 companies with most complaints, 20 companies with most complaints this year, 20 companies with most complaints 
"In progress" or "Untimely response"). 
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
             height=600, template='simple_white')

st.plotly_chart(fig, use_container_width=True)

'''
There is no link between monthly complaints and timely response. In addition, only five companies postpone two or more 
responses per month. 
'''

df_in_prog = pd.read_json('../tidy_data/df_in_prog.json')

df_in_prog['group'] = df_in_prog['group'].astype(str)

fig = px.bar(df_in_prog, x='company_name', y='complaint_id', color='group',
             category_orders={'company_name': df_in_prog.company_name},
             title='Complaints whose status is "In progress"', labels={'company_name': 'Companies',
                                                                       'complaint_id': 'Monthly complaints',
                                                                       'group': 'Groups'},
             height=600, template='simple_white')

st.plotly_chart(fig, use_container_width=True)

'''
However, when we look to complaints with "In progress" status one company with few monthly complaints presents almost 
the same amount in progress - Alliance Data Card Services. Backlog is an interest feature to observe because companies 
that don't present a high monthly complaints might not have capacity to deal with the backlog. Therefore, we present
below the ratio between complaints 'In progress' and monthly median complaints per company.

'''

df_median_prog = df_in_prog.merge(df_bplot.groupby(['group',
                                                    'company_name']).median(),
                                  how='left', on=['company_name'])

df_median_prog.rename(columns={'complaint_id_x': 'In progress', 'complaint_id_y': 'Median',
                      'company_name': 'Company Name', 'group': 'Group'}, inplace=True)
df_median_prog['Complaint ratio'] = df_median_prog['In progress'] / df_median_prog['Median']
df_median_prog.sort_values(by=['Complaint ratio'], ascending=False, inplace=True)

st.dataframe(df_median_prog[['Group', 'Company Name', 'In progress', 'Median', 'Complaint ratio']])

'''
Finally we took a brief look at complaints per product type and companies. "Credit reporting..." is by far the main 
cause of complaints and it is also responsible for the majority of the complaints in Group 1. Among other companies, 
apart the first product, that is also a leader, the companies themselves are less "specialized".
'''

df_prods = pd.read_json('../tidy_data/df_prods.json')

fig = px.bar(df_prods, x='product', y='complaint_id', color='company_name', height=1000, template='simple_white',
             labels={'company_name': 'Companies',
                     'complaint_id': 'Complaints',
                     'product': 'Products'})

fig.update_layout(legend=dict(title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"))

st.plotly_chart(fig, use_container_width=True)

'''
# A possible Shortlist

The group 1 should be in the list because the numbers of monthly complaints are very high and, even if those companies
might have a good customer service, a good price can be a good incentive to outsourcing it. Next, we proposed
include into the list all companies that present a ratio between monthly complaints and complaints in progress bigger 
than 30% because is possible that this companies do not have capacity to reduce this backlog by themselves. Finally,
companies that has more two complaints in average that are solved after the due date. The list is presented below with
the total complaints per year since 2018.
'''

complaints_per_year = pd.read_csv('../tidy_data/fc_per_y.zip', index_col='company_name')

shortlist = list(['EQUIFAX, INC.', 'Experian Information Solutions Inc.', 'Alliance Data Card Services',
                  'WELLS FARGO & COMPANY', 'TRANSUNION INTERMEDIATE HOLDINGS, INC.',
                  'BANK OF AMERICA, NATIONAL ASSOCIATION', 'SYNCHRONY FINANCIAL', 'PNC Bank N.A.'])

df_sl = complaints_per_year[complaints_per_year.index.isin(shortlist)]

st.dataframe(df_sl, height=300)

