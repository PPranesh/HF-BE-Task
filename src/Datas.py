from datetime import datetime
import base64,json
import pandas as pd

EXP_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

class Datas:
	def __init__(self):
		pass

	@staticmethod
	def formatting_datetime_values(date_string):
		try:
			""" 
				Cleaning datetime strings by removing additional timezone information, 
				e.g., (IST), etc. 
			"""
			_date_string_cleaned = date_string.split('(')[0].strip()
			
			date_obj =  datetime.strptime(_date_string_cleaned, '%a, %d %b %Y %H:%M:%S %z')
			return date_obj.strftime(EXP_TIME_FORMAT)
		except (Exception) as e:
			print(f" Exception occured in Datas -> formatting_datetime_values -> {e}")
			return None
	
	@staticmethod
	def body_contents(parts):
		try:
			_data = parts['body']['data'] if parts else None
			if _data is not None:
				_data = _data.replace("-","+").replace("_","/")
				return base64.urlsafe_b64decode(_data.encode('UTF-8')).decode('utf-8')
			return _data
		except (Exception) as e:
			print(f" Exception occured in Datas -> body_contents -> {e}")
			return "Data is not readable"
	
	@staticmethod
	def ORM2JSON(query,return_type='J'):
		df = pd.DataFrame(query)
		if df.empty:
			return []
		result = json.loads(df.to_json(orient='records',default_handler=str))
		del df
		try:
			if return_type == 'J':
				return result
			if return_type == 'P':
				return pd.DataFrame(result)
			return result
		except Exception as e:
			print(f"ORM2JSON - {str(e)}")
		return result
			
    