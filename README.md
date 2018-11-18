# Udacity Full Stack Developer project: Log Analysis

## Short project summary
The database contains newspaper articles,
as well as the web server log for the site.
The log has a database row for each time a reader loaded a web page.
Your code will answer questions about the site's user activity.

## Project details

There are 3 DB tables: articles, authors and log.
Table articles has a foreign key referencing authors.
Table log doesn't have explicit relation to other tables.
The task is to create a reporting tool that prints out reports (in plain text)
based on the data in the database.
This reporting tool is a Python program
using the psycopg2 module to connect to the database.

### The project's output
The questions that need to be answered by the project are:
1. What are the most popular three articles of all time?
   (Display the answer as a list where one row is
    an article's title followed by -- and number of views)
2. Who are the most popular article authors of all time?
   (The answer is a list of
    authors followed by total sum of visits to their articles)
3. On which days did more than 1% of requests lead to errors?
   (The answer is a date followed by the percentage of errors:
    July 29, 2016 — 2.5% errors)

### The DB tables info
The database is provided.
Here is an additional information about the tables:

#### Table articles

```
Table "public.articles"
Column |           Type           |                  Modifiers
-------+--------------------------+---------------------------------------------
author | integer                  | not null
title  | text                     | not null
slug   | text                     | not null
lead   | text                     |
body   | text                     |
time   | timestamp with time zone | default now()
id     | integer                  | not null default nextval('articles_id_seq'::regclass)
Indexes:
"articles_pkey" PRIMARY KEY, btree (id)
"articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
Foreign-key constraints:
"articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)
```
The table has 8 rows.

#### Table authors

```
Table "public.authors"
Column |  Type   |                      Modifiers
-------+---------+------------------------------------------------------
name   | text    | not null
bio    | text    |
id     | integer | not null default nextval('authors_id_seq'::regclass)
Indexes:
"authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)
```
The table has 4 rows.

#### Table Log

```
Table "public.log"
Column |           Type           |                    Modifiers
-------+--------------------------+--------------------------------------------
path   | text                     |
ip     | inet                     |
method | text                     |
status | text                     |
time   | timestamp with time zone | default now()
id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
"log_pkey" PRIMARY KEY, btree (id)
```
The table has 1,677,735 rows

## Helper queries (and results) that had been ran before implementing this project.

1. What are the different statuses?
```
news=> select distinct status from log;
    status
---------------
 404 NOT FOUND
 200 OK
(2 rows)
```
2. What the paths are like?
   They seem to be the only thing that can connect us to articles table.
```
news=> select distinct path from log limit 20;
                path
-------------------------------------
 /article/goats-eat-googlesh
 /article/goats-eat-googlesy
 /article/candidate-is-jerkb
 /article/balloon-goons-doomedr
 /article/bad-things-gonex
 /article/candidate-is-jerkn
 /article/bears-love-berriese
 /article/media-obsessed-with-bearsl
 /article/candidate-is-jerky
 /article/bears-love-berriesb
 /article/media-obsessed-with-bearsa
 /article/candidate-is-jerkg
 /article/trouble-for-troubledl
 /article/bears-love-berriesn
 /article/bad-things-goneh
 /article/so-many-bearsq
 /article/candidate-is-jerkq
 /article/trouble-for-troubledr
 /article/bears-love-berriesl
 /article/balloon-goons-doomedu
(20 rows)
```
3. Now let's look at the articles
```
news=> select title from articles;
               title
------------------------------------
 Bad things gone, say good people
 Balloon goons doomed
 Bears love berries, alleges bear
 Candidate is jerk, alleges rival
 Goats eat Google's lawn
 Media obsessed with bears
 Trouble for troubled troublemakers
 There are a lot of bears
(8 rows)
```
4. We see the extra letters at the end of paths. What if we will look only
at the successfull paths?
```
news=> select distinct path from log where status like '%200%';
                path
------------------------------------
 /
 /article/goats-eat-googles
 /article/balloon-goons-doomed
 /article/trouble-for-troubled
 /article/candidate-is-jerk
 /article/bears-love-berries
 /article/bad-things-gone
 /article/so-many-bears
 /article/media-obsessed-with-bears
(9 rows)
```
5. Can we turn an article title into a thing uniquely identifying path?
We see that the first word of the title changed to lower case combined with
preceding forward slash would work (except for so-many-bears).
We could use the replace function for that one.
```
news=> select replace(lower(substring(tit from 0 for position(' ' in tit))), 'there', 'so')
from (select distinct title as tit from articles) as titles;
  replace
-----------
 bears
 bad
 balloon
 trouble
 so
 media
 candidate
 goats
(8 rows)
```
6. See the first view for the assignment to answer first 2 questions.
7. Answer the first question:
```
news=> select '"' || title || '" -- ' ||  count(title) || ' views'
from article_log
group by title
order by count(title) desc;
                      ?column?
-----------------------------------------------------
 "Candidate is jerk, alleges rival" -- 338647 views
 "Bears love berries, alleges bear" -- 253801 views
 "Bad things gone, say good people" -- 170098 views
 "Goats eat Google's lawn" -- 84906 views
 "Trouble for troubled troublemakers" -- 84810 views
 "Balloon goons doomed" -- 84557 views
 "There are a lot of bears" -- 84504 views
 "Media obsessed with bears" -- 84383 views
(8 rows)
```
8. Answer the second question:
```
news=> select name || ' -- ' || count(name) || ' views'
news-> from article_log
news-> group by name
news-> order by count(name) desc;
                ?column?
----------------------------------------
 Ursula La Multa -- 507594 views
 Rudolf von Treppenwitz -- 423457 views
 Anonymous Contributor -- 170098 views
 Markoff Chaney -- 84557 views
(4 rows)
```

## Views created for this project.

### "article_log" view for the first 2 questions.

This view combines the information from all 3 tables to answer a lot of
different questions viewing log from authors and articles points of view.
This view will include only successful articles access.

```
news=> create view article_log
news->   as select articles.title,
news->             authors.name,
news->             log.path,
news->             log.id,
news->             log.time,
news->             log.ip
news-> from articles, authors, log
news-> where log.status like '%200%'
news->   and articles.author = authors.id
news->   and log.path like '%/'
news->         || (replace(
news(>               lower(substring(
news(>                  articles.title
news(>                  from 0
news(>                  for position(' ' in articles.title)
news(>               )),
news(>               'there',
news(>               'so'
news(>            )) || '%';
CREATE VIEW
```
