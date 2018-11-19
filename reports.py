#!/usr/bin/env python3
#
# Uses "newsdata" database to answer 3 questions (in plain text):
# What are the most popular three articles of all time?
# Who are the most popular article authors of all time?
# On which days did more than 1% of requests lead to errors?

import psycopg2

# Questions use can pick and choose from.
QUESTIONS = [
    "What are the most popular three articles of all time?",
    "Who are the most popular article authors of all time?",
    "On which days did more than 1% of requests lead to errors?",
]

# Queries for the questions above in the corresponding order.
QUERIES = [
    "select '\"' || title || '\" -- ' ||  count(title) || ' views' from article_log group by title order by count(title) desc limit 3;",
    "select name || ' -- ' || count(name) || ' views' from article_log group by name order by count(name) desc;",
    "select 'July ' || day || ', 2016 -- ' || substring(('' || error::float /percent) from 0 for  4 ) || '%  errors' from statistics where error > percent;",
]

# Run single query by the provided index. Get either result or an error message.
def single_query(idx):
    if (idx < 0 or idx >= len(QUERIES)):
        print "Idx = " + idx
        return ["Invalid question index: I only answer 3 predefined questions."]
    connection = psycopg2.connect("dbname=news")
    cursor = connection.cursor()
    cursor.execute(QUERIES[idx])
    result = cursor.fetchall()
    connection.close()
    return result

if __name__ == '__main__':
    print "\n\n"
    for i in range(3):
        print QUESTIONS[i]
        print "====================================================="
        result = single_query(i)
        for row in result:
          print row[0]
        print "\n\n\n"
