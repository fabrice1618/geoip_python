import csv
import gzip
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modeles import GeoIP

if __name__ == "__main__":
    # Connect to the database (assuming you have already created the table)
    engine = create_engine('sqlite:///geoip.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Open the CSV file for reading
    with gzip.open('geoip.csv.gz', 'rt') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile, delimiter=',')

        # Skip the header row (assuming the first row contains column names)
        next(reader)

        count = 0
        # Extract data from the current row
        for ip_from, ip_to, country_code, country_name, region_name, city_name, latitude, longitude in reader:
            count += 1
            # Insert data into the geoip table
            geoip_entry = GeoIP(ip_from=ip_from, ip_to=ip_to, country_code=country_code, country_name=country_name,
                            region_name=region_name, city_name=city_name, latitude=latitude, longitude=longitude)
            session.add(geoip_entry)
            if count % 100 == 0:
                session.commit()
                print(ip_from, country_code, city_name)

    # Commit changes to the database
    if count % 100 != 0:
        session.commit()
        print(ip_from, country_code, city_name)

    # Close the session
    session.close()
