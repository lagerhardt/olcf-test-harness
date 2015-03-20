#! /usr/bin/env python

import string
import os
import string
import datetime
import re
import uuid
from libraries import computers_1

#
# Author: Arnold Tharrington
# Email: arnoldt@ornl.gov
# National Center of Computational Science, Scientifc Computing Group.
#

#-----------------------------#
# Class: parse_status_file    #
#-----------------------------#
class rgt_status_file:
    ###################
    # Class variables #
    ###################
    line_format = "%-30s %-21s %-20s %-15s %-15s %-15s\n"

    #Header lines for status.
    header1 = line_format % (" "," "," "," "," "," ")
    header2 = string.replace(header1," ","#")
    header3 = line_format % ("#Start Time", "Unique ID","Batch ID", "Build Status","Submit Status", "Correct Results")

    header = header2
    header = header + header1
    header = header + header3
    header = header + header1
    header = header + header2

    #Name of the input file.
    filename = "rgt_status.txt"
    
    # The execution start and stop timestamp log file.
    start_execution_timestamp_filename = "start_binary_execution_timestamp.txt"
    final_execution_timestamp_filename = "final_binary_execution_timestamp.txt"

    build_start_execution_timestamp_filename = "start_build_execution_timestamp.txt"
    build_final_execution_timestamp_filename = "final_build_execution_timestamp.txt"

    submit_start_execution_timestamp_filename = "start_submit_execution_timestamp.txt"
    submit_final_execution_timestamp_filename = "final_submit_execution_timestamp.txt"

    #These are the entries in the input file.
    comment_line_entry = "#"


    FAILURE_CODES = { "Pass_Fail": 0,
                      "Hardware_Faiure": 1,
                      "Performance_Failure": 2,
                      "Incorrect_Result": 3
                     }
    ###################
    # Special methods #
    ###################
    def __init__(self,unique_id,mode):
        self.__job_id = ""
        self.__path_to_file = ""
        self.__unique_id = unique_id

        # Make the status file.
        self.__makeStatusFiles()

        # Add job to status file.
        if mode == "New":
            self.__add_job()

        elif mode == "Old":
            pass

    ###################
    # Public methods  #
    ###################
    def add_result(self,exit_value,mode):
        file_obj = open(self.__path_to_file,"r")
        records1 = file_obj.readlines()
        file_obj.close()
        event_time = datetime.datetime.now().isoformat()

        ip = -1
        for line in records1:
            ip = ip + 1

            #Get the uid for this run instance
            line1 = string.rstrip(line) 
            words1 = string.split(line1)

            if len(words1) >= 6:
                stime1 = words1[0]
                uid1 = words1[1]

                if uid1 == self.__unique_id:
                    if mode == "Add_Job_ID":
                        words1[2] = exit_value

                    if mode == "Add_Build_Result":
                        words1[3] = exit_value
                        self.__write_system_log('build_result', str(exit_value), event_time)

                    if mode == "Add_Submit_Result":
                        words1[4] = exit_value
                        self.__write_system_log('submit_result', str(exit_value), event_time)

                    if mode == "Add_Run_Result":
                        words1[5] = exit_value
                        self.__write_system_log('run_result', str(exit_value), event_time)

                    if mode == "Add_Run_Aborning":
                        words1[5] = "17"

                        cwd = os.getcwd()
                        (dir_head1, dir_tail1) = os.path.split(cwd)
                        path2 = os.path.join(dir_head1,"Status",uid1,"job_status.txt")
                        file_obj2 = open(path2,"w")
                        file_obj2.write("17")
                        file_obj2.close()
                        self.__write_system_log('run_aborning', str(exit_value), event_time)
   
                    records1[ip] = rgt_status_file.line_format  % (words1[0], words1[1], words1[2], words1[3], words1[4], words1[5])

        file_obj = open(self.__path_to_file,"w")
        file_obj.writelines(records1)
        file_obj.close()

    def logStartExecutionTime(self):
        currenttime = datetime.datetime.now()

        #
        # Get the current working directory.
        #
        cwd = os.getcwd()

        #
        # Get the head dir in cwd.
        #
        (dir_head1, dir_tail1) = os.path.split(cwd)

        path_to_file = os.path.join(dir_head1,
                                    "Status",
                                     str(self.__unique_id),
                                     rgt_status_file.start_execution_timestamp_filename )
        file_obj = open(path_to_file,"a")
        file_obj.write(currenttime.isoformat())
        file_obj.close()
        event_time = currenttime.isoformat()
        self.__write_system_log('binary_execute', 'start', event_time)

    def logFinalExecutionTime(self):
        currenttime = datetime.datetime.now()

        #
        # Get the current working directory.
        #
        cwd = os.getcwd()

        #
        # Get the head dir in cwd.
        #
        (dir_head1, dir_tail1) = os.path.split(cwd)

        path_to_file = os.path.join(dir_head1,
                                    "Status",
                                     str(self.__unique_id),
                                     rgt_status_file.final_execution_timestamp_filename )

        file_obj = open(path_to_file,"a")
        file_obj.write(currenttime.isoformat())
        file_obj.close()
        event_time = currenttime.isoformat()
        self.__write_system_log('binary_execute', 'end', event_time)


    def logBuildStartTime(self):
        currenttime = datetime.datetime.now()

        #
        # Get the current working directory.
        #
        cwd = os.getcwd()

        #
        # Get the head dir in cwd.
        #
        (dir_head1, dir_tail1) = os.path.split(cwd)

        path_to_file = os.path.join(dir_head1,
                                    "Status",
                                    str(self.__unique_id),
                                    rgt_status_file.build_start_execution_timestamp_filename )
        file_obj = open(path_to_file,"a")
        file_obj.write(currenttime.isoformat())
        file_obj.close()
        event_time = currenttime.isoformat()
        self.__write_system_log('build', 'start', event_time)

    def logBuildEndTime(self):
        currenttime = datetime.datetime.now()

        #
        # Get the current working directory.
        #
        cwd = os.getcwd()

        #
        # Get the head dir in cwd.
        #
        (dir_head1, dir_tail1) = os.path.split(cwd)

        path_to_file = os.path.join(dir_head1,
                                    "Status",
                                    str(self.__unique_id),
                                    rgt_status_file.build_final_execution_timestamp_filename )
        file_obj = open(path_to_file,"a")
        file_obj.write(currenttime.isoformat())
        file_obj.close()
        event_time = currenttime.isoformat()
        self.__write_system_log('build', 'end', event_time)

    def logSubmitStartTime(self):
        currenttime = datetime.datetime.now()

        #
        # Get the current working directory.
        #
        cwd = os.getcwd()

        #
        # Get the head dir in cwd.
        #
        (dir_head1, dir_tail1) = os.path.split(cwd)

        path_to_file = os.path.join(dir_head1,
                                    "Status",
                                    str(self.__unique_id),
                                    rgt_status_file.submit_start_execution_timestamp_filename )
        file_obj = open(path_to_file,"a")
        file_obj.write(currenttime.isoformat())
        file_obj.close()
        event_time = currenttime.isoformat()
        self.__write_system_log('submit', 'start', event_time)

    def logSubmitEndTime(self):
        currenttime = datetime.datetime.now()

        #
        # Get the current working directory.
        #
        cwd = os.getcwd()

        #
        # Get the head dir in cwd.
        #
        (dir_head1, dir_tail1) = os.path.split(cwd)

        path_to_file = os.path.join(dir_head1,
                                    "Status",
                                    str(self.__unique_id),
                                    rgt_status_file.submit_final_execution_timestamp_filename )
        file_obj = open(path_to_file,"a")
        file_obj.write(currenttime.isoformat())
        file_obj.close()
        event_time = currenttime.isoformat()
        self.__write_system_log('submit', 'end', event_time)

    ###################
    # Private methods #
    ###################
    def __makeStatusFiles(self):  
        #
        # Get the current working directory.
        #
        cwd = os.getcwd()

        #
        # Get the head dir in cwd.
        #
        (dir_head1, dir_tail1) = os.path.split(cwd)

        #
        # Now join dirhead1 to form path to rgt status file.
        #
        self.__path_to_file = os.path.join(dir_head1,"Status",rgt_status_file.filename)
        if (not os.path.lexists(self.__path_to_file)):
            file_obj = open(self.__path_to_file,"w")
            file_obj.write(rgt_status_file.header)
            file_obj.close()
             
 

    def __add_job(self):
        currenttime = datetime.datetime.now()
        file_obj = open(self.__path_to_file,"a")
        fmt1 =  rgt_status_file.line_format % (currenttime.isoformat(), self.__unique_id, "***" , "***" , "***" , "***" )
        file_obj.write(fmt1)
        file_obj.close()
  
    @staticmethod
    def write_system_log(test_id_string, event_name, event_value, event_time):
        """
        """
        #---Get tag.

        rgt_system_log_tag = os.environ['RGT_SYSTEM_LOG_TAG'] \
            if 'RGT_SYSTEM_LOG_TAG' in os.environ else ''

        if rgt_system_log_tag == '':
            return

        #---Determine whether to use Unix logger command.

        is_using_unix_logger = False

        rgt_system_log_dir = os.environ['RGT_SYSTEM_LOG_DIR'] \
            if 'RGT_SYSTEM_LOG_DIR' in os.environ else ''

        if rgt_system_log_dir == '':
            is_using_unix_logger = True
        elif not os.path.exists(rgt_system_log_dir):
            is_using_unix_logger = True

        #---Construct fields for log entry.

        user = os.environ['USER']

        wd = os.getcwd()
        (dir_head1, dir_scripts) = os.path.split(wd)
        (dir_head2, test) = os.path.split(dir_head1)
        (dir_head3, application) = os.path.split(dir_head2)

        dir_status = os.path.join(dir_head1, 'Status')

        dir_status_this_test = os.path.join(dir_status, test_id_string)

        file_job_id = os.path.join(dir_status_this_test, 'job_id.txt')
        if os.path.exists(file_job_id):
            file_ = open(file_job_id, 'r')
            job_id = file_.read()
            file_.close()
            job_id = re.sub(' ', '', job_id.split('\n')[0])
        else:
            job_id = ''

        file_job_status = os.path.join(dir_status_this_test, 'job_status.txt')
        if os.path.exists(file_job_status):
            file_ = open(file_job_status, 'r')
            job_status = file_.read()
            file_.close()
            job_status = re.sub(' ', '', job_status.split('\n')[0])
        else:
            job_status = ''

        dir_run_archive = os.path.join(dir_head1, 'Run_Archive')

        run_archive = os.path.join(dir_run_archive, test_id_string)

        rgt_path_to_sspace = os.environ['RGT_PATH_TO_SSPACE']

        build_directory = os.path.join(rgt_path_to_sspace, application, test,
                                       test_id_string, 'build_directory')

        workdir = os.path.join(rgt_path_to_sspace, application, test,
                               test_id_string, 'workdir')

        rgt_pbs_job_accnt_id = os.environ['RGT_PBS_JOB_ACCNT_ID']

        path_to_rgt_package = os.environ['PATH_TO_RGT_PACKAGE']

        #---Write log.

        if is_using_unix_logger:

            log_string = (
                  'logger -p local0.notice "' +
                  'rgt_system_log_tag=\\"' + rgt_system_log_tag + '\\" ' +
                  'user=\\"' + user + '\\" ' +
                  'rgt_pbs_job_accnt_id=\\"' + rgt_pbs_job_accnt_id + '\\" ' +
                  'path_to_rgt_package=\\"' + path_to_rgt_package + '\\" ' +
                  'build_directory=\\"' + build_directory + '\\" ' +
                  'workdir=\\"' + workdir + '\\" ' +
                  'run_archive=\\"' + run_archive + '\\" ' +
                  'application=\\"' + application + '\\" ' +
                  'test=\\"' + test + '\\" ' +
                  'test_id_string=\\"' + test_id_string + '\\" ' +
                  'job_id=\\"' + job_id + '\\" ' +
                  'job_status=\\"' + job_status + '\\" ' +
                  'event_time=\\"' + event_time + '\\" ' +
                  event_name + '_event_value=\\"' + event_value + '\\" ' +
                  '"' )

