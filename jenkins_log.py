import requests
import json
from argparse import ArgumentParser
from collections import OrderedDict

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Jenkins():
    
    def __init__(self, user, password, data):
        self.user = user
        self.password = password
        self.data = data
        
        
    def clear_console_file(self):
        logger.info("cleanup the console log file")
        try:
            f = open('console.log', 'r+')
            f.truncate()
        except Exception as e:
            print e
        
        
    def execute_build_nos(self, job_name):
        logger.info("Getting the jenkins job latest build nos")
        try:
            url = 'http://10.161.113.188:8080/job/%s/lastBuild/buildNumber' % job_name
            r = requests.get(url, auth=(self.user, self.password))
            return r.text
        except Exception as e:
            print e
        
        
    def write_console_output(self, text, job, build):
        logger.info("Writing the jenkins console output to log file.")
        try:
            with open("console.log", "a") as myfile:
                myfile.write(text.encode('utf-8'))
                myfile.write('\n===========================================================END OF LOG for %s:%s=================================================================\n' % (job, build))
        except Exception as e:
            print e
        
    
    def execute_console(self, job_name, build_nos):
        logger.info("Getting the jenkins console output")
        try:
            url = 'http://10.161.113.188:8080/job/%s/%s/consoleText' % (job_name, build_nos)
            r = requests.get(url, auth=(self.user, self.password))
            self.write_console_output(r.text, job_name, build_nos)
        except Exception as e:
            print e
            

    def job_execute(self):
        logger.info("Executing the jenkins jobs")
        try:
            for k, v in  OrderedDict(sorted(self.data.iteritems())).iteritems():
                last_build_nos = self.execute_build_nos(job_name=v)
                self.execute_console(job_name=v, build_nos=last_build_nos)
        except Exception as e:
            print e
            
        
if __name__ == '__main__':
    try:
        logger.info("Started python script for jenkins console")
        parser = ArgumentParser()
        parser.add_argument("-f", "--file", dest="file", help="user file input", metavar="FILE")
        parser.add_argument("-e", "--environment", type=str, help="environment to get console log")
        parser.add_argument("-u", "--user", type=str, help="username for jenkins")
        parser.add_argument("-p", "--password", type=str, help="password for jenkins")
        args = parser.parse_args()
        
        with open(args.file) as f:
            data = json.load(f)
        
        if not args.file or not args.user or not args.password or not args.environment:
            parser.error("Please provide arguments")
        
        ins = Jenkins(args.user, args.password, data[args.environment])
        
        ins.clear_console_file()
        ins.job_execute()
        logger.info("Ended python script for jenkins console")

    except Exception as e:
        print e
