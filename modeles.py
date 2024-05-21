from sqlalchemy import create_engine, Column, Integer, String, Float, Index
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

class Base(DeclarativeBase):
    pass

# Define the geoip table model
class GeoIP(Base):
    __tablename__ = 'geoip'

    ip_from = Column(Integer, primary_key=True, nullable=False)
    ip_to = Column(Integer, nullable=False)
    country_code = Column(String(2), nullable=False)
    country_name = Column(String(64), nullable=False)
    region_name = Column(String(128))
    city_name = Column(String(128))
    latitude = Column(Float)
    longitude = Column(Float)

class IPFrance(Base):
    __tablename__ = 'ip_france'

    ip_from = Column(Integer, primary_key=True, nullable=False)
    ip_to = Column(Integer, nullable=False)

class Country(Base):
    __tablename__ = 'countries'

    country_code = Column(String(2), primary_key=True, nullable=False)
    country_name = Column(String(64), nullable=False)
    
class Region(Base):
    __tablename__ = 'regions'

    region_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    country_code = Column(String(2), nullable=False)
    region_name = Column(String(128))

    # Define a named unique index on country_code and region_name
    unique_constraint = Index('unique_country_region', country_code, region_name, unique=True)

    # Add the index to table arguments
    __table_args__ = (unique_constraint,)


if __name__ == "__main__":
    engine = create_engine('sqlite:///geoip.db')

    # Create all tables in the engine (if they don't exist)
    Base.metadata.create_all(engine)

    # (Optional) Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    session.close()
