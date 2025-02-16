Alter table constructorresults add foreign key (raceId) references races(raceId);
desc constructorresults;
Alter table constructorresults add foreign key (constructorId) references constructors(constructorId);
desc constructorresults;
alter table constructorstandings add foreign key (raceId) references races(raceId);
desc constructorstandings;
alter table constructorstandings add foreign key (constructorId) references constructors(constructorId);
desc constructorstandings;

use f1db;