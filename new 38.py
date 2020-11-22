
#Copy the already created scoring_file_v_1_0_0.py file from the automl run into the scope.py
script_file_name='inference/scope.py'
best_run.download_file('outputs/scoring_file_v_1_0_0.py', 'inference/scope.py')


#Set up the inference_config
#The environment is set from the best_run of the automl run
inference_config = InferenceConfig(entry_script=script_file_name, environment=best_run.get_environment())

#Local Deployment
from azureml.core.webservice import LocalWebservice
local_config = LocalWebservice.deploy_configuration(port=9000)
local_service = Model.deploy(ws, "test", [auto_ml], inference_config, local_config)
local_service.wait_for_deployment(show_output=True)

#Set up the deployment_config as webservice
aci_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1, enable_app_insights=True)

#Deploy the model
service = Model.deploy(
    workspace = ws,
    name = "mywebservice",
    models = [auto_ml],
    inference_config = inference_config,
    deployment_config = aci_config, overwrite=True)

#wait until deployment is complete
service.wait_for_deployment(show_output = True)


#Print the webservice logs
print(service.get_logs())


#Print the state
print(service.state)

#Print the scoring uri of the service
print(service.scoring_uri)


#Import the test-data csv file in order to test the webservice
import pandas as pd
test_df=pd.read_csv('./test-data.csv')
test_df

#Import Json requests and test the webservice
import json
data= ({'data':test_df[0:3].to_dict(orient='records')})
test_sample=json.dumps(data)
output= service.run(test_sample)
print(output)


#Delete the service
service.delete()