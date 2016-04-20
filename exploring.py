import sqlite3
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
from collections import defaultdict as dd

states = {} #dd(str)
states['01'] = 'AL'
states['02'] = 'AK'
states['04'] = 'AZ'
states['05'] = 'AR'
states['06'] = 'CA'
states['08'] = 'CO'
states['09'] = 'CT'
states['10'] = 'DE'
states['11'] = 'DC'
states['12'] = 'FL'
states['13'] = 'GA'
states['15'] = 'HI'
states['16'] = 'ID'
states['17'] = 'IL'
states['18'] = 'IN'
states['19'] = 'IA'
states['20'] = 'KS'
states['21'] = 'KY'
states['22'] = 'LA'
states['23'] = 'ME'
states['24'] = 'MD'
states['25'] = 'MA'
states['26'] = 'MI'
states['27'] = 'MN'
states['28'] = 'MS'
states['29'] = 'MO'
states['30'] = 'MT'
states['31'] = 'NE'
states['32'] = 'NV'
states['33'] = 'NH'
states['34'] = 'NJ'
states['35'] = 'NM'
states['36'] = 'NY'
states['37'] = 'NC'
states['38'] = 'ND'
states['39'] = 'OH'
states['40'] = 'OK'
states['41'] = 'OR'
states['42'] = 'PA'
states['44'] = 'RI'
states['45'] = 'SC'
states['46'] = 'SD'
states['47'] = 'TN'
states['48'] = 'TX'
states['49'] = 'UT'
states['50'] = 'VT'
states['51'] = 'VA'
states['53'] = 'WA'
states['54'] = 'WV'
states['55'] = 'WI'
states['56'] = 'WY'

def get_st_abbr(state_cd):
	return states[str(state_cd)]

def get_key_in_map(key):
	for k in states:
		if states[k] == key:
			return True;
	return False

# Sign into plotly
py.sign_in("tfbbt8", "Chevroletz71")

# Database
school_conn = sqlite3.connect('school/database.sqlite')
school_cursor = school_conn.cursor()

# School, state, average family income, average in-state tuition
school_cursor.execute('''
	select instnm, stabbr, faminc, md_faminc, tuitionfee_in, avgfacsal, debt_mdn from scorecard where
		faminc != '' and faminc != 'PrivacySuppressed' and md_faminc != ''  and
		md_faminc != 'PrivacySuppressed' and tuitionfee_in != '' and tuitionfee_in
		!= 'PrivacySuppressed' and avgfacsal != '' and avgfacsal != 'PrivacySuppressed' and
		avgfacsal > 0 and debt_mdn != '' and debt_mdn != 'PrivacySuppressed' and debt_mdn > 0;
	''')

school_rows = school_cursor.fetchall()

# Iterate over school stats by state
school_avg_income = dd(float) #avg income by state in school set
school_avg_tuition = dd(float) #average tution in state from school set
school_count = dd(float)
school_income_ratio = dd(float)
for row in school_rows:
	school_avg_income[row[1]] += row[2]
	school_avg_tuition[row[1]] += row[6]*12
	school_count[row[1]] += 1

# Avg income per state
for key in school_avg_tuition:
	school_avg_tuition[key] /= school_count[key]

survey_conn = sqlite3.connect('database.sqlite')
survey_cursor = survey_conn.cursor()

survey_cursor.execute('''
	select st, fes, fincp from survey where
		st != '' and st != 'PrivacySuppressed' and fes != ''  and
		fes != 'PrivacySuppressed' and fincp != '' and fincp !=
		'PrivacySuppressed';
	''')

survey_rows = survey_cursor.fetchall()

survey_avg_income = dd(float)
survey_count = dd(float)
for row in survey_rows:
	survey_avg_income[get_st_abbr(row[0])] += row[2]
	survey_count[get_st_abbr(row[0])] += 1

for key in survey_avg_income:
	survey_avg_income[key] /= survey_count[key]

# Calculate ratio of income to tuition cost
for key, value in school_avg_tuition.items():
	if get_key_in_map(key): # Keys that should not have been...
		school_income_ratio[key] = school_avg_tuition[key] / survey_avg_income[key]

############################## CREATE AGGREGATE TABLE AND INSERT ALL DATA INTO IT ###################################################

ins_conn = sqlite3.connect('combined.sqlite')
ins_conn.execute('''
    DROP TABLE IF EXISTS COMBINED
    ''')
ins_conn.execute('''
    CREATE TABLE
    IF NOT EXISTS COMBINED(
        ST TEXT,
        RATIO REAL
    );''')
for key in school_income_ratio:
	ins_conn.execute('''
		insert into COMBINED values (?,?);
		''', (key, school_income_ratio[key]))
ins_conn.commit()
ins_conn.close()
