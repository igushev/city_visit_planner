/*drop table YuPointsDB.Points;
create table if not exists YuPointsDB.Points (
	PointId int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY ,
	PointName varchar(100) NOT NULL,
	LatitudeBeg    float NULL ,
	LongitudeBeg   float NULL ,
	LatitudeEnd    float NULL ,
	LongitudeEnd   float NULL ,
	#Altitude    float NULL , ?????
	Address varchar(1000),
	Phone varchar(20),
	WebSite varchar(150),
	Duration float NOT NULL,
	PriorityWithinLocation int, # from crawler
	Description longtext,
	LocationCityID_FK int(11),
	LocationCountryID_FK int(11),
	IndoorOutdoor boolean,
	Fee boolean,
	Kids boolean,
	Restroom boolean,
	DisabledAccess boolean, #paved unpaved	Complexity of hike?????
	StrollerAccess boolean,
	ChangingPad boolean,
	Parking boolean,
	PicnickArea boolean,
	Tips longtext, #SpecialTipsTable ??
	#PhotosTable
	#SpecialEventsTable
	DateOfEntry datetime NULL);*/
/*
# depends on season, month, day of week, special events
create table if not exists YuPointsDB.HoursOfOperation (
	PointID  int(11) NOT NULL,
	PeriodBeg date NOT NULL,
	PeriodBeg date NOT NULL,
	Monday time,
	Tuesday time,
	Wednesday time,
	Thursday time,
	Friday time,
	Saturday time,
	Sunday time
);

# Load from Wiki
create table if not exists YuPointsDB.WeatherPerMonth (
	LocationCityID int(11) NOT NULL,
	Month int,
	WeatherF int,
	WeatherC int
);
*/
# beach, museum, bridge...
drop table YuPointsDB.TypesOfPoint;
create table if not exists YuPointsDB.TypesOfPoint (
	PointTypeID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	TypeName varchar(100) NOT NULL
);

# M:M Points and Types of points
drop table YuPointsDB.TypesOfPoint_Points;
create table if not exists YuPointsDB.TypesOfPoint_Points(
	PointID int(11) NOT NULL,
	PointTypeID int(11) NOT NULL
);
/*
# Hiking, Biking, Horses...
create table if not exists YuPointsDB.Activities (
	ActivityID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	ActivityName varchar(100) NOT NULL
);

# M:M Points and Activities
create table if not exists YuPointsDB.Activities_Points (
	PointID int(11) NOT NULL,
	ActivityID int(11) NOT NULL
);

# Age categories
create table if not exists YuPointsDB.AgeCategories (
	AgeCategoryID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	AgeCategoryName varchar(100) NOT NULL,
	AgeFrom int,
	AgeTo int
);

# Ticket Prices in local currency divided by age category
create table if not exists YuPointsDB.TicketPrices (
	PointID int(11) NOT NULL,
	AgeCategoryID int(11) NOT NULL,
	Price int,
	PriceCurrencyID int NOT NULL
);

# Currency
create table if not exists YuPointsDB.Currency (
	CurrencyID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	CurrencyName varchar(15) NOT NULL,
	CurrencyRate float NULL
);

#Languages
*/
# City
drop table YuPointsDB.LocationCity;
create table if not exists YuPointsDB.LocationCity (
	LocationCityID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	LocationCityName varchar(100) NOT NULL,
	LocationCityName_Short varchar(100) NULL
);

# Country
drop table YuPointsDB.LocationCountry;
create table if not exists YuPointsDB.LocationCountry (
	LocationCountryID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	LocationCountryName varchar(100) NOT NULL,
	LocationCountryName_Short varchar(100) NULL
);
/*
# Means of conveyance
create table if not exists YuPointsDB.MeansOfConveyance (
	MeansOfConveyanceID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	MeansOfConveyanceName varchar(100) NOT NULL,
	IsPointOfInterest boolean
);

# M:M How to reach point
create table if not exists YuPointsDB.MeansOfConveyance_Points (
	PointID int(11) NOT NULL,
	MeansOfConveyanceID int(11)
);

# Images
create table if not exists YuPointsDB.Images (
	ImageID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	Image longblob NOT NULL,
	DateOfEntry datetime NOT NULL
);

# M:M Images of Points
create table if not exists YuPointsDB.Images_Points (
	PointID int(11) NOT NULL,
	ImageID int(11) NOT NULL
	
);


# Users
create table if not exists YuPointsDB.Users (
	UserID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	UserFirstName varchar(1000),
	UserMiddleName varchar(1000),
	UserLastName varchar(1000),
	Gender boolean,
	LocationCityID_FK int(11),
	LocationCountryID_FK int(11),
	Kids boolean,
	IndoorOutdoor boolean,
	PreferredTypeOfTransportationID int(11),
	PrimaryLanguageID int(11),
	PreferredCurrencyID int(11),
	DateOfReg     datetime
);

# M:M Images of Users
create table if not exists YuPointsDB.Images_Users (
	UserID int(11) NOT NULL,
	ImageID int(11) NOT NULL
	
);

# Languages
create table if not exists YuPointsDB.Languages (
	LanguageID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	LnaguageName varchar(100) NOT NULL
);

# Visited Points
create table if not exists YuPointsDB.VisitedPoints (
	UserId int(11) NOT NULL,
	PointID int(11) NOT NULL,
	DateOfVisit datetime NOT NULL
);

# Friends
create table if not exists YuPointsDB.Friends (
	UserId int(11) NOT NULL,
	FriendID int(11) NOT NULL
);

# Reviews
create table if not exists YuPointsDB.Reviews (
	ReviewID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	Review longtext NOT NULL,
	DateOfEntry datetime NOT NULL
);

# Review of Point by user
create table if not exists YuPointsDB.Review_Point_User (
	UserId int(11) NOT NULL,
	PointID int(11) NOT NULL,
	ReviewID int(11) NOT NULL
);

# Saved trips table






*/








