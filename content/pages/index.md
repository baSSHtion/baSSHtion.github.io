Title: About baSSHtion
Date: 2014-08-23 22:20
Modified: 2014-08-24 23:15
Category: ssh
Tags: about, overview
Slug: index
Authors: Jens Neuhalfen
Summary: baSSHtion.org provides administrators the means to effectively implement controlled,and secure access to their hosted applications. It provides tools, and recipes for OpenSSH, and others.
url: 
save_as: index.html


Often machines running in private nets need to be administered from the internet. The hypothetical example used here is a moderate complex application running on the internet. This application has a webserver facing to the internet, and a database server plus the application servers as backend systems. These machines are administered via SSH. For security reasons it is undesirable to expose the backend systems to the internet. Several solutions to this problem statement are dicussed here.

![]({filename}/images/Overview.png)

Managing such a setup relies on (at least) two roles: Application Operators (short: operator) that manage the applications on the backend systems (but do not manage the operating system), and System Administrators (short: administrator) that manage the operating system (including user management, and SSH). System Administrators have access to the role of `root`, whereas operators don't have this role. Distinguishing between these roles allows for a better reasoning in terms of access control, even if these roles are often carried out (*TODO: richtiges Wort?*) by the same person.

There exist several possibilities to allow operators to access the backend systems. The following options are often use to achieve this (follow the links for examples):

1) [Port *DNAT*](DNAT.md), where a host exposed to the internet DNATs some of its ports to the backed systems. E.g. `public-ip:2224` is forwarded to `db-server:22`, and `public-ip:2222` is forwarded to `app-server:22`. The operator points ssh to the public ip, e.g. `ssh public-ip -p2224` to transparently ssh to `db-server`.
2) A variant of Jump Hosts is using [*ProxyCommand*](ProxyCommand.md) to skip the step of opening a shell on the jump host. (e.g. `ssh public-ip -o ProxyCommand "nc app-server 22"`)
3) [*Jump Host with interactive session*](JumpHost.md), where a host exposed to the internet provides SSH access. System administrators connect to this host, and then manually open a new SSH connection to the next host. Authentication on the backend hosts is (often) done via agent forwarding to prevent storing secret keys on the exposed machine. E.g. `ssh -A public-ip` and there `ssh db-server`.
4) [*Jump Host without interactive session*](JumpHost.md), as above but without an interactive session (shell) on the bastion host. When system administrators connect to this host a new SSH connection to the next host is automatically opened via a _forced command_. Authentication on the backend hosts is done via agent forwarding. E.g. `ssh -A public-ip app-server`.

All of these solutions fulfil the requirement of a single exposed host, though in practice additional requirements are identified.

Extended Requirements
----------------------

When the system gets larger, and/or handles sensitive data, the said solutions lack some requirements. 

- **REQ 1: _Bastion Host_** Only one host shout be exposed to the internet (_bastion host_). This is the core means to prevent internet access to the backend systems.
- **REQ 2: _Auditable_** All communication must be monitored in such a way that a forensic analysis is possible at a later time (audit)
- **REQ 3: _Fine grained permissions_** Certain options should be configurable on a per user and system base (e.g. allow `scp`, `sftp`, or `port forwarding`).
- **REQ 4: _Robustness_** Configuration and management should be robust. It should be easy for the administrator to execute a given task (e.g. create new user, add a new backend system) but difficult to bring the system in an inconsitent state.
- **REQ 5: _Four eyes principle for usermanagement_** It should be impossible for the administrator of a single system to grant a new operator/administrator access from the internet.
- **REQ 6: _Port forwarding from the client_** The operator should be able to use SSH port forwarding from his workstation to the backend systems.
- **REQ 7: _scp to the backend_** The operator should be able to use scp from his workstation to the backend systems.


Wording
----------
* SSH : The OpenSSH tools (client/server) or protocol. SSHv1 is not considered.
* `ssh` : The OpenSSH SSH client.



Solutions in detail
====================

In the following sections the solution ideas from above are explained, and analysed. The discussed implementations are examples, and can be varied by a great deal.

An evaluation of each of the requirements stated is given, and summarized in the result

- _fully_ fulfills the requirement,
- _partially_ fulfills the requirement
- _no_ or inadequate fulfillment of the requirement

## Port DNAT

When using Port DNAT to access backend hosts, the backend hosts are partially exposed to the internet. The firewall will forward a port on its external interface to an ssh server running on a backend system. E.g. `public-ip:2224` is forwarded to `db-server:22`, and `public-ip:2223` is forwarded to `app-server:22`. 

![]({filename}/images/DNAT.png)

The operator points ssh to the public ip, e.g. `ssh public-ip -p2222` to transparently ssh to `db-server`.

### Example implementation
Setting up NAT is straight forward and requires a single firewall change per host.  Users are only managed on the backend systems.

#### Adding a new backend host
If the firewall is a Linux host, then the following `iptables` rules for the firewall sever implement the port DNAT from `public-ip:2224` to `db-serv:22`:

```bash
# run on the firewall

FIREWALL_EXTERNAL_IF=eth0
EXTERNAL_SRC_PORT=2224
BACKEND_SERVER=$(hostname db-serv)

# TODO: Implement

iptables -A  ...
```

Connecting to the database server from the internet is done by sshing to the specific port: 

```bash
# run on the operators system

ssh public-ip -p2224
```
#### Adding a new user
New users are only added to the backend systems.

