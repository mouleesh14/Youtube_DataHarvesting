# Youtube_DataHarvesting
YouTube Data Harvesting and Warehousing is a project aimed at developing a user-friendly Streamlit application that leverages the power of the Google API to extract valuable information from YouTube channels.

# Approach
1. Connect to YouTube API
2. Store data in Mongo DB lake
3. Migrate data to an SQL database warehouse
4. Query and display the data in Streamlit application

# YouTube API
The YouTube API (Application Programming Interface) allows developers to interact with YouTube's features and data programmatically. This API enables developers to integrate YouTube functionality into their applications, websites, or services.  This API allows developers to retrieve information about videos, playlists, channels, and user activities on YouTube. It provides access to read-only data, such as video details, comments, and user profiles.

# Mongo DB
MongoDB is a open-source NoSQL database management system that provides high performance, high availability, and easy scalability for handling large volumes of data. It falls under the category of document-oriented databases, which means it stores data in flexible, JSON-like documents instead of traditional table-based relational database structures.

The retrieved data is stored in a Mongo DB based on user authorization. If the data already exists in the database, it can be overwritten with user consent. This storage process ensures efficient data management and preservation, allowing for seamless handling of the collected data. 

# Mongo DB to MYSQL
MySQL is an open-source relational database management system (RDBMS) that is widely used for managing and organizing structured data. It is a key component in the LAMP stack (Linux, Apache, MySQL, PHP/Python/Perl) and is often used in conjunction with web applications to store and retrieve data. It uses Structured Query Language (SQL) for defining and manipulating the data in the database. SQL is a standard language for interacting with relational databases.

The application allows users to migrate data from MongoDB to a SQL data warehouse. To ensure compatibility with a structured format, the data is cleansed using the powerful pandas library. Following data cleaning, the information is segregated into separate tables, including channels, playlists, videos, and comments, utilizing SQL queries.

# Tools Used
 1. Spyder
 2. Mongo DB
 3. MYSQL Workbench

# Requried Libraries:
1. googleapiclient.discovery
2. Streamlit
3. Pymongo
4. mysql.connector
5. Regular Expression (re)
