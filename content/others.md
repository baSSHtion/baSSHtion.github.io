Title: Others
Date: 2014-08-23 22:20
Modified: 2014-08-24 23:15
Category: Misc
Tags: others
Slug: others
Authors: Jens Neuhalfen
Summary: Here are other possibilities
SortOrder: 70

## Attacks against SSH
### Man in the middle
> This program demonstrates man-in-the-middle attack with key manipulation for ssh that intercepts the plaintext communication, and the password used for authentication.
>
> If this PoC is run, it listens to a port on the local machine, and logically forwards the connection to a SSH server running on the network. It does so my terminating the SSH connection from the client, and establishing its own connection to the 'real' server. This allows the PoC to read the communication in plain.

[more](https://github.com/baSSHtion/ssh-man-in-the-middle-attack)

### Factoring keys with low entropy
> We have been able to remotely compromise about 0.4% of all the public keys used for SSL web site security. The keys we were able to compromise were generated incorrectly–using predictable “random” numbers that were sometimes repeated. There were two kinds of problems: keys that were generated with predictable randomness, and a subset of these, where the lack of randomness allows a remote attacker to efficiently factor the public key and obtain the private key. With the private key, an attacker can impersonate a web site or possibly decrypt encrypted traffic to that web site. We’ve developed a tool that can factor these keys and give us the private keys to all the hosts vulnerable to this attack on the Internet in only a few hours. 

[more](https://freedom-to-tinker.com/blog/nadiah/new-research-theres-no-need-panic-over-factorable-keys-just-mind-your-ps-and-qs/)

## Large(r) Installations
- [mussh](http://TODO) provides the means to run a command in parallel on multiple machines.
- [Chef](https://www.getchef.com/chef/), [Puppet](http://puppetlabs.com/), [salt](http://www.saltstack.com/), [ansible](http://www.ansible.com/home) and others are usefull to configure large infrastructure setups.

## Products
- [OpenSSH](http://www.openssh.com/)
- There is a commercial solution called [BalaBit Shell Control Box](https://www.balabit.com) that implements a pretty exthausive solution.
