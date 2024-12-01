import os
path = os.path.abspath(__file__)
path = os.path.abspath(os.path.join(path, os.pardir))

url_frontend = "http://localhost:3000/"
url_db = "mongodb+srv://dfki:qwe@adrz-lwttu.mongodb.net/test?retryWrites=true&w=majority"
url_clevr = "https://guideexport-sandbox.mxapps.io/rest/download/v1/"
db = 'tripleadapt'
task_collection_name = "tasks_cylinder_test"
model_path = path+'/Resources/data/Zylindermontage_V2_1.bpmn'
inside_docker = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
stay_online_db = True
method = "NN"
CLEVR_URL = "http://localhost:8080"
