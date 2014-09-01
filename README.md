Site
=====

The site is found at [basshtion.org](http://www.basshtion.org/) . Site generation is done by [pelican](http://docs.getpelican.com/en/3.4.0/index.html).

Preview
===========

```bash
./develop_server.sh start
firefox http://127.0.0.1:8000/
```


Pelican Help
==========

```text
$ make help

Makefile for a pelican Web site                                        
                                                                       
Usage:                                                                 
   make html                        (re)generate the web site          
   make clean                       remove the generated files         
   make regenerate                  regenerate files upon modification 
   make publish                     generate using production settings 
   make serve [PORT=8000]           serve site at http://localhost:8000
   make devserver [PORT=8000]       start/restart develop_server.sh    
   make stopserver                  stop local server                  
   make ssh_upload                  upload the web site via SSH        
   make rsync_upload                upload the web site via rsync+ssh  
   make dropbox_upload              upload the web site via Dropbox    
   make ftp_upload                  upload the web site via FTP        
   make s3_upload                   upload the web site via S3         
   make cf_upload                   upload the web site via Cloud Files
   make github                      upload the web site via gh-pages   
                                                                       
Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html
```

Build
==========

Build html & open in browser
------------------------------

```bash
make html 
make serve

```

Point browser to [http://localhost:8000](http://localhost:8000) .

Build everything, commit to `master` and push to github
----------------------------------------------------------

```
./build-master.sh
```



Install pelican
===============
```
virtualenv ../pelican.venv
. ../pelican.venv/bin/activate

pip install -r requirements.txt
```

FAQ
--------

*Q: Error `/usr/bin/python: No module named pelican` when generating site*
*A:* Either `pelican` is not installed, or the [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) is not sourced. Try `source /path/to/env/bin/activate .


