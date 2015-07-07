#!/usr/bin/env python

import MySQLdb
import json
import urllib2
import logging 
import logging.handlers
import time

HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWORD = ''
DBNAME = 'scanport'

import g_var

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException


def mycallback(nmaptask):
    nmaptask = g_var.nmap_proc.current_task
    if nmaptask:
        print("Task {0} ({1}): ETC: {2} DONE: {3}%".format(nmaptask.name,
                                                           nmaptask.status,
                                                           nmaptask.etc,
                                                           nmaptask.progress))




def nmap_ip(ip, port):
	opt = "-sV -p " + port
	print opt
	g_var.nmap_proc = NmapProcess(targets=ip,
                        options=opt,
                        event_callback=mycallback)
	g_var.nmap_proc.run()
	print(g_var.nmap_proc.stdout)
	
	try:
		parsed = NmapParser.parse(g_var.nmap_proc.stdout)
	except NmapParserException as e:
		print("Exception raised while parsing scan: {0}".format(e.msg))
	
	return parsed


def dump_in_database( conn,serv,ip,relate_man, mail,phone,region):
	cur = conn.cursor()
	sql = "insert into result 	(ip,relate_man,port,service,mail,phone,region,state,banner) values \
			('%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
				%(ip,relate_man, str(serv.port),serv.service,mail,phone,region,serv.state,serv.banner) 
	print sql
	cur.execute(sql)

# print scan results from a nmap report 
def print_scan(conn,nmap_report,relate_man,mail,phone,region): 
	print("Starting Nmap {0} ( http://nmap.org ) at {1}".format( 
		nmap_report.version, 
		nmap_report.started)) 
 
	for host in nmap_report.hosts: 
		if len(host.hostnames): 
			tmp_host = host.hostnames.pop() 
		else: 
			tmp_host = host.address 
 
		print("Nmap scan report for {0} ({1})".format( 
			tmp_host, 
			host.address)) 
		print("Host is {0}.".format(host.status)) 
		print("  PORT     STATE         SERVICE") 
 
		for serv in host.services: 
			pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format( 
				str(serv.port), 
				serv.protocol, 
				serv.state, 
				serv.service) 
			if len(serv.banner): 
				pserv += " ({0})".format(serv.banner) 
				print(pserv) 
				dump_in_database(conn,serv,host.address,relate_man,mail,phone,region)
		print(nmap_report.summary)



def get_all_ip_port(conn):
	cur = conn.cursor()
	sql = 'select ip,scan_port,relate_man,mail,phone,region from config' 
	cur.execute(sql)
	resList = cur.fetchall()
	for i in resList:	
		print i[0], i[1]
		parsed = nmap_ip(i[0], i[1])
		print_scan(conn, parsed,i[2],i[3],i[4],[5]) 
	conn.close()
	return 0





if __name__ == '__main__':
	print("-------BEGIN CHECK---------------------")
	try:
		conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DBNAME,port=PORT)
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])

	get_all_ip_port(conn)
