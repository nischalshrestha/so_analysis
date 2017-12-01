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

# Holds all the questions
df_all = pd.read_csv('QueryQuestions.csv')
df_q = df_all[df_all['ClosedDate'].isnull()]
df_qt = df_q.shape[0]
# Holds all the answers
df_a = pd.read_csv('QueryAllAnswers.csv')
df_at = df_a.shape[0]

# Given a filtered dataframe, print total rows and percentage from total
def print_stats(df, df_c, s, t='questions'):
	df_t = df.shape[0]
	df_p = (df_t / float(df_c.shape[0]))*100
	print("Number of %s with %s: %d (%.2f%%)" % (t, s, df_t, df_p))

# Descriptive stats for Table 1 answering RQ1 generally

# Looking at open questions
# TODO Automate some of this in a loop if possible

# questions with at least an answer
df_answer = df_q[df_q.AnswerCount > 0]
print_stats(df_answer, df_q, 'answers')

# questions with no answer
df_no_answer = df_q[df_q.AnswerCount == 0]
print_stats(df_no_answer, df_q, 'no answers')

# questions with accepted answer
df_accepted = df_q[df_q['AcceptedAnswerId'].isnull()]
print_stats(df_accepted, df_q, 'an accepted answer')

 # questions with score >= 3
df_vo = df_q[df_q.Score >= 3]
print_stats(df_vo, df_q, 'votes >= 3')

# questions with views >= 300
df_vu = df_q[df_q.ViewCount >= 300]
print_stats(df_vu, df_q, 'views >= 300')

# questions with favorites
df_f = df_q[df_q.FavoriteCount > 0]
print_stats(df_f, df_q, 'favorites')

# Returns a list of ids of df that contains a given html in body
def tags(df, tag):
	ids = []
	for index, row in df.iterrows():
		soup = BeautifulSoup(row['Body'], 'html.parser')
		if len(soup.find_all(tag)) > 0:
			ids.append(row['Id'])
	return ids

# print('****IMAGES****')

# questions with images
img_ids = tags(df_q, 'img')
df_i = df_q[df_q['Id'].isin(img_ids)]
print_stats(df_i, df_q, 'images')
# answers with images
img_ids = tags(df_answer, 'img')
df_i = df_answer[df_answer['Id'].isin(img_ids)]
print_stats(df_i, df_answer, 'images', t='answers')
# answers with images
img_ids = tags(df_accepted, 'img')
df_i = df_accepted[df_accepted['Id'].isin(img_ids)]
print_stats(df_i, df_accepted, 'images', t='accepted answers')

# # HREF LINKS GENERAL

# print('****LINKS****')

# questions with links
links_ids = tags(df_q, 'a')
df_links = df_q[df_q['Id'].isin(links_ids)]
print_stats(df_links, df_q, 'links')
# answers with links
links_ids = tags(df_answer, 'a')
df_links_a = df_answer[df_answer['Id'].isin(links_ids)]
print_stats(df_links_a, df_answer, 'links', t='answers')
# accepted answers with links
links_ids = tags(df_accepted, 'a')
df_links_aa = df_accepted[df_accepted['Id'].isin(links_ids)]
print_stats(df_links_aa, df_accepted, 'links', t='accepted answers')

# print('****SPECIFIC LINKS****')
other_sites = []
# HREF LINKS SPECIFIC (could be cleaned up but will do for now)
def links(df):
	so_links = []
	droid_links = []
	google_links = []
	other_links = []
	for index, row in df.iterrows():
		soup = BeautifulSoup(row['Body'], 'html.parser')
		urls = soup.find_all('a')
		google_urls = soup.find_all('a', href=re.compile('google.com/design'))
		so_urls = soup.find_all('a', href=re.compile('stackoverflow.com'))
		droid_urls = soup.find_all('a', href=re.compile('developer.android.com'))
		if len(droid_urls) > 0:
			droid_links.append(row['Id'])
		elif len(so_urls) > 0:
			so_links.append(row['Id'])
		elif len(google_urls) > 0:
			google_links.append(row['Id'])
		elif len(urls) > 0:
			for u in urls:
				if 'png' in u['href'] or 'jpg' in u['href'] or 'gif' in u['href']:
					continue;
				other_links.append(row['Id'])
				if u not in other_sites:
					other_sites.append(u['href'])
	return so_links, droid_links, google_links, other_links

# TODO Lots of redundancy here, automate some of this in a loop if possible

links_specific_q = links(df_links)
links_specific_a = links(df_links_a)
links_specific_aa = links(df_links_aa)

# questions with links to other SO posts: stackoverflow.com
df_so = df_links[df_links['Id'].isin(links_specific_q[0])]
print_stats(df_so, df_links, 'SO links')

# answers with links to other SO posts: stackoverflow.com
df_so = df_links_a[df_links_a['Id'].isin(links_specific_a[0])]
print_stats(df_so, df_links, 'SO links', t='answers')

# accepted answers with links to other SO posts: stackoverflow.com
df_so = df_links_aa[df_links_aa['Id'].isin(links_specific_aa[0])]
print_stats(df_so, df_links_aa, 'SO links', t='accepted answers')

# questions with links to Android Documentation: developer.android.com
df_d = df_links[df_links['Id'].isin(links_specific_q[1])]
print_stats(df_d, df_links, 'Android links')

# answers with links to Android Documentation: developer.android.com
df_d = df_links_a[df_links_a['Id'].isin(links_specific_a[1])]
print_stats(df_d, df_links_a, 'Android links', t='answers')

