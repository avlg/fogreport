//for more information on MySQL user rights assignment see
//http://dev.mysql.com/doc/refman/5.7/en/grant.html

CREATE USER 'fogreports'@'%' IDENTIFIED BY 'PASSWodR';
GRANT SELECT ON fog.* TO 'fogreports'@'%';
