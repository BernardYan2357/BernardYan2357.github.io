# SQL

References: [Learn SQL | SQLBolt | Learn&Exercise](https://sqlbolt.com/)

SQL, or **Structured Query Language**, is a language designed to allow users to query, manipulate, and transform data from a **relational database**. And due to its simplicity, SQL databases provide safe and scalable storage for millions of websites and mobile applications

> A relational database represents a collection of related (two-dimensional) tables. Each of the tables are similar to an Excel spreadsheet(n. 电子表格程序), with a fixed number of named columns (the attributes or properties of the table) and any number of rows of data

There are many popular SQL databases including SQLite, MySQL, Postgres, Oracle and Microsoft SQL Server. All of them support the common SQL language standard, but each implementation can differ in the additional features and storage types it supports

## Database Design

In relational database, Facing many-to-many data relationship

### Database Normalization

Entity data in the real world is often broken down into pieces and stored across multiple orthogonal(adj. 正交的，相互独立的) tables using a process known as _Database normalization_

[Database normalization](https://en.wikipedia.org/wiki/Database_normalization) is the process of structuring a relational database in accordance with a series of **normal forms** to reduce data redundancy(n. 冗余) and improve data integrity. **In general, it is a set of rules splitting tables**

There are three most commonly used normal forms:

- First normal form
	- each attribute domain is _atomic_, which contains no other attributes
	- 例如一张表里面联系方式一列填着“138xxxx, Beijing”，应该拆成“电话”和“地址”两列
- Second normal form
	- In addition to satisfying 1NF, a table which has **composite key**(复合主键) contains no partial dependencies
	- partial dependencies means there are non-primary keys which depend on only **part** of a composite key
	- 例如一张表有复合主键：（学号, 课程名），但还有“学分”一列。学分的多少只取决于“课程名”，与“学号”无关，存在部分依赖，应该拆出一个单独的表：“(课程名, 学分)”
- Third normal form
	-  In addition to satisfying 2NF, all non-primary key must be directly dependent on the primary key, dependencies cannot be indirectly passed on through other non-primary key
	- 例如一张表有属性：学号、学院ID、学院电话。学号决定了学院ID，学院ID又决定了学院电话，存在间接依赖，应单独建一个学院表：学院ID、学院电话，学生表里只保留学院ID作为外键

Database normalization is useful because it minimizes duplicate data in any single table, and allows for data in the database to grow independently of each other. As a trade-off, queries get  more complex since they have to be able to find data from different parts of the database, and performance issues can arise when working with many large tables. Some time we also use **Denormalization** to increase query speed

## Synatx

### CREATE Database

```sql
CREATE DATABASE IF NOT EXISTS mydatabase;
USE mydatabase; -- 切换到该数据库
```

注意 SQLite 没有 `CREATE DATABASE` 语句，SQLite 的数据库就是一个文件，在 SQLite 中创建数据库参考：[[SQL#open database]]

### CREATE Tables

Create a new database table using the `CREATE TABLE` statement

```sql
CREATE TABLE IF NOT EXISTS mytable ( 
	column_name DataType TableConstraint DEFAULT default_value, 
	another_column DataType TableConstraint DEFAULT default_value,
	...
);

-- example
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    director TEXT,
    year INTEGER, 
    length_minutes INTEGER
);
```

- If there already exists a table with the same name, the SQL implementation will usually throw an error, so to suppress the error and skip creating a table if one exists, you can use the `IF NOT EXISTS` clause
- The structure of the new table is defined by its table **schema**(n. 模式，结构), which defines a series of columns. Each column has a name, the type of data allowed in that column, an **optional** table constraint on values being inserted, and an optional default value

#### Data type

Different databases support different data types, but the common types support numeric, string, and other miscellaneous things like dates, booleans, or even binary data. Here are some examples: 

| Data type                                            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `INTEGER`, `BOOLEAN`                                 | The integer datatypes can store whole integer values like the count of a number or an age. In some implementations, the boolean value is just represented as an integer value of just 0 or 1.                                                                                                                                                                                                                                                      |
| `FLOAT`, `DOUBLE`, `REAL`                            | The floating point datatypes can store more precise numerical data like measurements or fractional values. Different types can be used depending on the floating point precision required for that value.                                                                                                                                                                                                                                          |
| `CHARACTER(num_chars)`, `VARCHAR(num_chars)`, `TEXT` | The text based datatypes can store strings and text in all sorts of locales. The distinction between the various types generally amount to underlaying efficiency of the database when working with these columns.<br>Both the CHARACTER and VARCHAR (variable character) types are specified with the max number of characters that they can store (longer values may be truncated), so can be more efficient to store and query with big tables. |
| `DATE`, `DATETIME`                                   | SQL can also store date and time stamps to keep track of time series and event data. They can be tricky to work with especially when manipulating data across timezones.                                                                                                                                                                                                                                                                           |
| `BLOB`                                               | SQL can store binary data in blobs right in the database. These values are often opaque to the database, so you usually have to store them with the right metadata to requery them.                                                                                                                                                                                                                                                                |
Consult your database docs: [SQLite Datatype](https://www.sqlite.org/datatype3.html)

#### Table constraints

Table constraints limit what values can be inserted into column. This list shows a few common constraints:

| Constraint           | Description                                                                                                                                                                                                                                                                                                                                                                                  |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PRIMARY KEY`        | This means that the values in this column are unique, and each value can be used to identify a single row in this table.                                                                                                                                                                                                                                                                     |
| `AUTOINCREMENT`      | For integer values, this means that the value is automatically filled in and incremented(v. 增加) with each row insertion. Not supported in all databases.                                                                                                                                                                                                                                     |
| `UNIQUE`             | This means that the values in this column have to be unique, so you can't insert another row with the same value in this column as another row in the table. Differs from the `PRIMARY KEY` in that it doesn't have to be a key for a row in the table.                                                                                                                                      |
| `NOT NULL`           | This means that the inserted value can not be `NULL`.                                                                                                                                                                                                                                                                                                                                        |
| `CHECK (expression)` | This allows you to run a more complex expression to test whether the values inserted are valid. For example, you can check that values are positive, or greater than a specific size, or start with a certain prefix, etc.                                                                                                                                                                   |
| `FOREIGN KEY`        | This is a consistency check which ensures that each value in this column corresponds to another value in a column in another table.  <br>For example, if there are two tables, one listing all Employees by ID, and another listing their payroll information, the `FOREIGN KEY` can ensure that every row in the payroll table corresponds to a valid employee in the master Employee list. |

### AlTER Tables

 Use the `ALTER TABLE` statement to add, remove, or modify columns and table constraints

 The syntax is similar to `CREATE TABLE`:

```sql
ALTER TABLE mytable
ADD column DataType TableConstraint DEFAULT default_value -- add columns
DROP column_to_be_deleted -- remove columns
RENAME TO new_table_name; -- rename the table
```

- some databases (including SQLite) don't support `DROP`. Instead you may have to create a new table and migrate the data over
- Consult your database docs: [SQLite](https://www.sqlite.org/lang_altertable.html "SQLite Alter Table")

### DROP Tables

Use the `DROP TABLE` statement, which differs from the `DELETE` statement in that it also removes the table schema from the database entirely

```sql
DROP TABLE IF EXISTS mytable;
```

- like the `CREATE TABLE` statement, the database may throw an error if the specified table does not exist, and to suppress that error, you can use the `IF EXISTS` clause
- if you have another table that is dependent on columns in table you are removing (for example, with a `FOREIGN KEY` dependency) then you will have to either update all dependent tables first to remove the dependent rows or to remove those tables entirely

### INSERT rows

Use an `INSERT` statement to declare which table to write into, the columns of data that we are filling, and one or more rows of data to insert. In general, each row of data you insert should contain values for every corresponding column in the table. You can insert multiple rows at a time by just listing them sequentially:

```sql
INSERT INTO mytable
VALUES (value_or_expr, another_value_or_expr, ...),
       (value_or_expr_2, another_value_or_expr_2, ...),
       ...;
```

In some cases, if you have incomplete data and the table contains columns that support default values, you can insert rows with only the columns of data you have by specifying them explicitly:

```sql
INSERT INTO mytable
(column, another_column, ...)
VALUES (value_or_expr, another_value_or_expr, ...),
      (value_or_expr_2, another_value_or_expr_2, ...),
      ...;
```

In these cases, the number of values need to match the number of columns specified. Despite this being a more verbose statement to write, inserting values this way has the benefit of being forward compatible. For example, if you add a new column to the table with a default value, no hardcoded `INSERT` statements will have to change as a result to accommodate that change.

In addition, you can use mathematical and string expressions with the values that you are inserting.  This can be useful to ensure that all data inserted is formatted a certain way

### UPDATE rows

In addition to adding new data, a common task is to update existing data, which can be done using an `UPDATE` statement. Similar to the `INSERT` statement, you have to specify exactly which table, columns, and rows to update. In addition, the data you are updating has to match the data type of the columns in the table schema

```sql
UPDATE mytable
SET column = value_or_expr, 
    other_column = another_value_or_expr, 
    ...
WHERE condition;
```

The statement works by taking multiple column/value pairs, and applying those changes to each and every row that satisfies the constraint in the `WHERE` clause

### DELETE rows

Use `DELETE` statement to delete data from a table in the database

```sql
DELETE FROM mytable
WHERE condition;
```

For `UPDATE` and `DELETE` statement, it's recommended that you run the constraint in a `SELECT` query first to ensure that you are removing the right rows. Without a proper backup or test database, it is downright easy to irrevocably remove data, so always read your `DELETE` statements twice and execute once

### SELECT Queries

To retrieve(v. 检索) **data** from a SQL **database**, we need to write `SELECT` statements, which are often colloquially(adv. 口语地) refered to as _queries_. A query in itself is just a statement which declares what data we are looking for, where to find it in the database, and optionally, how to transform it before it is returned

```sql
SELECT column, another_column, FROM mytable;
SELECT * FROM mytable; -- a simple way to inspect a table by dumping all the data at once
```

#### Queries with Constraints

Use a `WHERE` clause(n. 从句) in the query. The clause is applied to each row of data by checking specific column values to determine whether it should be included in the results or not

```sql
SELECT column, another_column, FROM mytable -- 此处不能有; 语句没有终止，后面还有从句
WHERE condition
	AND/OR another_condition -- 这里被筛选的 colnum 必须在上面出现
	AND/OR ...;
```
> More complex clauses can be constructed by joining numerous `AND` or `OR` logical keywords

Below are some useful operators that you can use for numerical(adj. 数字的) data (ie. integer or floating point):

| Operator            | Condition                                            | SQL Example                     |
| ------------------- | ---------------------------------------------------- | ------------------------------- |
| =, !=, <, <=, >, >= | Standard numerical operators                         | `col_name = 67`                 |
| BETWEEN x AND y     | `[x, y]`                                             | `col_name BETWEEN 1.5 AND 10.5` |
| NOT BETWEEN x AND y | Number is not within range of two values (inclusive) | `col_name NOT BETWEEN 1 AND 10` |
| IN (…)              | Number exists in a list，括号内也可以嵌套 SELECT 语句           | `col_name IN (2, 4, 6)`         |
| NOT IN (…)          | Number does not exist in a list                      | `col_name NOT IN (1, 3, 5)`     |

For columns containing text data, SQL supports a number of useful operators to do things like case-insensitive(adj. 不区分大小写的) string comparison and wildcard(adj. 通配符) pattern matching:

| Operator   | Condition                                                                                             | Example                                                                 |
| ---------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| =          | Case sensitive exact string comparison (_notice the single equals_)                                   | `col_name = "abc"`                                                      |
| != or <>   | Case sensitive exact string inequality comparison                                                     | `col_name != "abcd"`                                                    |
| LIKE       | Case insensitive exact string comparison                                                              | `col_name LIKE "ABC"`                                                   |
| NOT LIKE   | Case insensitive exact string inequality comparison                                                   | `col_name NOT LIKE "ABCD"`                                              |
| %          | Used anywhere in a string to match a sequence of zero or more characters (only with LIKE or NOT LIKE) | `col_name LIKE "%AT%"`<br>(matches "AT", "ATTIC", "CAT" or even "BATS") |
| _          | Used anywhere in a string to match a single character (only with LIKE or NOT LIKE)，占位符？               | `col_name LIKE "AN_"` (matches "AND", but not "AN")                     |
| IN (…)     | String exists in a list                                                                               | `col_name IN ("A", "B", "C")`                                           |
| NOT IN (…) | String does not exist in a list                                                                       | `col_name NOT IN ("D", "E", "F")`                                       |
> All strings must be quoted so that the query parser can distinguish words in the string from SQL keywords

We should note that while most database implementations are quite efficient when using these operators, full-text search is best left to dedicated libraries like [Apache Lucene](http://lucene.apache.org/ "Apache Lucene") or [Sphinx](http://sphinxsearch.com/ "Sphinx Search"). These libraries are designed specifically to do full text search, and as a result are more efficient and can support a wider variety of search features including internationalization and advanced queries.

#### Filtering and sorting Query results

Even though the data in a database may be unique, the results of any particular query may not be, take Movies table for example, many different movies can be released the same year. In such cases, SQL provides a convenient way to discard rows that have a duplicate(adj. 完全一样的) column value by using the `DISTINCT` keyword:

```sql
SELECT DISTINCT column, another_column, ... -- DISTINCT 针对指定的 colnums 去重，所以不要用 *
FROM mytable;
```

SQL provides a way to **sort your results** by a given column in ascending or descending order using the `ORDER BY` clause, each row is sorted alpha-numerically based on the specified column's value:

```sql
SELECT column, another_column, …
FROM mytable
ORDER BY column ASC/DESC;
```

Another clause which is commonly used with the `ORDER BY` clause are the `LIMIT` and `OFFSET` clauses. The `LIMIT` will reduce the number of rows to return, and the optional `OFFSET` will specify where to begin counting the number rows from:

```sql
SELECT column, another_column, …
FROM mytable
ORDER BY column ASC/DESC
LIMIT num_limit OFFSET num_offset; -- 展示第 1+num_offset 到第 num_limit+num_offset row
```

#### Multi-table queries with JOINs

In order to answer questions about an entity that has data spanning multiple tables in a **normalized database**, we need to learn how to write a query that can combine all that data and pull out exactly the information we need

Tables that share information about a single entity need to have a _primary key_ that identifies that entity _uniquely_ across the database. One common primary key type is an auto-incrementing integer (because they are space efficient), but it can also be a string, hashed value, so long as it is unique

Using the `JOIN` clause in a query, we can combine row data across two separate tables

`INNER JOIN` is a process that matches rows from the first table and the second table which **have the same key** (as defined by the `ON` constraint) to create a result row with the combined columns from both tables

```sql
SELECT mytable.column, another_table.column, ... -- JOIN 是 SELECT 的从句，所以在这里可以填写其它表的 colunm，这里也不必要选择 id 列，不会影响匹配
FROM mytable
INNER JOIN another_table
    ON mytable.id = another_table.id
WHERE condition(s)
...
```

If the two tables have asymmetric(adj. 不对称的) data, then we would have to use a `LEFT JOIN`, `RIGHT JOIN` or `FULL JOIN` instead to ensure that the data you need is not left out of the results

```sql
SELECT column, another_column, ...
FROM A
INNER/LEFT/RIGHT/FULL JOIN B
    ON A.id = B.matching_id
WHERE condition(s)
```

- LEFT JOIN: simply includes rows from A regardless of whether a matching row is found in B. For rows in A that do not contain the key from B, the key value is NULL
- RIGHT JOIN: Opposite of LEFT JOIN
- FULL JOIN: simply means that rows from both tables are kept, regardless of whether a matching row exists in the other table

#### Queries with expressions

We can use _expressions_ to write more complex logic on column values in a query. These expressions can use mathematical and string functions along with basic arithmetic to transform values when the query is executed, as shown in this physics example:

```sql
SELECT particle_speed / 2.0 AS half_particle_speed -- 使用 AS 给处理过的列设置别名，便于理解
FROM physics_data
WHERE ABS(particle_position) * 10.0 > 500;
```

Each database has its own supported set of mathematical, string, and date functions that can be used in a query, which you can find in their own respective docs

#### Queries with aggregates

SQL also supports the use of aggregate(adj. 聚合的) expressions (or functions) that allow you to summarize information about a group of rows of data

```sql
SELECT other_colnum, AGG_FUNC(column_or_expression) AS aggregate_description, ...
FROM mytable
WHERE constraint_expression;
```

Here are some common aggregate functions:

| Function                            | Description                                                                                                                                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **COUNT(*)**, **COUNT(**column**)** | A common function used to counts the number of rows in the group if no column name is specified. Otherwise, count the number of rows in the group with non-NULL values in the specified column. |
| **MIN(**column**)**                 | Finds the smallest numerical value in the specified column for all rows in the group.                                                                                                           |
| **MAX(**column**)**                 | Finds the largest numerical value in the specified column for all rows in the group.                                                                                                            |
| **AVG(**column)                     | Finds the average numerical value in the specified column for all rows in the group.                                                                                                            |
| **SUM(**column**)**                 | Finds the sum of all numerical values in the specified column for the rows in the group.                                                                                                        |
Consult your database docs: [SQLite aggfunc](http://www.sqlite.org/lang_aggfunc.html)

Without a specified grouping, each aggregate function is going to run on the whole set of result rows and return a **single value**. In addition to aggregating across all the rows, you can instead apply the aggregate functions to individual groups of data within that group. This would then create **as many results as there are unique groups** defined as by the `GROUP BY` clause

The `GROUP BY` clause works by grouping rows that have the same value in the column specified: 

```sql
SELECT AGG_FUNC(column_or_expression) AS aggregate_description, ...
FROM mytable
WHERE constraint_expression
GROUP BY column;
```

If the `GROUP BY` clause is executed after the `WHERE` clause (which filters the rows which are to be grouped), then how exactly do we filter the grouped rows?

Luckily, SQL allows us to do this by adding an additional `HAVING` clause which is used specifically with the `GROUP BY` clause to allow us to filter grouped rows from the result set

```sql
SELECT group_by_column, AGG_FUNC(column_expression) AS aggregate_result_alias, ... FROM mytable
WHERE condition
GROUP BY column
HAVING group_condition;
```

The `HAVING` clause constraints are written the same way as the `WHERE` clause constraints, and are applied to the grouped rows. The `HAVING` clause might not seem like a particularly useful construct, but if you imagine data with millions of rows with different properties, being able to apply additional constraints is often necessary to quickly make sense of the data

#### Order of execution of a Query

```sql
SELECT DISTINCT column, AGG_FUNC(column_or_expression), ...
FROM mytable
    JOIN another_table
      ON mytable.column = another_table.column
    WHERE constraint_expression
    GROUP BY column
    HAVING constraint_expression
    ORDER BY column ASC/DESC
    LIMIT count OFFSET COUNT;
```

Each query begins with finding the data that we need in a database, and then filtering that data down into something that can be processed and understood as quickly as possible. Because each part of the query is executed sequentially, it's important to understand the order of execution so that you know what results are accessible where

1. The `FROM` clause, and subsequent `JOIN`s are first executed to determine the total working set of data that is being queried. This includes [[SQL#Subqueries]] in this clause, and can cause temporary tables to be created under the hood
2. Once we have the total working set of data, the `WHERE` constraints are applied to the individual rows, and rows that do not satisfy the constraint are discarded. Each of the constraints can only access columns directly from the tables requested in the `FROM` clause. Aliases in the `SELECT` part of the query are **not accessible** in most databases since they may include expressions dependent on parts of the query that have not yet executed
3. The remaining rows after the `WHERE` constraints are applied are then grouped based on common values in the column specified in the `GROUP BY` clause
4. If the query has a `GROUP BY` clause, then the constraints in the `HAVING` clause are then applied to the grouped rows, discard the grouped rows that don't satisfy the constraint. Like the `WHERE` clause, aliases are also not accessible from this step in most databases
5. **Any expressions in the `SELECT` part of the query are finally computed**
6. Of the remaining rows, rows with duplicate values in the column marked as `DISTINCT` will be discarded
7. If an order is specified by the `ORDER BY` clause, the rows are then sorted by the specified data in either ascending or descending order. Since all the expressions in the `SELECT` part of the query have been computed, you can reference aliases in this clause
8. Finally, the rows that fall outside the range specified by the `LIMIT` and `OFFSET` are discarded, leaving the final set of rows to be returned from the query

### Subqueries

### NULL values in databases

It's always good to reduce the possibility of `NULL` values in databases because they require special attention when constructing queries, constraints (certain functions behave differently with null values) and when processing the results

An alternative to `NULL` values in your database is to have _data-type appropriate default values_, like 0 for numerical data, empty strings for text data, etc. But if your database needs to store incomplete data, then `NULL` values can be appropriate if the default values will skew(v. 使倾斜) later analysis (for example, when taking averages of numerical data)

Sometimes, it's also not possible to avoid `NULL` values, for example when outer-joining two tables with asymmetric data. In these cases, you can test a column for `NULL` values in a `WHERE` clause by using either the `IS NULL` or `IS NOT NULL` constraint

```sql
SELECT column, another_column, ...
FROM mytable
WHERE column IS/IS NOT NULL
AND/OR another_condition
AND/OR ...;
```

### SQL Insert

## SQLite

References: [The Code Inside Everything (That Gets Zero Credit)](https://www.youtube.com/watch?v=lSVgeMoXJTs)

### open database

```shell
sqlite3 mydatabase.db # 如果文件不存在，会自动创建
# or
sqlite3
sqlite> .open mydatabase.db # 打开或创建数据库文件
```

#### schema.sql

在该文件中使用 SQL 定义数据库的表结构，利用这个模板生成数据库表结构：

```shell
# 方式一：把 schema.sql 文件内容导入
sqlite3 mydatabase.db < schema.sql
# 方式二：在 SQLite 命令行里读取
sqlite3 mydatabase.db
.read schema.sql
.tables
```

### better-sqlite3

[better-sqlite3](https://github.com/WiseLibs/better-sqlite3) 是一个为 Node.js 设计的，快速、简单且高效的 SQLite3 数据库。它的核心特点是提供**同步（Synchronous）API**，在保证易用性的同时，性能远超传统的异步库（如 `node-sqlite3`）

better-sqlite3 的核心操作主要围绕 **Database** 和 **Statement** 这两个类展开

#### 1. Database 类方法

*   **`new Database(path, [options])`**: 创建或打开一个数据库连接。
    *   `path`: 数据库文件路径，传入 `":memory:"` 可创建内存数据库。
    *   `options`: 可选配置，如 `readonly`（只读）、`timeout`（超时时间）等。
    *   ```javascript
        const Database = require('better-sqlite3');
        const db = new Database('my-app.db', { verbose: console.log });
        ```
*   **`.prepare(string)`**: 预编译一个SQL语句，返回一个 `Statement` 对象。这是执行查询的推荐方式，安全且高效。
    *   ```javascript
        const stmt = db.prepare('SELECT * FROM users WHERE age > ?');
        ```
*   **`.transaction(function)`**: 将一个函数包装成一个数据库事务。函数内的所有数据库操作要么全部成功，要么全部回滚。
    *   ```javascript
        const insert = db.prepare('INSERT INTO users (name) VALUES (?)');
        const insertMany = db.transaction((names) => {
          for (const name of names) insert.run(name);
        });
        insertMany(['Alice', 'Bob', 'Charlie']);
        ```
*   **`.pragma(string, [options])`**: 执行一个 PRAGMA 语句，用于设置或查询数据库的配置，如 `journal_mode`。
    *   ```javascript
        db.pragma('journal_mode = WAL');
        ```
*   **`.exec(string)`**: 直接执行一个或多个SQL语句（不推荐用于常规查询，主要用于执行迁移脚本等）。
*   **`.close()`**: 关闭数据库连接。
    *   ```javascript
        db.close();
        ```

#### 2. Statement 类方法

*   **`.run([...bindParameters])`**: 执行一个不返回数据的SQL语句（如 `INSERT`, `UPDATE`, `DELETE`）。返回一个包含 `changes`（影响行数）和 `lastInsertRowid`（最后插入的ID）的对象。
    *   ```javascript
        const stmt = db.prepare('INSERT INTO users (name) VALUES (?)');
        const info = stmt.run('Alice');
        console.log(info.changes); // 输出: 1
        ```
*   **`.get([...bindParameters])`**: 执行查询并返回结果集中的**第一行**数据。如果没有找到数据，则返回 `undefined`。
    *   ```javascript
        const stmt = db.prepare('SELECT * FROM users WHERE id = ?');
        const user = stmt.get(123);
        console.log(user.name);
        ```
*   **`.all([...bindParameters])`**: 执行查询并**一次性**返回所有匹配的行，结果是一个数组。数据量不大时推荐使用。
    *   ```javascript
        const stmt = db.prepare('SELECT * FROM users WHERE age > ?');
        const users = stmt.all(18);
        console.log(users.length);
        ```
*   **`.iterate([...bindParameters])`**: 执行查询并返回一个**迭代器（Iterator）**，允许你逐行处理数据，适合处理大量数据以节省内存。
    *   ```javascript
        const stmt = db.prepare('SELECT * FROM large_table');
        for (const row of stmt.iterate()) {
          // 逐行处理 row
        }
        ```

#### 简单示例

```javascript
const Database = require('better-sqlite3');

// 1. 打开数据库
const db = new Database('example.db');

// 2. 创建表
db.prepare('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)').run();

// 3. 插入数据
const insertStmt = db.prepare('INSERT INTO users (name) VALUES (?)');
insertStmt.run('Alice');

// 4. 查询数据
const selectStmt = db.prepare('SELECT * FROM users');
const allUsers = selectStmt.all();
console.log(allUsers); // 输出: [ { id: 1, name: 'Alice' } ]

// 5. 关闭数据库
db.close();
```
