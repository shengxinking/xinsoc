#!/usr/bin/env python
from openvas_lib import VulnscanManager,VulnscanException
from threading import Semaphore
from functools import partial
from xml.etree import ElementTree
import base64
import datetime
import os
import sys,re
import subprocess
import time
import random
import MySQLdb
import json
import urllib2
import logging
import logging.handlers
import time
import sqlite3


HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWORD = ''
DBNAME = 'scanport'

def my_print_status(i):
    print str(i),
    sys.stdout.flush()
def write_report(manager,report_id,ip):
    result_dir=os.path.dirname(os.path.abspath(__file__))+"/results"
    try:
        report=manager.get_report_html(report_id)
	print "html %s" %(report)
    except Exception,e:
        print e
        return
    else:
        fout=open(result_dir+"/html/"+ip+".html","wb")
        fout.write(base64.b64decode(report.find("report").text))
        fout.close()
    try:
        report=manager.get_report_xml(report_id)
    except Exception,e:
        print e
        return
    else:
        fout=open(result_dir+"/xml/"+ip+".xml","wb")
        fout.write(ElementTree.tostring(report,encoding='utf-8',method='xml'))
        fout.close()
def run(manager,ip):
    Sem =Semaphore(0)
    scan_id,target_id=manager.launch_scan(
            target=ip,
            profile="Full and fast",
            callback_end=partial(lambda x:x.release(),Sem),
            callback_progress=my_print_status
            )
    Sem.acquire()
    print "scan id %s" %(scan_id)
    report_id=manager.get_report_id(scan_id)
    conn_sqlite = conn_sqlite3(PATH)
    dump_vul_data(report_id,conn_sqlite, conn_mysql)
    print "scan finished ok: repot id (%s)" %(report_id)
 #   write_report(manager,report_id,ip)
 #   manager.delete_scan(scan_id)
 #   manager.delete_target(target_id)


def get_all_ip_port(conn, manager):
    cur = conn.cursor()
    sql = 'select ip,scan_port,relate_man,mail,phone,region from config' 
    cur.execute(sql)
    resList = cur.fetchall()
    for i in resList:   
        print i[0], i[1]
        run(manager,i[0])
    conn.close()
    return 0

PATH = '/var/lib/openvas/mgr/tasks.db'
def conn_sqlite3(path):
	try:  
		sqlite_conn=sqlite3.connect(path)  
	except sqlite3.Error,e:  
		print "connect sqlite failed", "\n", e.args[0]  
	return sqlite_conn

def dump_in_mysql_database( conn,v_type,v_sev,v_desc,v_host,task):
    cur = conn.cursor()
    desc = MySQLdb.escape_string(v_desc)
    sql = "insert into vulresult (type, severity,description, host,task) values \
            ('%s','%s','%s','%s','%s')"\
                %(v_type,v_sev,desc,v_host,task)
    print sql
    cur.execute(sql)


def dump_vul_data(report_id, conn_sqlite, conn_mysql):
	cur = conn_sqlite.cursor()
	sql = 'SELECT task FROM reports where uuid = \'%s\';' %(report_id)
	print sql
	cur.execute(sql)  
	for row in cur:  
		print "reuslt:%s" %(row[0])
		task =row[0]

	sql = 'SELECT type, severity,description, host FROM results where task = \'%s\';' %(task)
	print sql
	cur.execute(sql)  
	for row in cur:  
		#	print "reuslt:%s:%s:%s:%s" %(row[0],row[1],row[2],row[3])
			dump_in_mysql_database(conn_mysql, row[0], row[1],row[2],row[3],task)
			conn_mysql.commit()

if __name__ == '__main__':
	
	try:
		conn_mysql = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DBNAME,port=PORT)
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1]) 
	try:
        #manager= VulnscanManager(openvas_ip,admin_name,admin_password)
		manager= VulnscanManager("127.0.0.1","admin","123456",9390,10)
		get_all_ip_port(conn_mysql, manager)
        #run(manager,"127.0.0.1")
	except Exception,e:
		print e
