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
   (Display the answer as article's title followed by -- and number of views)
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

### Table Log

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
