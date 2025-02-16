from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine('mysql+mysqlconnector://root:admin@localhost:3306/f1db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Driver(Base):
    __tablename__ = 'drivers'

    driverId = Column(Integer, primary_key=True)
    driverRef = Column(String(255))
    number = Column(Integer)
    code = Column(String(3))
    forename = Column(String(255))
    surname = Column(String(255))
    dob = Column(Date)
    nationality = Column(String(255))
    url = Column(String(255))

    def __repr__(self):
        return f"Driver(id={self.id}, name={self.name})"

class Race(Base):
    __tablename__ = "races"

    raceId = Column(Integer, primary_key=True)
    year = Column(Integer)
    name = Column(String(255))

class Results(Base):
    __tablename__ = "results"

    resultId = Column(Integer, primary_key=True)
    raceId = Column(Integer, nullable=False)
    driverId = Column(Integer, nullable=False)
    constructorId = Column(Integer, nullable=False)
    number = Column(Integer)
    grid = Column(Integer)
    position = Column(Integer)
    positionText = Column(String(255))
    positionOrder = Column(Integer)
    points = Column(Float)
    laps = Column(Integer)
    time = Column(String(255))
    milliseconds = Column(Integer)
    fastestLap = Column(Integer)
    rank = Column(Integer)
    fastestLapTime = Column(String(255))
    fastestLapSpeed = Column(String(255))
    statusId = Column(Integer)

    def __repr__(self):
        return f"<Results(resultId={self.resultId}, raceId={self.raceId}, driverId={self.driverId}, position={self.position})>"


drivers = session.query(Driver).all()
for driver in drivers:
    print(driver.driverId, driver.surname)

races = session.query(Race).all()
for race in races:
    if race.year >2023:
        print(race.raceId, race.year)


drivers_in_2024 = session.query(Driver, Race, Results) \
    .join(Results, Driver.driverId == Results.driverId) \
    .join(Race, Race.raceId == Results.raceId) \
    .filter(Race.year == 2024) \
    .all()
alonso_better_count =0
alonso_result = []
stroll_result = []
for driver, race, result in drivers_in_2024:
    if driver.surname =="Alonso":
        if result.position is None:
            result.position = 21
        alonso_result.append(result.position)
    if driver.surname =="Stroll":
        if result.position is None:
            result.position = 21
        stroll_result.append(result.position)

print(f"alonso {(alonso_result)}")
print(f"Stroll {(stroll_result)}")
for i in range(len(alonso_result)):
    if alonso_result[i] < stroll_result[i]:
        alonso_better_count +=1

print(f"Alonso był {alonso_better_count} razy lepszy od Strolla")
session.close()