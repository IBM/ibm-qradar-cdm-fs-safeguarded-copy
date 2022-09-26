# Proactive Early Threat Detection and Securing SQL Database With IBM QRadar and IBM Spectrum Copy Data Management using IBM FlashSystem Safeguarded Copy

# Documentation:

Refer to Resources section for various links to IBM Documentation about IBM QRadar, IBM Spectrum Copy Data Management and IBM FlashSystem.


# Support

The _sample_ Python code available in the repository is created as part of solution. There is __no__ official support on the code.

# Disclaimer

The script is purely created as a PoC and it is developed and tested in controlled lab environment. There is __no__ official support on the script. You may use the script as a template to create your own workflow.

# Workflow

For both control and data path use cases, we heavily depend on the audit logs, network flows in order to track the actions. IBM QRadar is used for threat detection. The audit logs from storage and network flows / logs are used to determine whether the storage is under attack. This is done using IBM QRadar's rules engine, and when the threat is detected a pre-defined custom action is triggered ( in this case run_restore_job.py ) that will execute a restore job PREDEFINED in IBM Copy Data Management and restores the latest safeguarded copy in a clean room environment for further scrutiny.

# Pre-requisites

Following section lists the pre-requisites.

    - IBM Copy Data Management installation
    - A predefined RESTORE job in IBM Copy Data Management
    - A host with all software pre-requisites to be used as clean room
    - IBM FlashSystem with a Safeguarded Copy schedule defined for application volumes

# run_restore_job.py

The script is a python implementation of a wrapper to invoke CSM API commands to interact with DS8K storage to invoke DS8K - Safeguarded Copy functionality. It is deployed in IBM QRadar environment with a set of parameters shown below by the Usage section.

```
Usage: run_restore_job.py [-h] -s CDM_SERVER [-p CDM_PORT] -u CDM_USER -P CDM_PASS -j RESTORE_JOB_NAME

optional arguments:
  -h, --help            show this help message and exit
  -s CDM_SERVER, --cdm_server CDM_SERVER
                        <Mandatory> IP/FQDN of CDM server
  -p CDM_PORT, --cdm_port CDM_PORT
                        <Optional> Port of CDM server
  -u CDM_USER, --cdm_user CDM_USER
                        <Mandatory> CDM user
  -P CDM_PASS, --cdm_pass CDM_PASS
                        <Mandatory> CDM user Password
  -j RESTORE_JOB_NAME, --restore_job_name RESTORE_JOB_NAME
                        <Mandatory> CDM Restore Job name
```

# Resources

 - [Solution Blueprint]()
 - [IBM FlashSystem Safeguarded Copy](https://www.ibm.com/docs/en/flashsystem-9x00/8.5.x?topic=configuring-safeguarded-copy-function)
 - [IBM Spectrum Copy Data Management](https://www.ibm.com/docs/en/scdm/2.2.17)
