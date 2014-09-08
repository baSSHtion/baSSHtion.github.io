Title: ProxyCommand
Date: 2014-08-23 22:20
Modified: 2014-08-24 23:15
Category: Implementation Options
Tags: ProxyCommand
Slug: proxy_command
Authors: Jens Neuhalfen
Summary: The SSH `ProxyCommand` is a configuration that tells the SSH client how to make the connection to the SSH server.  
SortOrder: 30

A built in solutions to implement a bastion host is the *ProxyCommand* command of OpenSSH. The proxy command tells the `ssh` client how to connect to the ssh server. 

![]({filename}/images/ProxyCommand.png)

### Example implementation
Setting up ProxyCommand is straight forward and requires an SSH server exposed to the internet (the bastion host). 

An ssh server exposed to the internet should never, ever have other authentication means beside public key authentication enabled. Not only is this much more secure, it also allows a fine grained access control via `forced-command`s. 

The users on the bastion host have the sole responsibility to execute netcat (`nc`) to the backend systems. 

These very restricted permissions of users allows the usage of a technical user account on the bastion host. Using a single, restricted user has the advantage, that this user can be locked down very easy, e.g. by creating a changeroot with only netcat installed.

The example implementation is a script on the bastion host that is run as ssh forced command. Operators connect to backend systems like this:

```config
# ~/.ssh/config

Host app-server.proxy
     User admin
     ProxyCommand    ssh -q -l sshgw bastion.example.org "nc app-server:22"

Host db.proxy
     User admin
     ProxyCommand    ssh -q -l sshgw bastion.example.org "nc db-server:22"
```

```bash
ssh app-server.proxy
```

This` would ssh to `bastion.example.org`. There it would execute netcat, and then try to connect from the client, _through_ the ssh to bastion host,  _through_ the netcat pipe and to the db-server to establish the final ssh connection.

ProxyCommand can best be used by implementing a `forced_command` script on the bastion host. 

#### Forced Command Script on Bastion

All proxy commands are executed by a single user (_sshgw_). This user has the following `.ssh/authorized_keys` file:

```
# ~sshgw/.ssh/authorized_keys
no-port-forwarding,no-pty,no-X11-forwarding,command="/opt/sshgw/sshgw alice" ssh-rsa AAAAB...1234== Alice, Laptop key

no-port-forwarding,no-pty,no-X11-forwarding,command="/opt/sshgw/sshgw alice" ssh-rsa AAAAB...5678== Alice, Workstation key

no-port-forwarding,no-pty,no-X11-forwarding,command="/opt/sshgw/sshgw bob" ssh-rsa AAAAB...abcd== Bob, Workstation key
```

Note that _alice_ has two public keys that allow her to log in.

```bash
#!/bin/bash

# This is /opt/sshgw/sshgw
# - Executable by user sshgw
# - Params
# - $1 : Name of the user. This is passed from the forced command in authorized_keys


### Evaluation

**WORK IN PROGRESS**
