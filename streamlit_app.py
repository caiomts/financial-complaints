import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv('./raw_data/shortlist.zip', index_col='date_received', parse_dates=True)

st.markdown(
    """<a style='display: block; text-align: right;'>A Web App by </a>
    <a style='display: block; text-align: right;' 
    href="https://github.com/caiomts/financial-complaints">Caio Mescouto</a>
    """,
    unsafe_allow_html=True,
)

colors = {'1':'#b2182b', '2': '#ef8a62', '3': '#fddbc7', '4': '#d1e5f0', '5': '#67a9cf', '6': '#2166ac'}

'''
# Insights on Financial Complaints

The **Consumer Financial Protection Bureau** maintains a public dataset with microdata of complaints against financial 
institutions. The following is a brief interactive report to raise some insights for an imaginary company that deals 
with customer complaints and offers its service to companies in the financial sector and is looking for new customers.
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
As complaints skyrocketed after the coronavirus outbreak, this trend is analyzed per companies.  
  
*These companies were first shortlisted as the union of the following subsets: 
20 companies with most complaints, 20 companies with most complaints this year (2021), 20 companies with most complaints 
"In progress" or "Untimely response"*. 
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
It is clear that three companies pushed the trend.  
   
In the sequence a non-parametric test was applied to slip the companies into groups that the distribution are statistically different (p<0.05), 
as presented in the chart below for the first six groups. 
'''

df_bplot = pd.read_json('./tidy_data/df_bpolt.json')

fig = px.box(df_bplot, x='company_name', y='complaint_id', color='group',
             title='Boxplot - Monthly Complaints per Companies', labels={'company_name': 'Companies',
                                                                         'complaint_id': 'Monthly complaints',
                                                                         'group': 'Groups'},
             color_discrete_map={1:'blue', 2: 'red', 3: 'green', 4: 'yellow', 5: 'purple', 6: 'pink'},
             category_orders={'group': [1, 2, 3, 4, 5, 6]},
             height=700, template='simple_white')

fig.update_layout(legend=dict(title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"))

st.plotly_chart(fig, use_container_width=True)

'''
Now it is clear which companies have the most monthly complaints. But how do these companies deal with deadlines?
'''

df_sub7_bplot = pd.read_json('./tidy_data/df_sub7_bplot.json')

df_sub7_bplot['group'] = df_sub7_bplot['group'].astype(str)

fig = px.bar(df_sub7_bplot, x='company_name', y='complaint_id', color='group',
             category_orders={'company_name': df_sub7_bplot.company_name},
             title='Average delayed responses per month', labels={'company_name': 'Companies',
                                                                          'complaint_id': 'Monthly complaints',
                                                                          'group': 'Groups'},
             color_discrete_map=colors,
             height=600, template='simple_white')

st.plotly_chart(fig, use_container_width=True)

'''
There is no clear link between monthly complaints and timely response. 
In addition, only five companies delayed two or more responses per month.  
  
However, how many complaints are still in progress? 
'''

df_in_prog = pd.read_json('./tidy_data/df_in_prog.json')

df_in_prog['group'] = df_in_prog['group'].astype(str)

fig = px.bar(df_in_prog, x='company_name', y='complaint_id', color='group',
             category_orders={'company_name': df_in_prog.company_name},
             title='Complaints whose status is "In progress"', labels={'company_name': 'Companies',
                                                                       'complaint_id': 'Monthly complaints',
                                                                       'group': 'Groups'},
             color_discrete_map=colors,
             height=600, template='simple_white')

st.plotly_chart(fig, use_container_width=True)

'''
Looking at complaints with "In progress" status companies with few monthly complaints present almost 
the same amount in progress. Backlog is an interesting feature to observe because companies 
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
Finally, we took a brief look at complaints per product type and companies. As noted below, "Credit reporting..." 
is by far the main cause of complaints and it is also responsible for the majority of complaints in Group 1. 
Among other companies, apart the first product, that is also a leader, the companies themselves are less "specialized".
'''

df_prods = pd.read_json('./tidy_data/df_prods.json')

fig = px.bar(df_prods, x='company_name', y='complaint_id', color='product', height=800, template='simple_white',
             labels={'company_name': 'Companies',
                     'complaint_id': 'Complaints',
                     'product': 'Products'})

fig.update_layout(legend=dict(title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"))

st.plotly_chart(fig, use_container_width=True)

'''
# A possible Shortlist

Business strategy and other assumptions play a key role here, thus shortlists rely on them. Since we don't have 
information on strategy or other assumptions, the list below is just one possibility. And you? Driven by these
data, would you suggest another one?

  
### My suggestion
(1) The group 1 should be on the list because the numbers of monthly complaints are very high and, even though 
those companies may have a good customer service, a good price can be an incentive to outsource it. (2) Next, I proposed
to include in the list all companies that have a ratio between monthly complaints and complaints in progress bigger 
than 30% because it is possible that these companies are not able to reduce this backlog on their own. (3) Finally,
companies that have more than two complaints, on average, that are solved after the deadline.  
*My shortlist is presented below with the total complaints per year since 2018.*
'''

complaints_per_year = pd.read_csv('./tidy_data/fc_per_y.zip', index_col='company_name')

shortlist = list(['EQUIFAX, INC.', 'Experian Information Solutions Inc.', 'Alliance Data Card Services',
                  'WELLS FARGO & COMPANY', 'TRANSUNION INTERMEDIATE HOLDINGS, INC.',
                  'BANK OF AMERICA, NATIONAL ASSOCIATION', 'SYNCHRONY FINANCIAL', 'PNC Bank N.A.'])

df_sl = complaints_per_year[complaints_per_year.index.isin(shortlist)]

st.dataframe(df_sl)

