# NBA Records

This app pulls data from [Basketball Reference](https://www.basketball-reference.com/) website and saves to MySQL database. The following information for every team in the NBA is saved:
* Conference (East or West)
* Team Abbreviation (e.g. DAL, BOS, NYK, etc.)
* Wins (int)
* Losses (int)
* Date

## Prerequisites
To run this Python program, the following packages are required:
```
pip install selenium
pip install webdriver_manager
pip install pandas
pip install mysql-connector-python
```

A MySQL database is also required. MySQL can be directly installed, or you can install Docker and run the following command to spin up a MySQL database instance: 
```
docker run --name myContainer -v /tmp/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=tigertiger -d -p 3306:3306 mysql:8
```

Running the above Docker command will create a MySQL 8 container with the name myContainer, database root password tigertiger, and port 3306. Also install a MySQL DB development tool, such as MySQL Workbench. Following the initialization of the Docker container, open MySQL Workbench and add the Docker database connection:
* Name: Anything of the user's choice
* Hostname: 127.0.0.1
* Port: 3306
* Username: root
* Password: tigertiger

Using MySQL Workbench, create a database called "nba" used by the program:
```
CREATE DATABASE nba;
```

## Running the program
Running the "extractor.py" file will extact NBA team stats data, and saves the data into a MySQL database table named "nbaRecords". If the table does not exist, it will be automatically created. 

To access the table data, execute the following query in MySQL Workbench:
```
SELECT * FROM nbaRecords;

SELECT * FROM nbaRecords WHERE wins = (SELECT MAX(wins) FROM nbaRecords)  -- Best team
SELECT * FROM nbaRecords WHERE wins < (SELECT AVG(wins) FROM nbaRecords); -- Under average teams
```

## References
* [Basketball Reference](https://www.basketball-reference.com/)
* [Docker](https://docs.docker.com/engine/install/)
* [MySQL Workbench] (https://www.mysql.com/products/workbench/)