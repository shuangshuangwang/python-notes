#!/usr/bin/env/python
# -*- coding: utf-8 -*-

def send_wechat_message_from_remote(content):
  import paramiko
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ## ssh -p20343 dp@172.19.111.11
  ssh.connect('172.19.111.11', 20343, 'dp')
  ## cd ~/script/hadoop/
  ssh.exec_command('python ~/script/hadoop/wechat-hadoop.py --user=dp --message="' + content + '"')
  ssh.close()

import sys

if len(sys.argv) > 1:
  if sys.argv[1].strip():
    send_wechat_message_from_remote(sys.argv[1])