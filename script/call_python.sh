#!/bin/sh

currdt=`date '+%Y-%m-%d %H:%M:%S'`
message="resubmit spark streaming job: ppc_models_pyspark_streaming at "$currdt"."
/home/anaconda3/anaconda3/bin/python $rootPath/sendmsg2wechat.py "$message"