import os
from machine_types.machines.cray_xk7 import CrayXK7
from machine_types.machines.ibm_power8 import IBMpower8


class MachineFactory:

    @staticmethod
    def create_machine():
        rgt_machine_name = os.environ.get("RGT_MACHINE_NAME")
        rgt_scheduler_type = os.environ.get("RGT_SCHEDULER_TYPE")
        rgt_jobLauncher_type = os.environ.get("RGT_JOBLAUNCHER_TYPE")

        if rgt_machine_name == None:
            print('No machine name provided. Please set the RGT_MACHINE_NAME variable'.format(rgt_machine_name))

        if rgt_scheduler_type == None:
            print('No scheduler type provided. Please set the RGT_SCHEDULER_TYPE variable'.format(rgt_scheduler_type))

        if rgt_jobLauncher_type == None:
            print('No scheduler type provided. Please set the RGT_JOBLAUNCHER_TYPE variable'.format(rgt_jobLauncher_type))

        print("Creating machine "+str(rgt_machine_name)+" with scheduler "+str(rgt_scheduler_type)+" with job launcher "+str(rgt_jobLauncher_type))

        tmp_machine = None
        if rgt_machine_name == "Crest":
            tmp_machine = IBMpower8(name=rgt_machine_name,scheduler=rgt_scheduler_type,jobLauncher=rgt_jobLauncher_type)
        elif rgt_machine_name == "Chester":
            tmp_machine = CrayXK7(name=rgt_machine_name,scheduler=rgt_scheduler_type,jobLauncher=rgt_jobLauncher_type)
        else:
            print("Machine name does not exist. Good bye!")

        return tmp_machine

    def __init__(self):
        pass

