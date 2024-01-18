#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup as bs
#import requests_cache
import os
import time

#requests_cache.install_cache('namecheap_cache')
SANDBOX=False

api_username = "username"
api_key = "put your namecheap api key here"
client_ip = "0.0.0.0"
nc_username = "username"

def main(): 
	complete_domain = os.getenv('CERTBOT_DOMAIN')
	parts = complete_domain.split('.') # [SUB, DOMAIN, SLD, TLD]
	domain = parts[-2] + '.' + parts[-1] # SLD.TLD
	subdomain = complete_domain.removesuffix(domain) # SUB.DOMAIN.
	subdomain = subdomain.removesuffix('.') # SUB.DOMAIN
	records = get_host_records(domain)
	records = clean_old_challenges(records, subdomain)
	records = append_challenge_tag(records, subdomain)
	set_host_records(domain, records)
	time.sleep(60)

def method_url(cmd_name, *args, **kwargs):
	"""
	Transforms a method name into a request URL.
	Can return either sandbox or live URL.
	"""
	global api_username, api_key, nc_username, client_ip
	sandbox = kwargs.get('sandbox', True)
	if sandbox:
		api_url = "https://api.sandbox.namecheap.com/xml.response"
	else:
		api_url = "https://api.namecheap.com/xml.response"
	
	params = { 'ApiUser': api_username, 'ApiKey': api_key, 'UserName': nc_username, 'ClientIp': client_ip, 'Command': cmd_name }
	return api_url, params

def get_host_records(domain):
	"""
	Return list of <Host> elements.
	Does not yet support mutlipart TLDs.
	"""
	url, args = method_url("namecheap.domains.dns.getHosts", sandbox=SANDBOX)
	[SLD, TLD] = domain.split('.')
	args['SLD'] = SLD
	args['TLD'] = TLD
	result = requests.get(url, params=args).text
	soup = bs(result, 'xml')
	hosts = soup.find_all('host')
	return hosts

def clean_old_challenges(records, subdomain):
	"""
	Removes all old _acme-challenge TXT tags.
	Returns list of <Host> elements,
	but without any challenge tags.
	"""
	record_name = "_acme-challenge"
	if (subdomain):
		record_name = record_name + '.' + subdomain

	for record in records.copy():
		if record['Name'] == record_name:
			records.remove(record)
	return records

def append_challenge_tag(records, subdomain):
	"""
	Generate a new challenge tag and append to records.
	Returns list of <Host> elements,
	with a new challenge tag appended.
	"""
	record_name = "_acme-challenge"
	if (subdomain):
		record_name = record_name + '.' + subdomain
	
	challenge = os.getenv('CERTBOT_VALIDATION')
	challenge_soup = bs(f'<Host Name="{record_name}" Type="TXT" Address="{challenge}" TTL="60"', 'xml')
	challenge_tag = challenge_soup.Host
	records.append(challenge_tag)
	return records

def set_host_records(domain, records):
	"""
	Updates records for domain.
	Currently only cares about name, type, address, and optional ttl.
	"""
	url, args = method_url("namecheap.domains.dns.setHosts", sandbox=SANDBOX)
	[SLD, TLD] = domain.split('.')
	args['SLD'] = SLD
	args['TLD'] = TLD
	args['EmailType'] = 'MX' # For manual MX setup. Lookup documentation if your config is different.

	n = 1
	for record in records:
		args[f'HostName{n}'] = record['Name']
		args[f'RecordType{n}'] = record['Type']
		args[f'Address{n}'] = record['Address']
		if 'TTL' in record.attrs:
			args[f'TTL{n}'] = record['TTL']
		if 'MXPref' in record.attrs:
			args[f'MXPref{n}'] = record['MXPref']
		n += 1
	
	result = requests.get(url, params=args).text
	soup = bs(result, 'xml')
	success = soup.DomainDNSSetHostsResult["IsSuccess"] == "true"
	if success:
		print("Namecheap API hook: records successfully updated.")

if __name__ == "__main__":
	main()
