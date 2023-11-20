# Youtube_DataHarvesting
YouTube Data Harvesting and Warehousing is a project aimed at developing a user-friendly Streamlit application that leverages the power of the Google API to extract valuable information from YouTube channels.

# Storing data in MongoDB
The retrieved data is stored in a MongoDB database based on user authorization. If the data already exists in the database, it can be overwritten with user consent. This storage process ensures efficient data management and preservation, allowing for seamless handling of the collected data.

# Migrating data from Mongo DB to MYSQL
The application allows users to migrate data from MongoDB to a SQL data warehouse. Users can choose which channel's data to migrate. To ensure compatibility with a structured format, the data is cleansed using the powerful pandas library. Following data cleaning, the information is segregated into separate tables, including channels, playlists, videos, and comments, utilizing SQL queries.

# Tools Used
 1. Spyder
 2. Mongo DB
 3. MYSQL Workbench

# Requried Libraries:
1. googleapiclient.discovery
2. Streamlit
3. Pymongo
4. mysql.connector
5. Regular Expression
