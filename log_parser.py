import requests
import re

from rich.console import Console
from rich.table import Table

# sample OpenSSH log 
url = 'https://raw.githubusercontent.com/logpai/loghub/refs/heads/master/OpenSSH/OpenSSH_2k.log'

# use a streaming request API to better support larger files
def get_stream(url, log_output_processor, state_register, callback):
    response = requests.get(url, stream=True, timeout=10)

    if response.ok:
        try:
            for line in response.iter_lines():
              if line:
                  log_output_processor(line.decode('utf-8'), state_register)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during streaming: {e}")
        finally:
            response.close()            
            callback(state_register)
    else:
        response.raise_for_status()
        
def find_ip_address(line):
    pattern = r'(\d{1,3}\.){3}\d{1,3}'
    match = re.search(pattern, line)
    if match:
        return match.group(0)
    return '<missing>'

def find_username(line):
    if 'user' in line:
        pattern = r'(?<=user )\w+'
        match = re.search(pattern, line)
        if match:
            return match.group(0)    
    return '<missing>'

def log_line_processor(line, state_register):
    # Example:
    #   Dec 10 07:07:45 LabSZ sshd[24206]: Failed password for invalid user test9 from
    
    if 'Failed password' in line:
      ip_address = find_ip_address(line)
      username = find_username(line)

      failed_ip_addresses_for_user = state_register.get(username, {})
      ip_count = failed_ip_addresses_for_user.get(ip_address, 0)
      failed_ip_addresses_for_user[ip_address] = ip_count + 1
      state_register[username] = failed_ip_addresses_for_user
    
def report_analysis(register_failed_logins):
    table = Table(title="Log Report")
    table.add_column("Username", justify="left", style="cyan", no_wrap=True)
    table.add_column("I.P Address", style="magenta")
    table.add_column("Failure Count", justify="right", style="green")

    for username, ip_addresses in register_failed_logins.items():
        print(f"User: {username}")
        for ip_address, count in ip_addresses.items():
            print(f"  IP Address: {ip_address}, Count: {count}")        
            table.add_row(username, ip_address, str(count))
    
    print("Total failed logins:", sum([sum(ip_addresses.values()) for ip_addresses in register_failed_logins.values()]))
    print("Unique users:", len(register_failed_logins))
    print("Unique IP addresses:", sum([len(ip_addresses) for ip_addresses in register_failed_logins.values()]))

    console = Console()
    console.print(table)
    
    
if __name__ == "__main__":
  register_failed_logins = {}
  get_stream(url, log_line_processor, register_failed_logins, report_analysis)
  