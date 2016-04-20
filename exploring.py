#For the second question (household income and family type vs financial aid), use HHT (family type) and HINCP (household income) in college data set, ???_DEBT_MDN in the community survey possibly. Not fully sure, so look it up. 

import sqlite3
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
from collections import defaultdict as dd

# Sign into plotly
py.sign_in("tfbbt8", "Chevroletz71")

# Database
school_conn = sqlite3.connect('school/database.sqlite')
school_cursor = school_conn.cursor()

survey_conn = sqlite3.connect('database.sqlite')
survey_cursor = survey_conn.cursor()

# Pct of students at a school within each income bracket
# cursor.execute('''
#     select INC_PCT_LO, INC_PCT_M1, INC_PCT_M2, INC_PCT_H1, INC_PCT_H2 from scorecard where
#     	INC_PCT_LO != 'PrivacySuppressed' and INC_PCT_LO != '' and
#     	INC_PCT_M1 != 'PrivacySuppressed' and INC_PCT_LO != '' and
#     	INC_PCT_M2 != 'PrivacySuppressed' and INC_PCT_LO != '' and
#     	INC_PCT_H1 != 'PrivacySuppressed' and INC_PCT_LO != '' and
#     	INC_PCT_H2 != 'PrivacySuppressed' and INC_PCT_LO != ''
#     ''')

# School, state, average family income, average in-state tuition
school_cursor.executescript('''
	select instnm, stabbr, faminc, md_faminc, tuitionfee_in from scorecard where
		faminc != '' and faminc != 'PrivacySuppressed' and md_faminc != ''  and
		md_faminc != 'PrivacySuppressed' and tuitionfee_in != '' and tuitionfee_in
		!= 'PrivacySuppressed';
	''')

school_rows = school_cursor.fetchall()

# Iterate over school stats by state
school_avg_income = dd(float) #avg income by state in school set
school_avg_tuition = dd(float) #average tution in state from school set
school_count = dd(float)
school_income_ratio = dd(float)
for row in school_rows:
	school_avg_income[row[1]] += row[2]
	school_avg_tuition[row[1]] += row[4]
	school_count[row[1]] += 1

# Avg income per state
for key, value in school_avg_tuition.items():
	value /= school_count[key]

# Avg income per state
for key, value in school_avg_income.items():
	value /= school_count[key]

school_conn.close()

survey_cursor.executescript('''
	select st, fes, fincp from survey where
		st != '' and st != 'PrivacySuppressed' and fes != ''  and
		fes != 'PrivacySuppressed' and fincp != '' and fincp !=
		'PrivacySuppressed';
	;
	''')

survey_rows = survey_cursor.fetchall()

survey_avg_income
for row in survey_rows:
	print(row[0])

# for key in school_avg_income:
# 	school_income_ratio[key] = school_avg_tuition[key] / school_avg_income[key]

# print(school_income_ratio)

# # Create dataframe with panda
# df = pd.DataFrame([[ij for ij in i] for i in rows])
# df.rename(columns={0: 'Session', 1: 'Student ID', 2: 'Exercise', 3: 'Activity', \
#         4: 'Start', 5: 'End', 6: 'Idle', 7: 'Mouse Wheel', 8: 'Wheel Click', \
#         9: 'Left Click', 10: 'Right Click', 11: 'Mouse Movement', 12: 'Keystroke'}, inplace=True)
# #df = df.sort_values(by=['Start'], ascending=[True])

# user_id = df['Student ID']

# trace1 = Scatter(
#     x=df['Left Click'],
#     y=df['Right Click'],
#     text=user_id,
#     mode='markers'
# )
# layout = Layout(
#     title='Left Mouse Click vs Right Mouse Click',
#     xaxis=XAxis(title='Left Mouse Click'),
#     yaxis=YAxis(title='Right Mouse Click'),
# )
# data = Data([trace1])
# fig = Figure(data=data, layout=layout)
# py.iplot(fig, filename='comparison')