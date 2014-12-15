INSERT INTO `YuPointsDB`.`Points`
(
`PointName`,
`LatitudeBeg`,
`LongitudeBeg`,
`LatitudeEnd`,
`LongitudeEnd`,
`Address`,
`Phone`,
`WebSite`,
`Duration`,
`PriorityWithinLocation`,
`Description`,
`LocationCityID_FK`,
`LocationCountryID_FK`,
`IndoorOutdoor`,
`Fee`,
`Kids`,
`Restroom`,
`DisabledAccess`,
`StrollerAccess`,
`ChangingPad`,
`Parking`,
`PicnickArea`,
`Tips`,
`DateOfEntry`)
VALUES

('The de Young','37.7715N','122.4687W','','','Golden Gate Park 50 Hagiwara Tea Garden Drive San Francisco, CA 94118','415-750-3600','http://deyoung.famsf.org/',3,0,
'The de Young, a fine arts museum located in San Francisco\'s Golden Gate Park, is one of the Fine Arts Museums of San Francisco along with the Legion of Honor. The de Young is named for its founder, early San Francisco newspaperman M. H. de Young.',
1,1,1,1,1,1,1,1,1,1,0,'','2014-08-14'),
('The Legion of Honor','37.7844N','122.5008W','','','Lincoln Park 100 34th Avenue San Francisco, CA 94121','415-750-3600','http://legionofhonor.famsf.org/',1.5,0,
'The Legion of Honor displays a collection spanning more than 6,000 years of ancient and European art and houses the Achenbach Foundation for Graphic Arts in a neoclassical building overlooking Lincoln Park and the Golden Gate Bridge.',
1,1,2,1,1,1,1,1,1,1,0,'','2014-08-14'),
('San Francisco Museum of Modern Art','37.7857N','122.401W','','','151 Third Street, San Francisco, California 94103','','http://www.sfmoma.org/',4,0,
'The San Francisco Museum of Modern Art (SFMOMA) is a modern art museum located in San Francisco, California. A nonprofit organization, SFMOMA holds an internationally recognized collection of modern and contemporary art and was the first museum on the West Coast devoted solely to 20th century art. The museums current collection includes over 29,000 works of painting, sculpture, photography, architecture, design, and media arts.',
1,1,1,1,1,1,1,1,1,1,0,'Closed for expansion till 2016','2014-08-14'),
('The San Francisco Zoo','37.7331N','122.5031W','','','2945 Sloat Blvd, San Francisco, CA 94132','415-753-7080','http://www.sfzoo.org/index.htm',4,0,
'The San Francisco Zoo is a 100-acre (40 ha) zoo located in the southwestern corner of San Francisco, California, between Lake Merced and the Pacific Ocean along the Great Highway.',
1,1,0,1,1,1,1,1,1,1,1,'','2014-08-19'),
('War Memorial Opera House','37.7786N','122.4208W','','','301 Van Ness Ave, San Francisco, CA 94102','415-864-3330','http://sfopera.com/Home.aspx',4,0,'It has been the home of the San Francisco Opera since opening night in 1932.',
1,1,1,1,1,1,1,1,1,0,0,'','2014-08-19'),
('San Francisco Symphony','37.778N','122.420W','','','201 Van Ness Ave, San Francisco, CA 94102','415-864-6000','http://www.sfsymphony.org/index.aspx',4,0,
'The San Francisco Symphony (SFS), founded in 1911, is an orchestra based in San Francisco, California. Since 1980, the orchestra has performed at the Louise M. Davies Symphony Hall in the Citys Hayes Valley neighborhood.',
1,1,1,1,1,1,1,1,1,0,0,'','2014-08-19'),
('Golden Gate Bridge','37.8197N','122.4786W','','','Golden Gate Bridge, San Francisco, CA 94129','','http://goldengate.org/',4,0,''
,1,1,0,0,1,1,1,1,0,0,1,'','2014-08-19'),
('Sutro Baths','37.4648 N','122.3049 W','','','Point Lobos Ave, San Francisco, CA 94121','415-426-5240','http://www.nps.gov/goga/planyourvisit/cliff-house-sutro-baths.htm',1.5,0,
'The Sutro Baths were a large, privately owned swimming pool complex near Seal Rock in San Francisco, California, built in the late 19th century. The facility was financially unprofitable and is now in ruins. Lands around the site have been integrated into the Golden Gate National Recreation Area.',
1,0,0,1,0,0,0,0,0,0,0,'','2014-08-19'),
('Coit Tower','37.8025N','122.4058W','','','1 Telegraph Hill Blvd, San Francisco, CA 94133','','',1.5,0,
'Storied 1930s-era building known for its WPA murals, 360-degree views & resident flock of parrots',
1,1,2,1,1,1,1,1,0,1,0,'','2014-08-19')
;

#
INSERT INTO `YuPointsDB`.`LocationCity`
(`LocationCityName`
)
VALUES
(
'San Francisco');

#
INSERT INTO `YuPointsDB`.`LocationCountry`
(
`LocationCountryName`,LocationCountryName_Short)
VALUES
('United States of America',
'USA');

#
INSERT INTO `YuPointsDB`.`TypesOfPoint`
(
`TypeName`)
VALUES
('museum')
,('beach')
,('music')
,('bridge')
,('park')
,('zoo')
,('view point')
,('hike')
,('explore')
,('kids')
,('historic')
,('art')
;

INSERT INTO `YuPointsDB`.`TypesOfPoint_Points`
(`PointID`,
`PointTypeID`)
VALUES
(1,1),
(2,1),
(2,9),
(2,10),
(2,12),
(3,1),
(3,9),
(3,10),
(4,1),
(4,12),
(5,1),
(5,5),
(6,1),
(6,12),
(8,3),
(7,6),
(9,3),
(10,4),
(11,7),
(11,11),
(12,7),
(12,11),
(12,12)








;



