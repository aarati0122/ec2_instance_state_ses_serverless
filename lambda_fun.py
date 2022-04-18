import boto3
import json
import logging
import datetime 
import os
from botocore.exceptions import ClientError
from datetime import timedelta
import smtplib
import csv

region = 'ap-south-1'
ec2 = boto3.resource('ec2',region)
client = boto3.client('ec2',region)


def lambda_handler(event, context):
    global stop
    global start
    stop = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    start = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance1 in stop:
        print('Ec2 Instances which are stopped: ', 'Instance ID: ', instance1.id, 'Instance state: ', instance1.state, 'Instance type: ',instance1.instance_type,'Instance Name',instance1.tags)
        
        print(instance1.state['Name'])
        state_ec2 = instance1.state['Name']
        if state_ec2 == "stopped":
            print("The EC2 instance is stopped and the ID is:",instance1.id)
            id = [instance1.id]
            # client.start_instances(InstanceIds=id)
            # URL = "https://instancestatepage.s3.ap-south-1.amazonaws.com/stop_start_instance.html?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECgaCmFwLXNvdXRoLTEiSDBGAiEA6ir3uKNDFh5HI84ZwtdZobzbeSDLPsOLXfiIuVPbX9oCIQCDYUDWlNI2VwcTa0KfWXW1lsV37Dt9VfAVFKANRiLvdSrtAgjR%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDQ5OTA4MTUzMjIzNyIM2pzb%2BO0qvBMSuqE9KsECFNC%2FWg5lLty5o7pvoEi%2FcdQezuThmu%2FX0OVHxvOzfuQ6NIcl7%2BrkAIwXye2jHLru5zUrbpcHiB%2FkdZCRMDMu9ifG2Zq0NOI1GWBSn6jmMndxeDvcBdRO5Iu3twIFL58ZXwJ8h6NGNMkEswQONnyaCHOU3fJePeX%2FI4dCEJv9fiGi0zKhVZis079xIWfJ3koNQaGWGL4sjvr9a96JZkRy56Lxz5KTLl3tV59K0f05dBt0V9jAeubl0s8KCrtqF565pERvxyQaXeqDuUTaMFcEZuGZOn6M4ZjalEEeMhfkD58IlzfJP3qkRmnPbBbJ5pIqQ0KAlZEDkEhJqEimRovzIBGK62WVoeF%2BbIUEmXG4z%2Bj3yq14WIRublT32Kich7GQSRYKJkrKwx2%2Bi2rZucF%2FGKllme3SK8b%2BgoiBEMKhRalMMLH785IGOrICbYwpcByY1IgUfA%2FjniWH3JmqdHdGVmeJr0SSDV4oVZ0SxULRjZKS7jTJFDqLrj%2FyUqRB4zX5Z6nWxBGolkBF5oBh21%2Ff4Ia7bg0CZy9j3tKXV5f7g5mY93vpD%2B4XMEewhZ4qMzlViL%2BFMrrjmDxi%2B%2FoKE9OH1ZdQeueBbUJyCiBab7YlntRN%2FVWdv5CCeBoZBjRt2FhlfK6X4RG3GWwSnw4Eq7PnNs0FCbub197%2FB21bAjYhi1AsgbjnhVGg4pe5rbU3rz%2FdnR3VKmdbwK%2F034znDGr8V1%2Fy2XC8jp%2BW58tmMNIEKyBcBbmCO7re1oXetIx1c6B%2BKxUixBmUPl%2Bkhy6rWca7dKPA%2FPVpvSLA%2F%2FsmS8GthEvgxN6IwXxVmO%2BdXQ61opoCmqY0TFu6wpuzwYU0&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220418T102843Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAXIM4T2NGQXJKDDWB%2F20220418%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=6cb8de51c9cb38a453c5287f7236cb471969fa8684879b8350472cf8c697c318"
            URL ="https://instancestatepage.s3.ap-south-1.amazonaws.com/stop_start_instance.html?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECgaCmFwLXNvdXRoLTEiSDBGAiEA6ir3uKNDFh5HI84ZwtdZobzbeSDLPsOLXfiIuVPbX9oCIQCDYUDWlNI2VwcTa0KfWXW1lsV37Dt9VfAVFKANRiLvdSrtAgjR%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDQ5OTA4MTUzMjIzNyIM2pzb%2BO0qvBMSuqE9KsECFNC%2FWg5lLty5o7pvoEi%2FcdQezuThmu%2FX0OVHxvOzfuQ6NIcl7%2BrkAIwXye2jHLru5zUrbpcHiB%2FkdZCRMDMu9ifG2Zq0NOI1GWBSn6jmMndxeDvcBdRO5Iu3twIFL58ZXwJ8h6NGNMkEswQONnyaCHOU3fJePeX%2FI4dCEJv9fiGi0zKhVZis079xIWfJ3koNQaGWGL4sjvr9a96JZkRy56Lxz5KTLl3tV59K0f05dBt0V9jAeubl0s8KCrtqF565pERvxyQaXeqDuUTaMFcEZuGZOn6M4ZjalEEeMhfkD58IlzfJP3qkRmnPbBbJ5pIqQ0KAlZEDkEhJqEimRovzIBGK62WVoeF%2BbIUEmXG4z%2Bj3yq14WIRublT32Kich7GQSRYKJkrKwx2%2Bi2rZucF%2FGKllme3SK8b%2BgoiBEMKhRalMMLH785IGOrICbYwpcByY1IgUfA%2FjniWH3JmqdHdGVmeJr0SSDV4oVZ0SxULRjZKS7jTJFDqLrj%2FyUqRB4zX5Z6nWxBGolkBF5oBh21%2Ff4Ia7bg0CZy9j3tKXV5f7g5mY93vpD%2B4XMEewhZ4qMzlViL%2BFMrrjmDxi%2B%2FoKE9OH1ZdQeueBbUJyCiBab7YlntRN%2FVWdv5CCeBoZBjRt2FhlfK6X4RG3GWwSnw4Eq7PnNs0FCbub197%2FB21bAjYhi1AsgbjnhVGg4pe5rbU3rz%2FdnR3VKmdbwK%2F034znDGr8V1%2Fy2XC8jp%2BW58tmMNIEKyBcBbmCO7re1oXetIx1c6B%2BKxUixBmUPl%2Bkhy6rWca7dKPA%2FPVpvSLA%2F%2FsmS8GthEvgxN6IwXxVmO%2BdXQ61opoCmqY0TFu6wpuzwYU0&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220418T111311Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAXIM4T2NGQXJKDDWB%2F20220418%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=8b9eee1e97321d1f08e12132c9403028b2189fe2d9ad3ec10982de8abec417f1"
            current_state = "The status of EC2 insrance is '{}' and its information Instance ID: '{}' , Instance type: '{}' and use following UI to change the state of instance {}  ".format(state_ec2, instance1.id,instance1.instance_type,URL)
            send_plain_email(current_state)
            
        #print('Ec2 Instances which are stopped: ', 'Instance ID: ', instance1.id, 'Instance state: ', instance1.state)
    for instance2 in start:
        #print('Ec2 Instances which are running: ', 'Instance ID: ', instance2.id, 'Instance state: ', instance2.state, 'Instance type: ',instance2.instance_type)
        print(instance2.state['Name'])
        state_ec2 = instance2.state['Name']
        if state_ec2 == "running":
            print("The EC2 instance is running and the ID is:",instance2.id)
            id = [instance2.id]
            # client.stop_instances(InstanceIds=id)
            # URL = "https://instancestatepage.s3.ap-south-1.amazonaws.com/stop_start_instance.html?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECgaCmFwLXNvdXRoLTEiSDBGAiEA6ir3uKNDFh5HI84ZwtdZobzbeSDLPsOLXfiIuVPbX9oCIQCDYUDWlNI2VwcTa0KfWXW1lsV37Dt9VfAVFKANRiLvdSrtAgjR%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDQ5OTA4MTUzMjIzNyIM2pzb%2BO0qvBMSuqE9KsECFNC%2FWg5lLty5o7pvoEi%2FcdQezuThmu%2FX0OVHxvOzfuQ6NIcl7%2BrkAIwXye2jHLru5zUrbpcHiB%2FkdZCRMDMu9ifG2Zq0NOI1GWBSn6jmMndxeDvcBdRO5Iu3twIFL58ZXwJ8h6NGNMkEswQONnyaCHOU3fJePeX%2FI4dCEJv9fiGi0zKhVZis079xIWfJ3koNQaGWGL4sjvr9a96JZkRy56Lxz5KTLl3tV59K0f05dBt0V9jAeubl0s8KCrtqF565pERvxyQaXeqDuUTaMFcEZuGZOn6M4ZjalEEeMhfkD58IlzfJP3qkRmnPbBbJ5pIqQ0KAlZEDkEhJqEimRovzIBGK62WVoeF%2BbIUEmXG4z%2Bj3yq14WIRublT32Kich7GQSRYKJkrKwx2%2Bi2rZucF%2FGKllme3SK8b%2BgoiBEMKhRalMMLH785IGOrICbYwpcByY1IgUfA%2FjniWH3JmqdHdGVmeJr0SSDV4oVZ0SxULRjZKS7jTJFDqLrj%2FyUqRB4zX5Z6nWxBGolkBF5oBh21%2Ff4Ia7bg0CZy9j3tKXV5f7g5mY93vpD%2B4XMEewhZ4qMzlViL%2BFMrrjmDxi%2B%2FoKE9OH1ZdQeueBbUJyCiBab7YlntRN%2FVWdv5CCeBoZBjRt2FhlfK6X4RG3GWwSnw4Eq7PnNs0FCbub197%2FB21bAjYhi1AsgbjnhVGg4pe5rbU3rz%2FdnR3VKmdbwK%2F034znDGr8V1%2Fy2XC8jp%2BW58tmMNIEKyBcBbmCO7re1oXetIx1c6B%2BKxUixBmUPl%2Bkhy6rWca7dKPA%2FPVpvSLA%2F%2FsmS8GthEvgxN6IwXxVmO%2BdXQ61opoCmqY0TFu6wpuzwYU0&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220418T102843Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAXIM4T2NGQXJKDDWB%2F20220418%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=6cb8de51c9cb38a453c5287f7236cb471969fa8684879b8350472cf8c697c318"
            URL = "https://instancestatepage.s3.ap-south-1.amazonaws.com/stop_start_instance.html?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECgaCmFwLXNvdXRoLTEiSDBGAiEA6ir3uKNDFh5HI84ZwtdZobzbeSDLPsOLXfiIuVPbX9oCIQCDYUDWlNI2VwcTa0KfWXW1lsV37Dt9VfAVFKANRiLvdSrtAgjR%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDQ5OTA4MTUzMjIzNyIM2pzb%2BO0qvBMSuqE9KsECFNC%2FWg5lLty5o7pvoEi%2FcdQezuThmu%2FX0OVHxvOzfuQ6NIcl7%2BrkAIwXye2jHLru5zUrbpcHiB%2FkdZCRMDMu9ifG2Zq0NOI1GWBSn6jmMndxeDvcBdRO5Iu3twIFL58ZXwJ8h6NGNMkEswQONnyaCHOU3fJePeX%2FI4dCEJv9fiGi0zKhVZis079xIWfJ3koNQaGWGL4sjvr9a96JZkRy56Lxz5KTLl3tV59K0f05dBt0V9jAeubl0s8KCrtqF565pERvxyQaXeqDuUTaMFcEZuGZOn6M4ZjalEEeMhfkD58IlzfJP3qkRmnPbBbJ5pIqQ0KAlZEDkEhJqEimRovzIBGK62WVoeF%2BbIUEmXG4z%2Bj3yq14WIRublT32Kich7GQSRYKJkrKwx2%2Bi2rZucF%2FGKllme3SK8b%2BgoiBEMKhRalMMLH785IGOrICbYwpcByY1IgUfA%2FjniWH3JmqdHdGVmeJr0SSDV4oVZ0SxULRjZKS7jTJFDqLrj%2FyUqRB4zX5Z6nWxBGolkBF5oBh21%2Ff4Ia7bg0CZy9j3tKXV5f7g5mY93vpD%2B4XMEewhZ4qMzlViL%2BFMrrjmDxi%2B%2FoKE9OH1ZdQeueBbUJyCiBab7YlntRN%2FVWdv5CCeBoZBjRt2FhlfK6X4RG3GWwSnw4Eq7PnNs0FCbub197%2FB21bAjYhi1AsgbjnhVGg4pe5rbU3rz%2FdnR3VKmdbwK%2F034znDGr8V1%2Fy2XC8jp%2BW58tmMNIEKyBcBbmCO7re1oXetIx1c6B%2BKxUixBmUPl%2Bkhy6rWca7dKPA%2FPVpvSLA%2F%2FsmS8GthEvgxN6IwXxVmO%2BdXQ61opoCmqY0TFu6wpuzwYU0&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220418T111311Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAXIM4T2NGQXJKDDWB%2F20220418%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=8b9eee1e97321d1f08e12132c9403028b2189fe2d9ad3ec10982de8abec417f1"
            current_state = "The status of EC2 insrance is '{}' and its information \n Instance ID: '{}' ,\n Instance type: '{}' , \n Instance Name: {} \n Use following UI to change the state of instance \n {} ".format(state_ec2, instance2.id,instance2.instance_type,instance1.tags,URL)
            send_plain_email(current_state)
        print('Ec2 Instances which are running: ', 'Instance ID: ', instance2.id, 'Instance state: ', instance2.state)
        
def send_plain_email(data):
    ses_client = boto3.client("ses", region_name="ap-south-1")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
            Destination={
                "ToAddresses": [
                    "abc@gmail.com",
                ],
            },
            Message={
                "Body": {
                    "Text": {
                        "Charset": CHARSET,
                        "Data": data,
                    }
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": "EC2 Instances Status Related",
                },
            },
            Source="xyz@gmail.com",
    )
    
