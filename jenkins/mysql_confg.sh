#!/bin/bash

apt-get update && apt-get install -y openjdk-8-jdk mysql-server-5.7

mysql -e "CREATE USER 'devops'@'%' IDENTIFIED BY 'mestre';"
mysql -e "CREATE USER 'devops_dev'@'%' IDENTIFIED BY 'mestre';"
mysql -e "CREATE DATABASE todo;"
mysql -e "CREATE DATABASE todo_dev;"
mysql -e "CREATE DATABASE test_todo_dev;"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'devops'@'%' IDENTIFIED BY 'mestre';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'devops_dev'@'%' IDENTIFIED BY 'mestre';"
