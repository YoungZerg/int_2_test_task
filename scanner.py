import paramiko
from db_connector import write_to_bd
import logging
from config import error_counter_global

logging.basicConfig(level=logging.INFO, filename='scanner.log', filemode='a',
                                format="""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
%(asctime)s [%(levelname)s]\n%(message)s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n""")

error_counter_global = 0


class Scanner:
    def __init__(self, log: str, passwd: str, port: int, ip: str) -> None:
        self.login = log
        self.password = passwd
        self.port = port
        self.ip_addr = ip
        self.os_type = ""
        self.kernel = ""
        self.architecture = ""
        
    

    def ssh_conn_n_parse(self) -> None:
        try:
            client = paramiko.SSHClient()
            #Setting policy because servers doesn't have a host key
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            logging.info(f"Connecting to {self.ip_addr}, (Port: {self.port}, Login: {self.login})")
            client.connect(hostname=self.ip_addr,
                           port=self.port,
                           username=self.login,
                           password=self.password)
            

            stdin, stdout, stderr = client.exec_command("hostnamectl")
            
            
            if stdout.channel.recv_exit_status() == 0:
                logging.info(f"Successfully connected to {self.ip_addr}")
                #parsing the result stored in stdout
                needed_info = ["Architecture", "Kernel", "Operating System"]
                os_params = [os_info.strip() for os_info in stdout.readlines() if os_info.strip()[:os_info.strip().find(":")] in needed_info]
                
                self.os_type, self.kernel, self.architecture = os_params
                #slicing strings to remove unnecessary parts such as "Architecture:" and etc and also removing whitespaces
                self.os_type = self.os_type[self.os_type.find(':')+1:].strip()
                self.kernel = self.kernel[self.kernel.find(':')+1:].strip()
                self.architecture = self.architecture[self.architecture.find(':')+1:].strip()
                logging.info("Proceeding to open database")
                write_to_bd(self.ip_addr, 
                            self.os_type, 
                            self.kernel, 
                            self.architecture)
            else:
                global error_counter_global
                error_counter_global = 1
                err_msg = stderr.read().decode("utf-8")
                logging.error(f"An error occured while executing command: {err_msg}")

            stdin.close()
            stdout.close()
            stderr.close()

        except Exception as ex:
            logging.error(f"Couldn't establish connection due to: {ex}")
        finally:
            client.close()