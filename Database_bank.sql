CREATE database bankingsys;
USE bankingsys;

##################################################

--
-- Table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `cust_num` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(30) DEFAULT NULL,
  `address` varchar(80) DEFAULT NULL,
  `bal` float(15,2) DEFAULT NULL,
  PRIMARY KEY (`acc_no`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;



##################################################

--
-- Table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
CREATE TABLE IF NOT EXISTS `transaction` (
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `amount` float(10) DEFAULT NULL,
  `acc_type` char(20) DEFAULT NULL,
  `type` char(20) DEFAULT NULL,
  `cust_num` int(10) DEFAULT NULL,
  PRIMARY KEY (`index`),
  FOREIGN KEY (`cust_num`) REFERENCES customer(`cust_num`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

