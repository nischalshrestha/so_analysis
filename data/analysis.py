import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re

# import matplotlib.pyplot as plt

# Question cols
# print(df_q.columns.values)
# ['Id' 'PostTypeId' 'AcceptedAnswerId' 'ParentId' 'CreationDate'
#  'DeletionDate' 'Score' 'ViewCount' 'Body' 'OwnerUserId' 'OwnerDisplayName'
#  'LastEditorUserId' 'LastEditorDisplayName' 'LastEditDate'
#  'LastActivityDate' 'Title' 'Tags' 'AnswerCount' 'CommentCount'
#  'FavoriteCount' 'ClosedDate' 'CommunityOwnedDate']

# Answer cols
# print(df_a.columns.values)
# ['Id' 'PostTypeId' 'AcceptedAnswerId' 'ParentId' 'CreationDate'
#  'DeletionDate' 'Score' 'ViewCount' 'Body' 'OwnerUserId' 'OwnerDisplayName'
#  'LastEditorUserId' 'LastEditorDisplayName' 'LastEditDate'
#  'LastActivityDate' 'Title' 'Tags' 'AnswerCount' 'CommentCount'
#  'FavoriteCount' 'ClosedDate' 'CommunityOwnedDate' 'Id.1' 'PostTypeId.1'
#  'AcceptedAnswerId.1' 'ParentId.1' 'CreationDate.1' 'DeletionDate.1'
#  'Score.1' 'ViewCount.1' 'Body.1' 'OwnerUserId.1' 'OwnerDisplayName.1'
#  'LastEditorUserId.1' 'LastEditorDisplayName.1' 'LastEditDate.1'
#  'LastActivityDate.1' 'Title.1' 'Tags.1' 'AnswerCount.1' 'CommentCount.1'
#  'FavoriteCount.1' 'ClosedDate.1' 'CommunityOwnedDate.1']

# Gotcha: parens needed in conditions
df = pd.read_csv('Questions.csv')
df['Accepted'] = np.where(df['AcceptedAnswerId'].notnull(), 1, 0)
df = df[(df['ClosedDate'].isnull()) & (df['Score'] > 0)]
df = df.loc[:, ['Score', 'Accepted', 'AnswerCount', 'CommentCount']]
# df = df.groupby(['Score']).mean()
# if selecting multiple
# df = df.groupby(['Score', 'Accepted']).mean()
# by : mapping, function, str, or iterable (also don't need "by=")
# the below groupby is like doing ". ~ Score" for R's by in aggregate
df = df.groupby('Score', as_index=False).mean()
# by : str or list of str
df = df.sort_values('Score', ascending=False)
# df.corr('pearson')
# print(df.sort_values('Score', ascending=False))
print(df.corr('pearson'))

# Holds all the questions
df = pd.read_csv('Questions.csv')
df_q = df[df['ClosedDate'].isnull()]
df_qt = len(df_q)
# print("Number of questions total: %d" % df_qt)
# print(df_q[['ClosedDate']])
# In Python we use [] to select columns
# ':' is used to slice
# For vanilla slice we have [n:n], [:n], [:n] [n:n:+/-n]
# all rows with all cols (no slice)
# print(df_q[:])
# first row with all cols
# print(df_q[1:2])
# you can use a 3rd number for steps
# e.g. every other
# print(df_q[0:7:2])
# you can also go in reverse
# print(df_q[6::-1])
# print(df_q[:6:-1])

# Gotcha: you can't use +/- steps for anything other than
# vanilla slicing.
# use loc for label-based indexing 
# all rows all cols
# print(df_q.loc[:,])
# all rows 1 or more cols 
# print(df_q.loc[:,'ClosedDate'].head(100))
# Example of transfer issue within Python, the below code doesn't
# work and prints all rows instead of filtering null values
# Another issue is that usually in Python you use null or not null
# to filter for nulls but here isnull() and notnull() are used.
# print(df['ClosedDate'].dtype)

# gotcha: you need to wrap each condition here with parens
# if you don't you get different results

# you can also have condition for the : part of loc
# print(df.query('ClosedDate.isnull() & Score == 0').head(2))
# print(df.loc[(df['ClosedDate'].isnull()) & (df['Score'] == 0), ['ClosedDate', 'Score']].head(2))
# print(df.loc[(df['ClosedDate'].isnull()) & (df['Score'] == 0), ['ClosedDate', 'Score']].head(2))

# print(len(df_q.query('(AnswerCount > 0) & (Score > 0)')))

# print(df.loc[df['ClosedDate'].isnull() & df['Score'] == 0, ['ClosedDate', 'Score']])
# Equivalent:
# print(df[(df['ClosedDate'].isnull()) & (df['Score'] == 0)].loc[:,['ClosedDate', 'Score']])


# first two rows and all cols
# print(df_q[1:3])

# use ix for indexing dfs based on indices
# first and third row and all cols
# print(df_q.ix[[0,2]])
# using iloc:
# print(df_q.iloc[[0,2],:])

# iloc for
# first row and 2nd and third col
# print(df_q.iloc[0:1,1:3])

# first, second row and second and third col
# print(df_q.iloc[0:2,1:3])

# all rows and first column
# print(df_q.iloc[:,0:1])
# or:
# print(df_q.iloc[:,[0]])

# all rows and first and third col
# print(df_q.iloc[:,[0,1]])



