import requests
import json

base_job_url = "http://172.19.100.62:404%s/api/v1/applications"
base_job_batches_url = "http://172.19.100.62:404%s/api/v1/applications/%s/streaming/batches?status=%s"

f=open('/home/anaconda3/streaming/streaming_jobs_queued_checking.status.txt','r+')
flist=f.readlines()


def send_alter_message_to_wechat(content):
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('172.19.111.11', 20343, 'dp')
    ssh.exec_command('python ~/script/hadoop/wechat-hadoop-sgc.py --user=dp --message="' + content+'"')
    ssh.close()

def kill_queued_job(appid):
    app_kill_url = "http://172.19.100.62:8090/app/kill/"
    resp = requests.post(app_kill_url, {'id': appid, 'terminate': 'true'})

## 目前共6个作业（4040~4046），completed正常返回1000条数据，flist文件每分钟更新一次，
## 相当于从某个时间开始持续阻塞，即completed状态的最后一个批次数据持续一分钟以上没有执行完成，且排队数据超过20即kill任务并报警

if __name__ == '__main__':
    for i in range(10):#目前检查4040-4049段程序执行情况
        url_job_id = base_job_url % str(i)
        try:
            print('checking 404'+str(i))
            job_response = requests.get(url_job_id)
            if job_response.status_code == 200:
                job_json = json.loads(job_response.content)
                if len(job_json) > 0:
                    job_id = job_json[0]['id']
                    base_job_batches_url_completed = base_job_batches_url % (str(i),job_id,"completed")
                    job_baches_response = requests.get(base_job_batches_url_completed)
                    if job_baches_response.status_code == 200:
                        job_batches_json_completed = json.loads(job_baches_response.content)
                        if job_batches_json_completed[0]["batchTime"]+"\n"!=flist[i]:
                            flist[i]=job_batches_json_completed[0]["batchTime"]+"\n"
                            continue
                        else:
                            base_job_batches_url_queued = base_job_batches_url % (str(i),job_id,"queued")
                            job_baches_response = requests.get(base_job_batches_url_queued)
                            job_batches_json_queued = json.loads(job_baches_response.content)
                            if job_baches_response.status_code == 200 and len(job_batches_json_queued) > 20 and len(job_batches_json_completed) > 500:
                                send_alter_message_to_wechat("killing streaming job: " + job_json[0]['name'] + ", batch queued size: " + str(len(job_batches_json_queued)))
                                kill_queued_job(job_id)
                                print('task queued, killing job: '+job_id)
        except Exception as e:
            if 'Connection refused' in str(e):
                print('has no application in port:404'+str(i))
            continue
    f=open('/home/anaconda3/streaming/streaming_jobs_queued_checking.status.txt','w+')
    f.writelines(flist)
    f.close()