#                  'event_name=\\"' + event_name + '\\" ' +
#                  'event_value=\\"' + event_value + '\\" ' +

            os.system(log_string)

        else:

            #---Alt: could use uuid.uuid1()

            log_file = application + '_#_' + \
                       test + '_#_' + \
                       test_id_string + \
                       '.txt'

            log_path = os.path.join(rgt_system_log_dir, log_file)

            log_string = \
                     'rgt_system_log_tag="' + rgt_system_log_tag + '" ' + \
                     'user="' + user + '" ' + \
                     'rgt_pbs_job_accnt_id="' + rgt_pbs_job_accnt_id + '" ' + \
                     'rgt_path_to_sspace="' + rgt_path_to_sspace + '" ' + \
                     'path_to_rgt_package="' + path_to_rgt_package + '" ' + \
                     'wd="' + wd + '" ' + \
                     'application="' + application + '" ' + \
                     'test="' + test + '" ' + \
                     'test_id_string="' + test_id_string + '" ' + \
                     'job_id="' + job_id + '" ' + \
                     'job_status="' + job_status + '" ' + \
                     'event_time="' + event_time + '" ' + \
                     event_name + '_event_value="' + event_value + '" ' + \
                     '\n'

#                     'event_name="' + event_name + '" ' + \
#                     'event_value="' + event_value + '" ' + \


            file_ = open(log_path, 'a')
            file_.write(log_string)
            file_.close()

    def __write_system_log(self, event_name, event_value, event_time):
        """
        """
        rgt_status_file.write_system_log(self.__unique_id, event_name,
                                         event_value, event_time)


