ID Document Liveness Detection SDK Demo Guide

############# 

1. OS requirements
	Operating System: Ubuntu 22.04 or later
	CPU: 8 cores
	RAM: 8 GB
	HDD: 8 GB

2. Run './install.sh' to install dependencies.

3. Copy 'license.txt' file to project root directory ('ID_Live').

4. Run './run.sh -g' for gradio demo(127.0.0.1:7860), './run.sh -f' for flask demo(127.0.0.1:9000).


#############   Use Docker Container

1. Build docker container named 'id-live'.
	sudo docker build -t id-live .
2. Run 'id-live' container with 'license.txt' file.
	sudo docker run -it -v /path/to/host/license.txt:/path/in/container/license.txt -p 9001:9000 -p 7861:7860 id-live:latest -g
	Examle:
	sudo docker run -it -v /root/license.txt:/app/license.txt -p 9001:9000 -p 7861:7860 id-live:latest -g
	
