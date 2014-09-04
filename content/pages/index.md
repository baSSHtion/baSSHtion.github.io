Title: Securely administer server via SSH
Date: 2014-08-23 22:20
Modified: 2014-08-24 23:15
Category: ssh
Tags: about, overview
Slug: index
Authors: Jens Neuhalfen
Summary: baSSHtion.org provides administrators the means to effectively implement controlled, and secure SSH access to their systems. It provides tools, and recipes for OpenSSH, and others.
SortOrder: 10
Status: hidden
url: /
save_as: index.html

The basic question answered by baSSHtion.org is:

**How can an operator/administrator securely manage backend servers not directly exposed to the internet?**

Often machines running in private nets need to be administered from the internet. The hypothetical example used here is a moderate complex application running on the internet. This application has a webserver facing to the internet, and a database server plus application servers as backend systems. These machines are administered via SSH. For security reasons it is undesirable to expose the backend systems to the internet. 

Several solutions to this problem statement are dicussed here.

![Setup used for examples.]({filename}/images/Overview.png)

Managing such a setup relies on (at least) two roles: _Application Operators_ (short: _operator_) that manage the applications on the backend systems (but do not manage the operating system), and _System Administrators_ (short: _administrator_) that manage the operating system (including user management, and SSH). System Administrators have access to the role of `root`, whereas operators don't have this role. Distinguishing between these roles allows for a better reasoning in terms of access control, even if these roles are often carried out by the same person.

Basic Requirements
----------------------

These are the basic requirements that each of the solutions is evaluated against:

- **REQ 1: _Secured to the end_** The whole connection from the operators system (internet) to the backend system must be secured via SSH.
- **REQ 2: _no escape for operators_** Operators must not be able to break out of the system (whereas system administrators might be able t do so). What _breaking out_ means depends on the solution but it basically means, that the operator has to follow the rules set by the system administrator.
- **REQ 3: _Bastion Host_** Only one host shout be exposed to the internet (_bastion host_). This is the core means to prevent internet access to the backend systems.

Solutions
----------------------

There exist several possibilities to allow operators to access the backend systems. Some of the more popular solutions are:

1. [Port *DNAT*]({filename}/DNAT.md), where a host exposed to the internet [DNATs](http://en.wikipedia.org/wiki/Network_address_translation#DNAT) some of its ports to the backed systems. E.g. `public-ip:2224` is forwarded to `db-server:22`, and `public-ip:2222` is forwarded to `app-server:22`. To access the DB server the operator points ssh to the public ip, e.g. `ssh public-ip -p2224`.
2. A built in solutions is the [*ProxyCommand*](ProxyCommand.md) to provide the connection to the backend system (e.g. `ssh public-ip -o ProxyCommand "nc app-server 22"`)
3. [*Jump Host with interactive session*]({filename}/JumpHostInteractive.md), where a host exposed to the internet provides SSH access with an interactive terminal. Operators connect to this host, and then manually open a new SSH connection to the next host. Authentication on the backend hosts is (often) done via agent forwarding to prevent storing secret keys on the exposed machine. E.g. `ssh -A public-ip` and there `ssh db-server`.
4. [*Jump Host without interactive session*]({filename}/JumpHostNonInteractive.md), as above but without an interactive session (shell) on the bastion host. When system administrators connect to this host a new SSH connection to the next host is automatically opened via a _forced command_. Authentication on the backend hosts is done via agent forwarding. E.g. `ssh -A public-ip app-server`.
5. [*Other solutions*]({filename}/others.md)

All of these solutions fulfil the requirement of a single exposed host, though in practice additional requirements are identified.

Extended Requirements
----------------------

When the system gets larger, and/or handles sensitive data, additional requiremens emerge:

- **REQ 4: _Auditable_** All communication must be monitored in such a way that a forensic analysis is possible at a later time (audit)
- **REQ 5: _Fine grained permissions_** Certain options should be configurable on a per user and system base (e.g. allow `scp`, `sftp`, or `port forwarding` for user X to system Y).
- **REQ 6: _Robustness_** Configuration and management should be robust. It should be easy for the administrator to execute a given task (e.g. create new user, add a new backend system) but difficult to bring the system in an inconsitent state.
- **REQ 7: _Four eyes principle for usermanagement_** It should be impossible for the administrator of a single system to grant a new operator/administrator access from the internet.
- **REQ 8: _Port forwarding from the client_** The operator should be able to use SSH port forwarding from his workstation to the backend systems.
- **REQ 9: _scp to the backend_** The operator should be able to use scp from his workstation to the backend systems.


Wording
----------
* **Administrator** : The role responsible for managing the access control system (and the operating system). Can add/delete users on all systems. Has `root` access to all machines.
* **Operator** : A user responsible for managing the application. Has accounts on the backend systems, potentially even `root`.  An operator *might* have accounts on the bastion host, but never with `root` level access.
* **SSH** : The OpenSSH tools (client/server) or protocol. SSHv1 is not considered.
* **`ssh`** : The OpenSSH SSH client.



# Ressources
* [RFC 4251: SSH architecture](http://datatracker.ietf.org/doc/rfc4251/?include_text=1)
* [RFC 4252: Authentication](http://datatracker.ietf.org/doc/rfc4252/?include_text=1)
* [RFC 4253: Transport Layer](http://datatracker.ietf.org/doc/rfc4253/?include_text=1)
* [RFC 4254: Connection Protocol](http://datatracker.ietf.org/doc/rfc4254/?include_text=1)
