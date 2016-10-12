Install and development instruction

Make sure you have virtual environment installed
`pip install virtualenv`

Create a new venv in the folder
`virtualenv venv`

Active env
`source venv/bin/activate`

Install required packages
`pip install -r requirements.txt`

Install package from requirements.txt
`pip install package`

Save your installed package as dependency in requirements.txt
`pip freeze > requirements.txt`

Deactivate env
`deactivate`

Docker commands

build image from `src/` folder `-t` flag to name image
`docker build -t app .`

run image and `-p` port mapping `$hostport:$containerPort` `-d` detached from terminal
`docker run -d -p 5000:5000 -t app`

kill all running process
`docker kill $(docker ps -q)`

remove all images with force
`docker rmi --force $(docker images -a -q)`
