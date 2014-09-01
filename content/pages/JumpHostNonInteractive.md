Title: JumpHost/non-interactive
Date: 2014-08-23 22:20
Modified: 2014-08-24 23:15
Category: ssh
Tags: about, overview, jumphost, interactive
Slug: jump_host_non_interactive
Authors: Jens Neuhalfen
Summary: Using the bastion host to access backend systems via the  bastion host, but without an interactive session on the bastion host.
SortOrder: 50


Solution in detail
====================

In the following sections the solution ideas from above are explained, and analysed. The discussed implementations are examples, and can be varied by a great deal.

An evaluation of each of the requirements stated is given, and summarized in the result

- _fully_ fulfills the requirement,
- _partially_ fulfills the requirement
- _no_ or inadequate fulfillment of the requirement



## Jump Host without interactive session

![]({filename}/images/JumpHost-ForcedCommand.png)

### Example implementation

```
ssh -t -A public-ip "script -c 'ssh db-server'" 
```

 or, more elaborate:

```
ssh -t -A 127.0.0.1 "script -c 'ssh db.server' --timing=/tmp/script.timing /tmp/script.log" 
```

Replaying the recorded session:
```
 scriptreplay --timing=/tmp/script.timing /tmp/script.log
```

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