#-----------------------------------------------------
# Convert job status to numerical value              -
#                                                    -
#-----------------------------------------------------
def convert_to_job_status(job_exit_status):
    tmpsum = 0

    ival = job_exit_status["Pass_Fail"]
    tmpsum = tmpsum + ival*1

    ival = job_exit_status["Hardware_Faiure"]
    tmpsum = tmpsum + ival*2

    ival = job_exit_status["Performance_Failure"]
    tmpsum = tmpsum + ival*4

    ival = job_exit_status["Incorrect_Result"]
    tmpsum = tmpsum + ival*8

    return sum



#-----------------------------#
# Function: parse_status_file #
#-----------------------------#
def parse_status_file(path_to_status_file,startdate,enddate,mycomputer_with_events_record):

    number_of_tests = 0
    number_of_passed_tests = 0
    number_of_failed_tests = 0
    number_of_inconclusive_tests = 0

    shash = {"number_of_tests" : number_of_tests,
             "number_of_passed_tests" : number_of_passed_tests,
             "number_of_failed_tests" : number_of_failed_tests,
             "number_of_inconclusive_tests" : number_of_inconclusive_tests}

    failed_jobs = []

    if os.path.exists(path_to_status_file):
        pass
    else:
        return shash

    sfile_obj = open(path_to_status_file,'r')
    sfile_lines = sfile_obj.readlines()
    sfile_obj.close()

    print "parsing status file: ", path_to_status_file
    for line in sfile_lines:
        tmpline = line.lstrip()
        if len(tmpline) >0 and tmpline[0] != rgt_status_file.comment_line_entry:
            number_of_tests = number_of_tests + 1
            words = tmpline.split()

            #Get the pbs id.
            pbsid1 = words[2]
            pbsid2 = pbsid1.split(".")
            pbsid = pbsid2[0]

            #Get the creation time.
            creationtime = words[0]

            # Get the number of passed tests.
            #Conservative check
            if  (mycomputer_with_events_record.in_time_range(pbsid,creationtime,startdate,enddate)) and (words[3].isdigit())  and (words[4].isdigit()) and (words[5].isdigit()) :
                if int(words[5]) == 0:
                    number_of_passed_tests = number_of_passed_tests + 1

                if int(words[5]) == 1:
                    number_of_failed_tests = number_of_failed_tests + 1

                if int(words[5]) >= 2:
                    number_of_inconclusive_tests = number_of_inconclusive_tests + 1
            else:
                number_of_tests = number_of_tests - 1

            #Agressive check
            #if (words[2].find('.nid') >= 0) :
            #    if words[5].isdigit():
            #        if int(words[5]) == 0:
            #            number_of_passed_tests = number_of_passed_tests + 1

            #    if words[5].isdigit():
            #        if (int(words[5])==1) or (words[3].find('***') >= 0) or (words[4].find('***') >= 0) or ( words[5].find('***') >= 0):
            #            number_of_failed_tests = number_of_failed_tests + 1
            #    elif words[5].find('***') >= 0:
            #        if (words[3].find('***') >= 0) or (words[4].find('***') >= 0) or ( words[5].find('***') >= 0):
            #            number_of_failed_tests = number_of_failed_tests + 1
            #else:
            #    number_of_tests = number_of_tests - 1


    shash = {"number_of_tests" : number_of_tests,
             "number_of_passed_tests" : number_of_passed_tests,
             "number_of_failed_tests" : number_of_failed_tests,
             "number_of_inconclusive_tests" : number_of_inconclusive_tests}


    return shash,failed_jobs



