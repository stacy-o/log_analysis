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
at the successful paths?
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
9. What is the time span in the log?
```
news=> select min(time), max(time) from log;
          min           |          max
------------------------+------------------------
 2016-07-01 07:00:00+00 | 2016-07-31 19:59:55+00
(1 row)
```
  It all happens in the same months, so we can use "day" part
  of the date to aggregate the data.
10. See the second view.
11. Show the second view (as there are only 31 rows).
```
news=> select * from statistics;
 good  | error | day | total | percent
-------+-------+-----+-------+---------
 38431 |   274 |   1 | 38705 |     387
 54811 |   389 |   2 | 55200 |     552
 54465 |   401 |   3 | 54866 |     548
 54523 |   380 |   4 | 54903 |     549
 54162 |   423 |   5 | 54585 |     545
 54354 |   420 |   6 | 54774 |     547
 54380 |   360 |   7 | 54740 |     547
 54666 |   418 |   8 | 55084 |     550
 54826 |   410 |   9 | 55236 |     552
 54118 |   371 |  10 | 54489 |     544
 54094 |   403 |  11 | 54497 |     544
 54466 |   373 |  12 | 54839 |     548
 54797 |   383 |  13 | 55180 |     551
 54813 |   383 |  14 | 55196 |     551
 54554 |   408 |  15 | 54962 |     549
 54124 |   374 |  16 | 54498 |     544
 54642 |  1265 |  17 | 55907 |     559
 55215 |   374 |  18 | 55589 |     555
 54908 |   433 |  19 | 55341 |     553
 54174 |   383 |  20 | 54557 |     545
 54823 |   418 |  21 | 55241 |     552
 54800 |   406 |  22 | 55206 |     552
 54521 |   373 |  23 | 54894 |     548
 54669 |   431 |  24 | 55100 |     551
 54222 |   391 |  25 | 54613 |     546
 53982 |   396 |  26 | 54378 |     543
 54122 |   367 |  27 | 54489 |     544
 54404 |   393 |  28 | 54797 |     547
 54569 |   382 |  29 | 54951 |     549
 54676 |   397 |  30 | 55073 |     550
 45516 |   329 |  31 | 45845 |     458
(31 rows)
```
12. See the errors percentage:
```
news=> select day, error, percent, substring(
news(>  ('' || error::float /percent) from 0 for  4 ) as result from statistics;
 day | error | percent | result
-----+-------+---------+--------
   1 |   274 |     387 | 0.7
   2 |   389 |     552 | 0.7
   3 |   401 |     548 | 0.7
   4 |   380 |     549 | 0.6
   5 |   423 |     545 | 0.7
   6 |   420 |     547 | 0.7
   7 |   360 |     547 | 0.6
   8 |   418 |     550 | 0.7
   9 |   410 |     552 | 0.7
  10 |   371 |     544 | 0.6
  11 |   403 |     544 | 0.7
  12 |   373 |     548 | 0.6
  13 |   383 |     551 | 0.6
  14 |   383 |     551 | 0.6
  15 |   408 |     549 | 0.7
  16 |   374 |     544 | 0.6
  17 |  1265 |     559 | 2.2
  18 |   374 |     555 | 0.6
  19 |   433 |     553 | 0.7
  20 |   383 |     545 | 0.7
  21 |   418 |     552 | 0.7
  22 |   406 |     552 | 0.7
  23 |   373 |     548 | 0.6
  24 |   431 |     551 | 0.7
  25 |   391 |     546 | 0.7
  26 |   396 |     543 | 0.7
  27 |   367 |     544 | 0.6
  28 |   393 |     547 | 0.7
  29 |   382 |     549 | 0.6
  30 |   397 |     550 | 0.7
  31 |   329 |     458 | 0.7
(31 rows)
```
13. The query that answers the last (3rd) question:
```
select 'July ' || day || ', 2016 -- '
       || substring(('' || error::float /percent) from 0 for  4 )
       || '%  errors' as answer3
  from statistics
 where error > percent;
            answer3
-------------------------------
 July 17, 2016 -- 2.2%  errors
(1 row)
```

## Views created for this project.

### The "article_log" view for the first 2 questions.

This view combines the information from all 3 tables to answer a lot of
different questions viewing log from authors and articles points of view.
This view will include only successful articles access.
This view could answer other questions like: from how many different IPs
was accessed each article? Which article was most popular on a particular day?
Which day was the "peak interest" for a particular article or author? And so on.

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

## The "silver_slug" view.
This view is the same as "article_log", but the query for it is much simpler.
This is what happens when you don't judge data by the column name, but instead
go and check it out.
```
create view silver_slug --(as in "silver bullet")
  as select articles.title,
            authors.name,
            log.path,
            log.id,
            log.time,
            log.ip
       from articles, authors, log
      where log.status like '%200%'
        and articles.author = authors.id
        and log.path like ('%/' || articles.slug || '%');
CREATE VIEW
```

### The "statistics" view for the last question.
This view aggregates counts of success and failures for each day, and calculates
total as well as how many attempts constitutes one percent of the day's traffic.
This view can answer additional questions such as what was the most busy day,
What is the biggest traffic fluctuation, is there any correlation between
traffic, errors and days of the week and so on.
```
news=> create view statistics as
news-> select good.count as good,
news->        bad.count as error,
news->        good.day,
news->        good.count + bad.count as total,
news->        (good.count + bad.count)/100 as percent
news->   from (
news(>         select date_part('day', time) as day, count(*) as count
news(>           from log
news(>          where status like '%200%'
news(>         group by date_part('day', time)
news(>        ) as good,
news->        (
news(>         select date_part('day', time) as day, count(*) as count
news(>           from log
news(>          where status not like '%200%'
news(>         group by date_part('day', time)
news(>        ) as bad
news->  where good.day = bad.day;
CREATE VIEW
```