### Evaluation
| Requirement                                    | requirement fulfilled | comment |
|------------------------------------------------|---------|-----------------------------------------------------------------------------------------|
| *REQ 1: Bastion Host*                           | partially | The firewall reduces the attack surface of the backend systems to the ssh port.      |
| *REQ 2: Auditable*                              | no      | Only SSH encrypted traffic passes through the firewall, preventing an audit of the content.|
| *REQ 3: Fine grained permissions*               | no      | The firewall can only restrict communication to specific source/destination addresses. |
| *REQ 4: Robustness*                             | fully   | Changes are limited to one system, making them very robust to carry out.               |
| *REQ 5: Four eyes principle for usermanagement*  | no     | Anybody who can manage users on a backend system can do so alone. Anyone who can administer the firewall can add/remove hosts. |
| *REQ 6: Port forwarding*  | | |
| *REQ 7: scp*  | | |

### Conclusion
#### Strengths
+ Very simple to set up
+ Works well for smaller systems and when the requirements are less strict
+ All SSH sub-protocolls,  and tools work without any changes (`sftp`, port-forwarding, `rsync`, ...)

#### Weaknesses
- Many requirements not fulfilled.
- All backend systems are directly exposed to the internet. This makes patching harder.
- Might get complex, when many backend systems are installed and/or they frequently change (_Which port was server 4711 again?_)

#### Final words

A simple solution for small scale systems with modest requirements regarding security.

#### Additional Ressources
* [iptables](TODO)
* [NATing](TODO)

## Via `ProxyCommand`

An SSH `ProxyCommand` is a configuration that tells the SSH client how to make the connection to the SSH server. When a proxy command is specified for a connection, then SSH
![]({filename}/images/ProxyCommand.png)

### Example implementation
#### Adding a new backend host
#### Adding a new user
### Evaluation
| Requirement                                     | requirement fulfilled | comment |
|-------------------------------------------------|-----------|-----------------------------------------------------------------------------------------|
| *REQ 1: Bastion Host*                           | partially |                                                                                         |
| *REQ 2: Auditable*                              | no        |                                                                                         |
| *REQ 3: Fine grained permissions*               |           |                                                                                         |
| *REQ 4: Robustness*                             |           |                                                                                         |
| *REQ 5: Four eyes principle for usermanagement* |           |                                                                                         |
| *REQ 6: Port forwarding*  | | |
| *REQ 7: scp*  | | |


### Conclusion
#### Strengths
#### Contra
#### Final words

## Jump Host with interactive session

![]({filename}/images/JumpHost.png)

### Example implementation
#### Adding a new backend host
#### Adding a new user
### Evaluation
| Requirement                                     | requirement fulfilled | comment |
|-------------------------------------------------|-----------|-----------------------------------------------------------------------------------------|
| *REQ 1: Bastion Host*                           | partially |                                                                                         |
| *REQ 2: Auditable*                              | no        |                                                                                         |
| *REQ 3: Fine grained permissions*               |           |                                                                                         |
| *REQ 4: Robustness*                             |           |                                                                                         |
| *REQ 5: Four eyes principle for usermanagement* |           |                                                                                         |
| *REQ 6: Port forwarding*  | | |
| *REQ 7: scp*  | | |


### Conclusion
#### Strengths
#### Weaknesses
#### Final words

## Jump Host without interactive session

![]({filename}/images/JumpHost-ForcedCommand.png)

### Example implementation
#### Adding a new backend host
#### Adding a new user
### Evaluation
| Requirement                                     | requirement fulfilled | comment |
|-------------------------------------------------|-----------|-----------------------------------------------------------------------------------------|
| *REQ 1: Bastion Host*                           | partially |                                                                                         |
| *REQ 2: Auditable*                              | no        |                                                                                         |
| *REQ 3: Fine grained permissions*               |           |                                                                                         |
| *REQ 4: Robustness*                             |           |                                                                                         |
| *REQ 5: Four eyes principle for usermanagement* |           |                                                                                         |
| *REQ 6: Port forwarding*  | | |
| *REQ 7: scp*  | | |


## Conclusion
#### Strengths
#### Weaknesses
#### Final words

# Ressources
* [RFC 4251: SSH architecture](http://datatracker.ietf.org/doc/rfc4251/?include_text=1)
* [RFC 4252: Authentication](http://datatracker.ietf.org/doc/rfc4252/?include_text=1)
* [RFC 4253: Transport Layer](http://datatracker.ietf.org/doc/rfc4253/?include_text=1)
* [RFC 4254: Connection Protocol](http://datatracker.ietf.org/doc/rfc4254/?include_text=1)

############################################################################################

## Summary

| Solution / Requirement | single exposed host | auditable | per user configuration | robust | four eyes |
|------------------------|---------------------|-----------|------------------------|--------|-----------|
| DNAT | yes | no, SSH connection is encrypted | yes, in sshd on backend systems | no, configuration spread over multiple machines | no |
| Jump Host | yes | yes (no scp, port forwarding) | yes, via ssh config on bastion | partly (via `~/.ssh/authorized_keys`) | yes |
| ProxyCommand | yes | partly | yes, via ssh config on bastion | partly (via `~/.ssh/authorized_keys`) | yes |

JumpHost
------------

### Interactive Session

### non interactive session
` ssh -t -A public-ip -p 3333 "script -c 'ssh db-server'" `
ssh -t -A 127.0.0.1 -p 3333 "script -c 'ssh 127.0.0.1' --timing=/tmp/script.timing /tmp/script.log" 

 scriptreplay --timing=/tmp/script.timing /tmp/script.log

## MISC
- [Transparent proxy](https://github.com/neuhalje/man-in-the-middle-attack.git) (-> Link auf Projekt)