#-----------------------------#
# Function: parse_status_file #
#-----------------------------#
def parse_status_file2(path_to_status_file):

    number_of_tests = 0
    number_of_passed_tests = 0
    number_of_failed_tests = 0
    number_of_inconclusive_tests = 0

    shash = {"number_of_tests" : number_of_tests,
             "number_of_passed_tests" : number_of_passed_tests,
             "number_of_failed_tests" : number_of_failed_tests,
             "number_of_inconclusive_tests" : number_of_inconclusive_tests}

    failed_jobs = []

    if os.path.exists(path_to_status_file):
        pass
    else:
        return shash

    sfile_obj = open(path_to_status_file,'r')
    sfile_lines = sfile_obj.readlines()
    sfile_obj.close()

    print "parsing status file: ", path_to_status_file
    for line in sfile_lines:
        tmpline = line.lstrip()
        if len(tmpline) >0 and tmpline[0] != rgt_status_file.comment_line_entry:
            number_of_tests = number_of_tests + 1
            words = tmpline.split()

            # Get the number of passed tests.
            #Conservative check
            if  (words[3].isdigit())  and (words[4].isdigit()) and (words[5].isdigit()) :
                if int(words[5]) == 0:
                    number_of_passed_tests = number_of_passed_tests + 1

                if int(words[5]) == 1:
                    number_of_failed_tests = number_of_failed_tests + 1

                if int(words[5]) >= 2:
                    number_of_inconclusive_tests = number_of_inconclusive_tests + 1
            else:
                number_of_tests = number_of_tests - 1

            #Agressive check
            #if (words[2].find('.nid') >= 0) :
            #    if words[5].isdigit():
            #        if int(words[5]) == 0:
            #            number_of_passed_tests = number_of_passed_tests + 1

            #    if words[5].isdigit():
            #        if (int(words[5])==1) or (words[3].find('***') >= 0) or (words[4].find('***') >= 0) or ( words[5].find('***') >= 0):
            #            number_of_failed_tests = number_of_failed_tests + 1
            #    elif words[5].find('***') >= 0:
            #        if (words[3].find('***') >= 0) or (words[4].find('***') >= 0) or ( words[5].find('***') >= 0):
            #            number_of_failed_tests = number_of_failed_tests + 1
            #else:
            #    number_of_tests = number_of_tests - 1


    shash = {"number_of_tests" : number_of_tests,
             "number_of_passed_tests" : number_of_passed_tests,
             "number_of_failed_tests" : number_of_failed_tests,
             "number_of_inconclusive_tests" : number_of_inconclusive_tests}

    print "shash=",shash
    print "failed_jobs=",failed_jobs
    return shash,failed_jobs