# accepted answers with links to Android Documentation: developer.android.com
df_d = df_links_aa[df_links_aa['Id'].isin(links_specific_aa[1])]
print_stats(df_d, df_links_aa, 'Android links', t='accepted answers')

# questions with links to Google Design Documentation: google.com/design
df_g = df_links[df_links['Id'].isin(links_specific_q[2])]
print_stats(df_g, df_links, 'Google Design links')

# answers with links to Google Design Documentation: google.com/design
df_g = df_links_a[df_links_a['Id'].isin(links_specific_a[2])]
print_stats(df_g, df_links_a, 'Google Design links', t='answers')

# accepted answers with links to Google Design Documentation: google.com/design
df_g = df_links_aa[df_links_aa['Id'].isin(links_specific_aa[2])]
print_stats(df_g, df_links_aa, 'Google Design links', t='accepted answers')

# questions with links to other sites
df_o = df_links[df_links['Id'].isin(links_specific_q[3])]
print_stats(df_o, df_links, 'other links')

# answers with links to other sites
df_o = df_links_a[df_links_a['Id'].isin(links_specific_a[3])]
print_stats(df_o, df_links_a, 'other links', t='answers')

# answers with links to other sites
df_o = df_links_aa[df_links_aa['Id'].isin(links_specific_aa[3])]
print_stats(df_o, df_links_aa, 'other links', t='accepted answers')

with open('other_sites.txt', 'w') as f:
	for o in other_sites:
		f.write(o+'\n')

# CODE LINKS (either markup for single word or code sample)

print('****CODE MARKUP PRESENT****')

# questions with code markup or code sample
codes_ids = tags(df_q, 'code')
df_codes = df_q[df_q['Id'].isin(codes_ids)]
print_stats(df_codes, df_q, 'code markup')
	
# questions with single word code markup
def coverage(df, file):
	with open(file, 'r') as f:
		ids = []
		referenced = []
		coverage_type = f.read()
		coverage_type = list(filter(None, coverage_type.split('\n')))
		for d in coverage_type:
			for index, row in df.iterrows():
				if d in row['Title'] or d in row['Body']:
					if d not in referenced:
						referenced.append(d)
						if d in row['Body'] and d not in ids:
							ids.append(row['Id'])
		return referenced, coverage_type, ids

# # print('****CLASS + METHOD COVERAGE****')
class_coverage = coverage(df_q, 'added_classes.txt')
class_ref = class_coverage[0]
class_added = class_coverage[1]
class_ids = class_coverage[2]
class_t = len(class_ref)
class_p = (class_t / float(len(class_added)))*100

print("Number of questions with added classes: %d (%0.2f%%)" % (class_t, class_p))
print("Number of total added classes: %d" % (len(class_added)))

class_coverage = coverage(df_q, 'changed_classes.txt')
class_t = len(class_coverage[0])
class_p = (class_t / float(len(class_coverage[1])))*100
print("Number of questions with changed classes: %d (%0.2f%%)" % (class_t, class_p))
print("Number of total changed classes: %d" % (len(class_coverage[1])))

# This was used to clean the methods files which only includes names of methods
# with open('removed_methods.txt', 'r') as f, open('removed_methods_clean.txt', 'w') as o:
# 		referenced = []
# 		lines = f.read().split('\n')
# 		for l in lines:
# 			if 'type' not in l:
# 				o.write(l.split(' ')[0]+'\n')

method_coverage = coverage(df_q, 'added_methods.txt')
method_t = len(method_coverage[0])
method_p = (method_t / float(len(method_coverage[1])))*100
print("Number of questions with added methods: %d (%0.2f%%)" % (method_t, method_p))
print("Number of total questions with added methods: %d" % (len(method_coverage[1])))

method_coverage = coverage(df_q, 'changed_methods.txt')
method_t = len(method_coverage[0])
method_p = (method_t / float(len(method_coverage[1])))*100
print("Number of questions with changed methods: %d (%0.2f%%)" % (method_t, method_p))
print("Number of total questions with changed methods: %d" % (len(method_coverage[1])))

method_coverage = coverage(df_q, 'removed_methods.txt')
method_t = len(method_coverage[0])
method_p = (method_t / float(len(method_coverage[1])))*100
print("Number of questions with removed methods: %d (%0.2f%%)" % (method_t, method_p))
print("Number of total questions with removed methods: %d" % (len(method_coverage[1])))

# questions with code sample
# Randomly sample 100 questions that have answers
# The html file is simply to make the tagging process easier, in the future
# one could build a web app for such tasks
# df_r = df_vu.sample(100)
# with open('random_sample.html', 'w') as f, open('random_sample_ids.txt', 'w') as o:
# 	f.write('<!DOCTYPE html>\n')
# 	f.write('<html lang="en-US">\n')
# 	f.write('<head><style>body {background-color: #5c8457;}' \
# 		+ ' h1 {color: white;}p {color: #E8AA0C;}</style></head>')
# 	f.write('<body><p>\n')
# 	values = list(df_r['Id'].values)
# 	# print(values)
# 	for i in range(0, len(values)):
# 		o.write(str(values[i])+'\n')
# 		f.write('<a href=\"https://stackoverflow.com/questions/' + \
# 			# str(values[i]) + '\" target=\"_blank\">' + str(values[i])+'</a>\n')
# 			str(values[i]) + '\">' + str(values[i])+'</a>\n')
# 	f.write('</p><body>\n')
# 	f.write('</html>')


