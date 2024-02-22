import json

from dataclasses import dataclass
from GmailAPI import GmailAPI
from Database import Email

@dataclass
class EmailRule:
    id: str
    predicate: str
    conditions: list
    actions: list

@dataclass
class Condition:
    field: str
    predicate: str
    value: str

@dataclass
class Action:
    type: str

class EmailProcessor:
	def __init__(self, gmail_api):
		self.gmail_api = gmail_api
		self.rules = []
	
	def generate_sql_query(self,root_predicate, rules):
		try:
			""" Define the base SQL query """
			base_query = "SELECT mail_thread_id FROM emails"

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
					operator = "<" if predicate == "less than" else ">"
					condition = f"{field} {operator} DATE('now', '-{value} days')"
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
			print(f" EmailProcessor -> generate_sql_query_error - {e}")
	
	def load_rules_from_file(self, rules_file='../config/rules.json'):
		try:
			with open(rules_file, 'r') as file:
				raw_rules = json.load(file)
			
			for raw_rule in raw_rules:
				rule = EmailRule(**raw_rule)
				self.rules.append(rule)
		except (Exception) as e:
			print(f" EmailProcessor -> load_rules_from_file_error - {e}")
	
	def execute_rules(self,run_rule="Rule1"):
		try:
			for rule in self.rules:
				if rule.id==run_rule:
					print("*** "*3)
					print(f"Applying rule ID - {rule.id}")
					print(f"Applying rule.predicate - {rule.predicate}")
					print(f"Applying rule.conditions - {rule.conditions}")
					print(f"Applying rule.actions - {rule.actions}")
					print("*** "*3)
					email_obj = Email()
					sql_query = email_obj.generate_sql_query(rule.predicate, rule.conditions)
					email_datas = email_obj.fetch_email_db(sql_query)
					print("email_datas => ",email_datas)
					
					if email_datas:
						return self.gmail_api.apply_actions(email_datas, rule.actions)
					print("No email datas found for the rules!!")
					return "No email datas found for the rules!!"
		except (Exception) as e:
			print(f'EmailProcessor -> execute_rules_error -> {e}')
			return "Error in rules execution"

if __name__ == "__main__":
	gmail_api = GmailAPI()
	gmail_api.authenticate(scopes=["https://mail.google.com/"])
	
	email_processor = EmailProcessor(gmail_api)
	email_processor.load_rules_from_file()
	
	email_processor.execute_rules()
	# email_processor.execute_rules(run_rule="Rule3")