def summarize_status_file(path_to_status_file,startdate,enddate,mycomputer_with_events_record):
    sfile_obj = open(path_to_status_file,'r')
    sfile_lines = sfile_obj.readlines()
    sfile_obj.close()

    number_of_tests = 0
    number_of_passed_tests = 0
    number_of_failed_tests = 0
    number_of_inconclusive_tests = 0

    flist = []
    ilist = []
    print "parsing status file: ", path_to_status_file
    for line in sfile_lines:
        tmpline = line.lstrip()
        if len(tmpline) >0 and tmpline[0] != rgt_status_file.comment_line_entry:
            words = tmpline.split()

            #Get the pbs id.
            pbsid1 = words[2]
            pbsid2 = pbsid1.split(".")
            pbsid = pbsid2[0]

            print "===="
            print "Test instance: ", tmpline
            print "pbs job id: ",pbsid 

            #Get the creation time.
            creationtime = words[0]
            (creationtime1, creationtime2) = creationtime.split("T")
            (year,month,day) = creationtime1.split("-")
            (time1,time2) = creationtime2.split(".")
            (hour,min,sec) = time1.split(":")
            creationdate = datetime.datetime(int(year),int(month),int(day))

            # Get the number of passed tests.
            #Conservative check
            if (mycomputer_with_events_record.in_time_range(pbsid,creationtime,startdate,enddate)):
                print "In range"

                number_of_tests = number_of_tests + 1

                if (words[2].isdigit()) and (words[3].isdigit())  and (words[4].isdigit()) and (words[5].isdigit()) :
                    if int(words[5]) == 0:
                        number_of_passed_tests = number_of_passed_tests + 1

                    if int(words[5]) >= 1:
                        number_of_failed_tests = number_of_failed_tests + 1
                        flist = flist + [words[1]]

                    if int(words[5]) == -1:
                        number_of_inconclusive_tests = number_of_inconclusive_tests + 1
                        ilist = ilist + [words[1]]

                elif (words[3] == "***")  or (words[4] == "***") or (words[5] == "***"):
                    number_of_inconclusive_tests = number_of_inconclusive_tests + 1

            elif (startdate <= creationdate) and (creationdate <= enddate) and  (pbsid == "***"):
                print "In range"
                number_of_tests = number_of_tests + 1
                number_of_inconclusive_tests = number_of_inconclusive_tests + 1
                ilist = ilist + [words[1]]
                
            print "number of  tests = ",number_of_tests 
            print "===="
            print
            print

            #Agressive check
            #if (words[2].find('.nid') >= 0) :
            #    if words[5].isdigit():
            #        if int(words[5]) == 0:
            #            number_of_passed_tests = number_of_passed_tests + 1

            #    if words[5].isdigit():
            #        if (int(words[5])==1) or (words[3].find('***') >= 0) or (words[4].find('***') >= 0) or ( words[5].find('***') >= 0):
            #            number_of_failed_tests = number_of_failed_tests + 1
            #    elif words[5].find('***') >= 0:
            #        if (words[3].find('***') >= 0) or (words[4].find('***') >= 0) or ( words[5].find('***') >= 0):
            #            number_of_failed_tests = number_of_failed_tests + 1
            #else:
            #    number_of_tests = number_of_tests - 1

    shash = {"number_of_tests" : number_of_tests,
             "number_of_passed_tests" : number_of_passed_tests,
             "number_of_failed_tests" : number_of_failed_tests,
             "number_of_inconclusive_tests" : number_of_inconclusive_tests,
             "failed_jobs" : flist,
             "inconclusive_jobs" : ilist}

    return shash