# Holds all the answers
df_a = pd.read_csv('QueryAllAnswers.csv')
df_at = len(df_a)
# print("Number of answers total: %d" % df_at)

# Given a filtered dataframe, print total rows and percentage from total
def print_stats(df, s):
	df_t = len(df)
	df_p = int(((df_t / float(df_qt)) * 100))
	print("Number of questions with %s: %d (%d%%)" % (s, df_t, df_p))

# # Descriptive stats for Table 1 answering RQ1 generally

# # Looking at open questions

# questions with at least an answer
# df_answer = df_q[df_q.AnswerCount > 0]
# print_stats(df_answer, 'answers')

# # questions with no answer
# df_no_answer = df_q[df_q.AnswerCount == 0]
# print_stats(df_no_answer, 'no answers')

# # questions with accepted answer
# df_accepted = df_q[df_q['AcceptedAnswerId'].isnull()]
# print_stats(df_accepted, 'an accepted answer')

#  # questions with score >= 3
# df_vo = df_q[df_q.Score >= 3]
# print_stats(df_vo, 'votes >= 3')

# # questions with views >= 300
# df_vu = df_q[df_q.ViewCount >= 300]
# print_stats(df_vu, 'views >= 100')

# # questions with favorites
# df_f = df_q[df_q.FavoriteCount > 0]
# print_stats(df_f, 'favorites')

# # questions with code markup or code sample
# # df_code = df_q[df_q]

# # html_text = """
# # <h2>this is cool #12345678901</h2>
# # <h2>this is nothing</h2>
# # <h2>this is interesting #126666678901</h2>
# # <h2>this is blah #124445678901</h2>
# # """

# # soup = BeautifulSoup(html_text, 'html.parser')

# # pattern = re.compile(r'blah')
# # print(soup.find('h2', text=pattern))

# # Returns a list of ids of df that contains a given html in body
# def tags(tag):
# 	ids = []
# 	for index, row in df_q.iterrows():
# 		soup = BeautifulSoup(row['Body'], 'html.parser')
# 		if len(soup.find_all(tag)) > 0:
# 			ids.append(row['Id'])
# 	return ids

# # HREF LINKS GENERAL

# # questions with links
# links_ids = tags('a')
# df_links = df_q[df_q['Id'].isin(links_ids)]
# df_links_t = df_links.shape[0]
# df_links_p = int(((df_links_t / float(df_qt))*100))
# print("Number of questions with links: %d (%d%%)" % (df_links_t, df_links_p))

# # HREF LINKS SPECIFIC (could be cleaned up but will do for now)
# so_links = []
# droid_links = []
# other_links = []
# for index, row in df_links.iterrows():
# 	soup = BeautifulSoup(row['Body'], 'html.parser')
# 	so_urls = soup.find_all('a', href=re.compile('stackoverflow.com'))
# 	droid_urls = soup.find_all('a', href=re.compile('developer.android.com'))
# 	if len(droid_urls) > 0:
# 		droid_links.append(row['Id'])
# 	elif len(so_urls) > 0:
# 		so_links.append(row['Id'])
# 	else:
# 		other_links.append(row['Id'])

# # questions with links to other SO posts: stackoverflow.com
# df_so = df_links[df_links['Id'].isin(so_links)]
# df_so_t = df_so.shape[0]
# df_so_p = (df_so_t / float(df_links_t))*100
# print("Number of questions with SO links: %d (%.2f%%)" % (df_so_t, df_so_p))

# # questions with links to Android Documentation: developer.android.com
# df_d = df_links[df_links['Id'].isin(droid_links)]
# df_d_t = df_d.shape[0]
# df_d_p = (df_d_t / float(df_links_t))*100
# print("Number of questions with Android links: %d (%.2f%%)" % (df_d_t, df_d_p))

# # questions with links to other sites
# df_o = df_links[df_links['Id'].isin(other_links)]
# df_o_t = df_o.shape[0]
# df_o_p = (df_o_t / float(df_links_t))*100
# print("Number of questions with other links: %d (%.2f%%)" % (df_o_t, df_o_p))

# # CODE LINKS (either markup for single word or code sample)

# # questions with code markup or code sample
# codes_ids = tags('code')
# df_codes = df_q[df_q['Id'].isin(codes_ids)]
# df_codes_t = df_codes.shape[0]
# df_codes_p = int(((df_codes_t / float(df_qt))*100))
# print("Number of questions with codes: %d (%d%%)" % (df_codes_t, df_codes_p))

# # questions with single word code markup

# # questions with code sample

# # randomly sample 300 questions that have answers
# # df_r = df_q.sample(300)
# # with open('random_sample.html', 'w') as f:
# # 	f.write('<!DOCTYPE html>\n')
# # 	f.write('<html lang="en-US">\n')
# # 	f.write('<head><style>body {background-color: #5c8457;}' \
# # 		+ ' h1 {color: white;}p, a {color: #E8AA0C;}</style></head>')
# # 	f.write('<body><p>\n')
# # 	values = list(df_r['Id'].values)
# # 	# print(values)
# # 	for i in range(0, len(values)):
# # 		f.write('<a href=\"https://stackoverflow.com/questions/' + \
# # 			str(values[i]) + '\" target=\"_blank\">' + str(values[i])+'</a>\n')
# # 	f.write('</p><body>\n')
# # 	f.write('</html>')

# # TODO: Descriptive stats for Table 1 answering RQ1 by category on random 
# # subset of questions

