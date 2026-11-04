"""Module for CRUD operations in a MongoDB collection.

Developer: Jenna Gorham
"""

from pymongo import MongoClient 
from bson.objectid import ObjectId

class CollectionManager(object): 
    """CRUD operations for a MongoDB collection.
    
    Attributes:
        client (MongoClient): Connection to MongoDB.
        database (Database): MongoDB database.
        collection (Collection): Database collection.
    """ 

    def __init__(self, username, pwd, db, col, host, port): 
        """Initialize a CollectionManager object.
        
        Parameters:
            username (str): Database username credential.
            pwd (str): Database password credential.
            db (str): Name of database.
            col (str): Name of collection in database.
            host (str): Host domain of database.
            port (int): Port corresponding to host.
        
        Raises:
            TypeError: Incorrect data type for database credentials.
        """
        # Validate input
        if not isinstance(username, str):
            raise TypeError("Username must be a string.")
        if not isinstance(pwd, str):
            raise TypeError("Password must be a string.")
        if not isinstance(db, str):
            raise TypeError("Database name must be a string.")
        if not isinstance(col, str):
            raise TypeError("Collection name must be a string.")
        if not isinstance(host, str):
            raise TypeError("Host must be a string.")
        if not isinstance(port, int):
            raise TypeError("Port must be an integer.")
        
        # Initialize Connection 
        
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (username, pwd, host, port)) 
        self.database = self.client['%s' % (db)] 
        self.collection = self.database['%s' % (col)] 
            
    def create(self, data):
        """Create a document in the collection.
        
        Parameters:
            data (dict): Document to insert.
            
        Returns:
            bool: Whether insert was successful.
            
        Raises:
            TypeError: Incorrect data type for query.
        """
        # Validate input
        if data is None:
            raise TypeError("Data parameter must be non-empty.")
        if not isinstance(data, dict):
            raise TypeError("Data parameter must be a dictionary.")
        
        # Query database to insert document
        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except Exception as e:
            print(f"The following error occurred: {e}")
            return False

    def read(self, query):
        """Query the collection for documents.
        
        Parameters:
            query (dict): Key/value lookup pairs.
            
        Returns:
            list: Documents returned by query.
        
        Raises:
            TypeError: Incorrect data type for query.
        """
        # Input validation
        if query is None:
            raise TypeError("Query parameter must be non-empty.")   
        if not isinstance(query, dict):
            raise TypeError("Query parameter must be a dict")
        
        # Query database to read documents
        try:
            cursor = self.collection.find(query)
            # The PyMongo find() method returns a cursor object
            # This must be handled and converted to a list
            return list(cursor)
        except Exception as e:
            print(f"The following error occurred: {e}")
            return []
    
    def update(self, filter_query, update_query):
        """Update documents in the collection.
        
        Parameters:
            filter_query (dict): Criteria to select documents for update.
            update_query (dict): Updates to perform on selected documents.
            
        Returns:
            int: Number of documents modified.
            
        Raises:
            TypeError: Incorrect data type for query.
        """
        # Input validation
        if filter_query is None:
            raise TypeError("Filter query parameter must be non-empty.")
        if not isinstance(filter_query, dict):
            raise TypeError("Filter query parameter must be a dict.")
        if update_query is None:
            raise TypeError("Update query parameter must be non-empty.")
        if not isinstance(update_query, dict):
            raise TypeError("Update query parameter must be a dict.")
        
        # Query database to update documents
        try:
            result = self.collection.update_many(filter_query, update_query)
            return result.modified_count
        except Exception as e:
            print(f"The following error occurred: {e}")
            return 0
    
    def delete(self, filter_query):
        """Delete documents from the collection.
        
        Parameters:
            filter_query (dict): Criteria to select documents for deletion.
        
        Returns:
            int: Number of documents deleted.
            
        Raises:
            TypeError: Incorrect data type for query.
        """
        # Input validation
        if filter_query is None:
            raise TypeError("Filter query parameter must be non-empty.")
        if not isinstance(filter_query, dict):
            raise TypeError("Filter query parameter must be a dict.")
    
        # Query database to delete documents
        try:
            result = self.collection.delete_many(filter_query)
            return result.deleted_count
        except Exception as e:
            print(f"The following error occurred: {e}")
            return 0
