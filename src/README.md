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

I'm still working on the Dockerfile
`docker run -expose 5000 -p localhost:5000:5000 -t cloud-testing`
`docker kill $(docker ps -q)`
