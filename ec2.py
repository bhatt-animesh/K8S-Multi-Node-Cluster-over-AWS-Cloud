#!/usr/bin/python3
import json  #ansible can understand easily
import time
try:
    import boto3  #used to connect aws
    import boto.ec2
except Exception as e:
    print("please check boto module is installed or not\n if not then use 'pip3 install boto3' ")
    print(e)
# we are getting IPs and appending in list
def get_hosts(ec2_ob, fv):
    f={"Name":"tag:Name", "Values": [fv]}
    v={'Name': 'instance-state-name', 'Values': ['running']}
    hosts=[]

    for each in ec2_ob.instances.filter(Filters=[f,v]):
        hosts.append(each.public_ip_address)
    return hosts



def main():
    ec2_ob=boto3.resource("ec2","ap-south-1")   #checking ec2 info in ap-south-1 region
    ec2_name = boto.ec2.connect_to_region('ap-south-1')
    name_tag = 0

    for instance in ec2_ob.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]):   #rename the name of master and worker
        if name_tag == 0:
            #print (instance.id , instance.state)
            reservations = ec2_name.get_all_instances(instance_ids=instance.id)
            instance = reservations[0].instances[0]
            instance.add_tag('Name', 'k8S-master')
            name_tag =+ 1
            print ("Master Node : " + instance.id) 
        else:
            #print (instance.id)
            reservations = ec2_name.get_all_instances(instance_ids=instance.id)
            instance = reservations[0].instances[0]
            instance.add_tag('Name', 'k8S-worker')

            print ("Worker Node : " + instance.id)


    k8s_master=get_hosts(ec2_ob, 'k8S-master')
    k8s_worker=get_hosts(ec2_ob,'k8S-worker')
    with open('/root/ip.txt', 'a') as f:
     f.write("[k8s-master]" + "\n" )   
     for master_ip in k8s_master:
       f.write("%s\n" % master_ip)
     f.write("[k8s-worker]" + "\n")
     for worker_ip in k8s_worker:
       f.write("%s\n" % worker_ip)


    print ("waiting for instance")
    time.sleep(60)
    all_IPs={'master': k8s_master,'worker': k8s_worker }  # converting list into json so that ansible can understand

    print(json.dumps(all_IPs))



if __name__=="__main__":
    main()
