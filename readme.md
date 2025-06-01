# Out-of-Band Configuration Script
### This is an experimental script for configuring out-of-band management systems. It currently supports HPE iLO 5 with plans to support iDRAC 9 and Lenovo XCC in the near future.

## Installation
Ensure you have Git and Python 3 installed. From a terminal, run the following commands:
```
git --version
python3 --version
```
### Windows 10, 11
If the above commands do not return a version number (or return Python 2), install Git and Python 3 using winget:
```
winget install -e --id Git.Git
winget install -e --id Python.Python.3.11
```
**Note**: Python 3 may be aliased to `python` or `py` on your system. In that case, replace `python3` in the commands below with the appropriate command for your system.

From a terminal, clone the repository and `cd` into its directory:
```
> git clone https://github.com/techietristan/cohesity_ipmi_config.git
> cd cohesity_ipmi_config
```
Install any modules required by the script:
```
pip3 install -r requirements.txt
```

## Usage
To run the script interactively, use `python` to run the script without any arguments:
```
python3 .
```
**Note**: Ensure that you have navigated to the script's directory in your terminal before running this command.

Supply the configuration for the first iLO and enter `y` to confirm the information is correct.

**Note**: 
* iLO default passwords are unique to each server and can be found on a sticker on top of the chassis and usually on a pull-out tab on the front of the server as well. You will be prompted to enter (or scan) the password for the currently connected iLO for each configuration.
* You can enter the subnet mask in dotted decimal (e.g. `255.255.255.128`) or CIDR format (e.g. `/25`).
* The default gateway will be suggested automatically based on the first available IP in the subnet you specify. Simply hit the 'Enter' key to accept the suggested gateway.

```
Welcome to the Out-of-Band configuration script!
Please enter the static IP to set for the iLO: 192.168.1.130
Please enter the hostname to set for the iLO: test_hostname001
Please enter the subnet mask to set for the iLO (dotted decimal or CIDR format): 25
Please enter the default gateway to set for the iLO (press Enter to use 192.168.1.129): 
Please enter the domain name to set for the iLO: my.test.domain.net
Please enter the username to set for the iLO: test_user
Please enter the password to set for the iLO: 
Please enter the password again: 

Do you want to push the following config to the currently connected iLO?

	 Static IP: 192.168.1.130
	 Hostname: test_hostname001-r
	 Subnet Mask: 255.255.255.128
	 Default Gateway: 192.168.1.129
	 Domain: my.test.domain.net
	 Username: test_user
	
(y or n): y
```
Once the configuration is successfully pushed to the iLO, the hostname and IP address will automatically be incremented and you'll be prompted to connect to the next iLO