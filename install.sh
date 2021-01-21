sudo pip3 install flask

sudo apt install mysql-server

SET GLOBAL validate_password.policy=LOW;
CREATE USER 'deepak'@'%' IDENTIFIED BY 'forth';
GRANT ALL PRIVILEGES ON *.* TO 'deepak'@'%';
FLUSH PRIVILEGES;

pip3 install mysql-connector-python
pip3 install Flask-Mail