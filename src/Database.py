from sqlalchemy import create_engine, Column,Integer,String,TEXT,CHAR,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

Base = declarative_base()

# Replace 'your_username', 'your_password', 'your_host', 'your_database' with your actual MySQL credentials
DATABASE_URL = "mysql://your_username:your_password@your_host/your_database"

engine = create_engine(DATABASE_URL, echo=True)

""" Create the table """
Base.metadata.create_all(bind=engine)

""" Inserting data """
Session = sessionmaker(bind=engine)

""" Email Model class """
class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    mail_thread_id = Column(String(100), nullable=False, comment='Email unqiue theard ID of the sender')
    sender = Column(String(100), nullable=False, comment='Email ID of the sender')
    status = Column(CHAR(1), nullable=False, comment='Status of the email U - UNREAD, R - READ')
    subject = Column(String(255), nullable=False, comment='Email subject contents')
    mail_rec_time = Column(TIMESTAMP, nullable=False, comment='Email received time stamp')
    body = Column(TEXT, comment='Body contents of the email')
    
    """ Inserting the email informations into the DB """
    def insert_emails_db(self,session,email_dicts):
        try:
            new_email = Email(**email_dicts)
            session.add(new_email)
        except (Exception) as e:
            print(f'Email -> insert_emails_db_error -> {e}')
    
    """ Fetching the email informations from the DB """
    def fetch_email_db(self,db_query):
        results = []
        session = Session()
        try:
            db_query = text(db_query)
            results = session.execute(db_query).fetchall()
        except (Exception) as e:
            print(f'Email -> fetch_email_db_error -> {e}')
        session.close()
        return results
    
    def generate_sql_query(self,root_predicate, rules):
        try:
            """ Define the base SQL query """
            base_query = "SELECT distinct mail_thread_id FROM emails"

            """ Generate the WHERE clause based on the rules """
            conditions = []
            for rule in rules:
                field = rule["field"]
                predicate = rule["predicate"]
                value = rule["value"]
                
                """ 
                    If:   Handle string type fields
                    elif: Handle date type field (Received) - Less than / Greater than for days / months
                    else: Raise Error message
                """
                if predicate in ["contains", "does not contain", "equals", "does not equal"]:
                    if predicate == "contains":
                        condition = f"{field} LIKE '%{value}%'"
                    elif predicate == "does not contain":
                        condition = f"{field} NOT LIKE '%{value}%'"
                    elif predicate == "equals":
                        condition = f"{field} = '{value}'"
                    elif predicate == "does not equal":
                        condition = f"{field} != '{value}'"
                elif predicate in ["less than", "greater than"]:
                    operator = ">=" if predicate == "less than" else "<"
                    condition = f"{field} {operator} DATE_SUB(NOW(), INTERVAL {value} DAY)"
                    # else:
                    #     condition = f"{field} < DATE_SUB(NOW(), INTERVAL {value} DAY)"
                        
                    # condition = f"{field} {operator} DATE_SUB(NOW(), ' INTERVAL {value} DAY')"
                else:
                    raise ValueError(f"predicate value is invalid: {predicate}")
                conditions.append(condition)
            
            """ Join conditions based on the root_predicate """
            if root_predicate == "ALL":
                where_clause = " AND ".join(conditions)
            elif root_predicate == "ANY":
                where_clause = " OR ".join(conditions)
            else:
                raise ValueError("root_predicate value is invalid, use 'ALL' or 'ANY' only.")
            full_query = f"{base_query} WHERE {where_clause}"
            return full_query
        except (Exception) as e:
            print(f'Email -> generate_sql_query_error -> {e}')
            return ""


"""
def testInsertion():
    try:
        session = Session()

        # Example of inserting an email
        new_email = Email(sender="example@email.com", subject="Test Subject", timestamp=datetime.now())
        session.add(new_email)
        session.commit()

        # Querying data
        emails = session.query(Email).all()
        
        for email in emails:
            print(f"Email ID: {email.id}, Sender: {email.sender}, Subject: {email.subject}, Timestamp: {email.timestamp}")

        # Close the session
        session.close()
    except (Exception) as e:
        print(f'Email session error - {e}')
"""
