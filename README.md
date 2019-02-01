[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/victoriancode/amp4endpoint)
# AMP for Endpoints - Duplicate Fixer
This python script is intended to delete duplicated AMP for EndPoint hostnames.



The script executes as follows: Enter AMP4E -API Credentials -> Search all hostnames -> Create hostname duplicate list -> Query duplicate install date -> delete dated hostname. After the script runs, check AMP4E Console > Accounts > Audit Log, for changes the script performed.

Use Case: Host machine is wiped, new machine installs new AMP4EP connector. AMP4EP Console displays 2 licenses, one for wiped machine as well as new machine. Script deletes older machine plus GUID with matching hostnames.

Authors: Max Wijnbladh and Chris Maxwell

Video Demo: https://youtu.be/jXujBqelfLU

## UML for script

![](AMP4EP_Duplicator.png)
