# Network-Monitor
Network Monitor in Python 👨‍💻

# Disclaimer: 
Programmes like these are to be used on networks you have explicit permission to test. I WILL NOT BE RESPONSIBLE FOR MISUSE OF THIS SOFTWARE!

## NOTE: Make Sure nmap is installed and is accesible in the terminal
## *Written in python 3.8.5*

# Installation on Windows:
* `git clone https://github.com/jmarcantony/Network-Monitor.git`
* `cd Network-Monitor`
* `python main.py`

# Installation on Linux and Unix like OS:
* `git clone https://github.com/jmarcantony/Network-Monitor.git`
* `cd Network-Monitor`
* `python3 main.py`

# Docs:
## --create-config:
###  Description:
    Creates or resets data in config file
###  Usage:
	python main.py --create-config

## How To Monitor Adresses:
### Do you want to get notified when a device you want to monitor conncets or disconncets from you're network, you can do so by tweaking the config json file
#### By default the config file should be named 'network_monitor_config.json'. The base file should like this
	{
		"delay": 5,
		"hosts_to_monitor": {}
	}
#### You can add a host to monitor by adding a host object to the "hosts_to_monitor" key.
#### eg. 1: lets say you want to monitor 192.168.0.1, the config file should look like this
	{
		"delay": 5,
		"hosts_to_monitor": {
			"192.168.0.1": {
				"ringtone": "[PATH TO RINGTONE]",
				"alert_on_leave": true
			}
		}
	}

#### eg. 2: lets say you want to monitor 192.168.0.1 and 192.168.0.2, the config file should look like this
	{
		"delay": 5,
		"hosts_to_monitor": {
			"192.168.0.1": {
				"ringtone": "[PATH TO RINGTONE]",
				"alert_on_leave": true
			},
			"192.168.0.2": {
				"ringtone": "[PATH TO RINGTONE]",
				"alert_on_leave": false
			}
		}
	}

#### You can keep adding more host objects while following the appropraite json format

#### For the host object you must give 2 required fields, the 'ringtone' and 'alert_on_leave'

### 'ringtone' field:
#### The ringtone field should be the path of the audio file when a device connects or disconnects from you're network.

### 'alert_on_leave' field:
#### This field should be a boolean value where you can set it true if you want to get notified when the device disconnects or false if you do not want to get notified when the device disconnects 