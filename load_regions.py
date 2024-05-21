from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from modeles import GeoIP, Country, Region

# (Assume you have already defined the GeoIP model and database connection)
if __name__ == "__main__":
    engine = create_engine('sqlite:///geoip.db')
    Session = sessionmaker(bind=engine)

    # Create a session to interact with the database
    session = Session()

    # Define the query using SQLAlchemy's query builder
    query = session.query(GeoIP.country_code, GeoIP.region_name).group_by(GeoIP.country_code, GeoIP.region_name)

    # Execute the query and fetch results
    for country_code, region_name in query.all():
        region_existante = session.query(Region).filter(Region.country_code == country_code, Region.region_name == region_name).first()
        if region_existante is None:
            region = Region(country_code=country_code, region_name=region_name)
            session.add(region)
            print(f"Add: country Code: {country_code}, region_name: {region_name}")        

    # Close the session when done
    session.commit()
    session.close()
