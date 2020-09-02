import requests
from os import getenv
import exceptions

class Database():
	def __init__(self, url=None):
		
		if not url:
			self.url = getenv("REPLIT_DB_URL")
		else:
			self.url = url
		if self.url is None:
			raise exceptions.ReplitDBNotEnabled("Repl.it database is not enabled or the url could not be found")
	def get_key(self, key):
		val = requests.get(self.url + '/' + key).text
		return (val, bool(val))




	def set_key(self, keys):
		for key, val in keys.items():
			resp = requests.post(self.url, data={key:val})
			if resp.status_code != 200:
				raise exceptions.ReplitDBGeneralError(f"Could not set {key} to {val}: response: {resp.status_code}")


	def delete_key(self, key):

		resp = requests.delete(self.url  + '/' + key).status_code
		if resp != 200:
			raise exceptions.ReplitDBGeneralError(f"Could not delete {key}: response: {resp.status_code}")

	def list_keys(self, key=""):
		return requests.get(f'{self.url}?prefix={key}').text.split('\n')
	
	def list_keys_values(self):
		kv  = {}
		keys = self.list_keys()
		for key in keys:
			kv[key] = self.get_key(key)
		return kv