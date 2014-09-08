Title: DNAT
Date: 2014-08-23 22:20
Modified: 2014-08-24 23:15
Category: Implementation Options
Tags:  dnat, firewall
Slug: dnat
Authors: Jens Neuhalfen
Summary: Using the firewall to access backend systems via DNAT.
SortOrder: 20

A possibility to give operators SSH access to backed systems is to use Port *DNAT*. With Port DNAT, a host exposed to the internet [DNATs](http://en.wikipedia.org/wiki/Network_address_translation#DNAT) some of its ports to the backed systems. E.g. `public-ip:2224` is forwarded to `db-server:22`, and `public-ip:2222` is forwarded to `app-server:22`. To access the DB server the operator points ssh to the public ip, e.g. `ssh public-ip -p2224`.


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

iptables -t nat -I PREROUTING -i ${FIREWALL_EXTERNAL_IF} -p tcp --dport ${EXTERNAL_SRC_PORT}  -m state --state NEW -j DNAT --to ${BACKEND_SERVER}:22

```

Connecting to the database server from the internet is done by sshing to the specific port: 

```bash
# run on the operators system

ssh public-ip -p2224
```

#### Adding a new user
New users are only added to the backend systems.

### Evaluation

An evaluation of each of the requirements stated is given, and summarized in the result

- _fully_ fulfills the requirement,
- _partially_ fulfills the requirement
- _no_ or inadequate fulfillment of the requirement

####  **REQ 1:** From the internet to the backend
_An operator can access the backend system from the internet (via ssh)._

The  solution  _fully_  fulfills the requirement. In the example above, the database server is made available to the operator.

####  **REQ 2:** Secured to the end 
_The whole connection from the operators system (internet) to the backend system must be secured via SSH._

The  solution  _fully_  fulfills the requirement. In the example above, the database server is accessed by a direct ssh connection.

####  **REQ 3:** no escape for operators 
_Operators must not be able to break out of the system (whereas system administrators might be able to do so)._

This solution does not allow ssh specific restrictions on the firewall. The only restriction is, which hosts are made available to the internet. The  solution  _fully_  fulfills the requirement. 
####  **REQ 4:**Bastion Host
_Only one host shout be exposed to the internet (the *bastion host*)._

The  solution  provides _no_  solution to this requirement. In the example above, the database server is directly made available to any one on the internet.

#### **REQ 5:** Fine grained permissions
_Certain options should be configurable on the bastion host on a per user and system base (e.g. allow `scp`, `sftp`, or `port forwarding` for user X to system Y)._

The  solution  provides _no_  solution to this requirement, the connection is directly made to the backend systems.

####  **REQ 6:** Robustnes
_Configuration and management should be robust. It should be easy for the administrator to execute a given task (e.g. create new user, add a new backend system) but difficult to bring the system in an inconsitent state._

The  solution  _fully_  fulfills the requirement. Only a single system (the firewall) needs to be modified.

####  **REQ 7:** Four eyes principle for usermanagement
_It should be impossible for the administrator of a single system to grant a new operator/administrator access from the internet._

The  solution  provides _no_  solution to this requirement. Once the backend system is exposed to the internat, an operator on the backend system can give new users access.

####  **REQ 8:**  Port forwarding from the client
_The operator should be able to use SSH port forwarding from his workstation to the backend systems._

The  solution  _fully_  fulfills the requirement. In the example above, the database server is accessed by a direct ssh connection.

####  **REQ 9:** scp to the backend
_The operator should be able to use scp from his workstation to the backend systems._

The  solution  _fully_  fulfills the requirement. In the example above, the database server is accessed by a direct ssh connection.

####  **REQ 10:** Auditable
_All communication must be monitored in such a way that a forensic analysis is possible at a later time (audit)_

The  solution  provides _no_  solution to this requirement. In the best case, the firewall logs can be used to determine, which ip addresses have accessed the backend systems from the internet.

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
* [iptables](http://www.netfilter.org/)
* [NATing](https://en.wikipedia.org/wiki/Network_address_translation)
