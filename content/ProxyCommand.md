Title: ProxyCommand
Date: 2014-08-23 22:20
Modified: 2014-08-24 23:15
Category: Implementation Options
Tags: about, overview, ProxyCommand
Slug: proxy_command
Authors: Jens Neuhalfen
Summary: The SSH `ProxyCommand` is a configuration that tells the SSH client how to make the connection to the SSH server.  
SortOrder: 30

**WORK IN PROGRESS**

Solution in detail
====================

In the following sections the solution ideas from above are explained, and analysed. The discussed implementations are examples, and can be varied by a great deal.

An evaluation of each of the requirements stated is given, and summarized in the result

- _fully_ fulfills the requirement,
- _partially_ fulfills the requirement
- _no_ or inadequate fulfillment of the requirement


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
