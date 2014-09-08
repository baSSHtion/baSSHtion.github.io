Title: SSHv2 internals
Date: 2014-08-23 22:20
Modified: 2014-08-24 23:15
Category: ssh
Tags: rfc
Slug: rfc
Authors: Jens Neuhalfen
Summary: A condensed version of the RFCs that specify SSHv2.
SortOrder: 95

 
The following paragraphs provide a condensed version of the RFCs that specify SSHv2.
 
A good definition of what SSH is comes from the _SSH Protocol Architecture_ [RFC4251](http://datatracker.ietf.org/doc/rfc4251/?include_text-1) (which is a good read to get an overview of SSHv2):
 
>   Secure Shell (SSH) is a protocol for secure remote login and other
>   secure network services over an insecure network.  It consists of
>   three major components:
> 
>   o  The Transport Layer Protocol [SSH-TRANS] provides server
>      authentication, confidentiality, and integrity.  It may optionally
>      also provide compression.  The transport layer will typically be
>      run over a TCP/IP connection, but might also be used on top of any
>      other reliable data stream.
> 
>   o  The User Authentication Protocol [SSH-USERAUTH] authenticates the
>      client-side user to the server.  It runs over the transport layer
>      protocol.
> 
>   o  The Connection Protocol [SSH-CONNECT] multiplexes the encrypted
>      tunnel into several logical channels.  It runs over the user
>      authentication protocol.
> 
>   The client sends a service request once a secure transport layer
>   connection has been established.  A second service request is sent
>   after user authentication is complete.  This allows new protocols to
>   be defined and coexist with the protocols listed above.
 

Graphically the architecture of SSH can be visualized as follows.
 
```
### : SSH-CONNECT SSH connection protocol, RFC4254
+++ : SSH-USERAUTH User authentication, RFC4252
=== : SSH-TRANS Transport layer, RFC4253
 
                                                               
      #### SSH-CONNECT ######### Channel 1 "session" ########### (the channel id is arbitrary)
      #### SSH-CONNECT ######### Channel 2 "tcpip-forward" ##### (              ''           )
               ....
      #### SSH-CONNECT ######### Channel n "..." ############### (              ''           )
 
    ++++++++++++++++ SSH-USERAUTH ++++++++++++++++++++++++++++++++++   (User authentication)
                                              
=============================  SSH-TRANS ============================== (Server authentication & link security)
```                                                                 
 
SSH is designed to be flexible, and modular. The communication between client and server is message based. Algorithms and methods are defined by interfaces (e.g. [USER-AUTH](http://datatracker.ietf.org/doc/rfc4252/?include_text-1)), and identified by string names (see [chapter 6](http://datatracker.ietf.org/doc/rfc4251/?include_text-1)). These names are split into e-mail like namespaces "name@domainname", e.g. "ourcipher-cbc@example.com" or "xyz@openssh.com". Names defined in RFCs have no suffix ("3des-cbc").
 
## SSH-TRANS
 
From the [RFC4253](http://datatracker.ietf.org/doc/rfc4253/?include_text-1):
  
>   The SSH transport layer is a secure, low level transport protocol.
>   It provides strong encryption, cryptographic host authentication, and
>   integrity protection.
> 
>   Authentication in this protocol level is host-based; this protocol
>   does not perform user authentication.  A higher level protocol for
>   user authentication can be designed on top of this protocol.
> 
>   The protocol has been designed to be simple and flexible to allow
>   parameter negotiation, and to minimize the number of round-trips.
>   The key exchange method, public key algorithm, symmetric encryption
>   algorithm, message authentication algorithm, and hash algorithm are
>   all negotiated.  It is expected that in most environments, only 2
>   round-trips will be needed for full key exchange, server
>   authentication, service request, and acceptance notification of
>   service request.  The worst case is 3 round-trips.
 
In summary the connection starts with the _Protocol Version Exchange_ where the server announces its version. Then the key exchange (server keys, not user keys) takes place.
 
After the key exchange the to be used algorithms are negotiated and the client requests a service by its name.
 
The RFC defines two services for the transport protocol:
 
* `ssh-userauth`  - A summary of [RFC4252](http://datatracker.ietf.org/doc/rfc4252/?include_text-1) follows in the next section.
* `ssh-connection` - A summary of [RFC4254](http://datatracker.ietf.org/doc/rfc4254/?include_text-1) is found further below.
 

## SSH-USERAUTH
 

Cited from [RFC4252](http://datatracker.ietf.org/doc/rfc4252/?include_text-1):
 
>   The SSH authentication protocol is a general-purpose user
>   authentication protocol.  It is intended to be run over the SSH
>   transport layer protocol [SSH-TRANS].  This protocol assumes that the
>   underlying protocols provide integrity and confidentiality
>   protection.
> 
>   [...]
> 
>   The 'service name' for this protocol is "ssh-userauth".
> 
>   When this protocol starts, it receives the session identifier from
>   the lower-level protocol (this is the exchange hash H from the first
>   key exchange).  The session identifier uniquely identifies this
>   session and is suitable for signing in order to prove ownership of a
>   private key.  This protocol also needs to know whether the lower-
>   level protocol provides confidentiality protection.
 

User authentication starts ith the client sending a request to authenticate with the `none` method. The server replies with a list of the allowed authentication methods (e.g. `publickey,password`). The user is free to choose any of the offered methods to authenticate. The server may require several authentication methods in succession ('partial success'), e.g.  first a valid publickey authentication, followed by a one time password authentication with a hardware token.
 
### Example Message Exchange for Password Authentication
 
This is a message exchange of the user `admin` authenticating with `password` authentication for the usage of an interactive terminal:
 
```
 
Client                                           Server
 
   |                                                |
   | >------------ SSH_MSG_USERAUTH_REQUEST ------> |
   |         user name:    "admin"                  |
   |         service name: "session"                |
   |         method-name:  "none"                   |
   |                                                |
   | <------------- SSH_MSG_USERAUTH_FAILURE -----< |
   |         name list:    "publickey,password"     |
   |         partial success: FALSE                 |
   |                                                |
   | >------------ SSH_MSG_USERAUTH_REQUEST ------> |
   |         user name:    "admin"                  |
   |         service name: "session"                |
   |         method-name:  "password"               |
   |         change-passwd: FALSE                   |
   |         password:     "s3cr3t"                 |
   |                                                |
   | <------------- SSH_MSG_USERAUTH_SUCCESS -----< |
   |                                                |
 
       ( the user is now authenticated)
```
 

## SSH-CONNECT
 
Cited from [RFC4254](http://datatracker.ietf.org/doc/rfc4254/?include_text-1):
 
>   The SSH Connection Protocol has been designed to run on top of the
>   SSH transport layer and user authentication protocols ([SSH-TRANS]
>   and [SSH-USERAUTH]).  It provides interactive login sessions, remote
>   execution of commands, forwarded TCP/IP connections, and forwarded
>   X11 connections.
> 
>   The 'service name' for this protocol is "ssh-connection".
 

### Global Requests
 
Global requests are independent of channels (see below), and allow for example to initialize port forwarding (see section 7 of the RFC).
 

### Channels
 
The connection protocol multiplexes several logical connections (_channel_) over the tranport connection. Both the client, and the server can open a channel via `SSH_MSG_CHANNEL_OPEN` requests.
 
A `SSH_MSG_CHANNEL_OPEN` request is subtyped by a string name (analogous to the names in user authentication). Both ends of a channel identify the channel by a numeric channel id. These ids can differ between sender and receiver. Channel ids are sometimes shown in ssh debug messages.
 
Once a channel has been opened, requests (`SSH_MSG_CHANNEL_REQUEST`) can be sent to the other side of the channel. This could, for example, be the request to open a pty for an interactive session.
 
Data transfer for a session is done using `SSH_MSG_CHANNEL_DATA` and `SSH_MSG_CHANNEL_EXTENDED_DATA` requests. The extended data type `SSH_EXTENDED_DATA_STDERR` has been defined for stderr data.
 

#### Interactive Session
 
The following mesage exchange shows how a session with a pty is opened:
 
```text
 
Client                                           Server
   |                                                |
   | >------------ SSH_MSG_CHANNEL_OPEN ----------> |
   |         channel name:   "session"              |
   |         sender channel: 42                     |
   |                                                |
   | <------------- SSH_MSG_CHANNEL_SUCCESS  -----< |
   |         recipient channel: 67                  |
   |                                                |
 
(the client channel #42 is now connected to the server channel #67)
 
   | >------------ SSH_MSG_CHANNEL_REQUEST  ------> |
   |         recipient channel:  67                 |
   |         request name:      "pty-req"           |
   |         want reply:         FALSE              |
   |         TERM:              "xterm-256"         |
   |         [further params]:  "..."               |
   |                                                |
 
     (the client channel #42 now resembles a pty)
 
```
 

#### X11 forwarding
 
See section 6.3.2 of the SSH-CONNECT [RFC](http://datatracker.ietf.org/doc/rfc4254/?include_text-1).
 
#### Agent Forwarding
 
The agent forwrding protocol used by OpenSSH is not defined by an RFC, but by a OpenSSH [directly](http://cvsweb.openbsd.org/cgi-bin/cvsweb/src/usr.bin/ssh/PROTOCOL.agent?rev=HEAD).
 
#### Port forwarding
 
Port forwarding (described in section 7 of the RFC) allows connections to a local or remote port to be tunnled through a channel. Each forwarding rule is initialized via a `SSH_MSG_GLOBAL_REQUEST` with the request string "tcpip-forward". SSH will create a new channel for each tcp connection made. E.g. when a local port is forwarded to a remote system, each tcp connection to this port opens a separate channel.
 
#### sftp
 
[sftp](http://en.wikipedia.org/wiki/SSH_File_Transfer_Protocol) is implemented as SSH _subsystem_ that can be startet by sending a `SSH_MSG_CHANNEL_REQUEST` with the request name "subsystem". The Filezilla project also has a good collection of [references](https://wiki.filezilla-project.org/SFTP_specifications).
 

#### scp
 
There is no RFC that defines scp.
 

# Ressources
 
* http://www.openssh.com/manual.html
* [RFC4251](http://datatracker.ietf.org/doc/rfc4251/?include_text-1) SSH-ARCH
* [RFC4252](http://datatracker.ietf.org/doc/rfc4252/?include_text-1) USER-AUTH
* [RFC4253](http://datatracker.ietf.org/doc/rfc4253/?include_text-1) SSH-TRANS
* [RFC4254](http://datatracker.ietf.org/doc/rfc4254/?include_text-1) SSH-CONNECT
 
 

