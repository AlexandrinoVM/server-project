import yaml
import paramiko
import getpass
import socket
import os

class ConnectionManager:
    def __init__(self, yaml_path="data.yaml"):
        self.yaml_path = yaml_path
        self.user = getpass.getuser()
        self.private_key_path = f"/home/{self.user}/.ssh/id_rsa"


    def exlude_server(self,name):
        existing = self.read_yaml()
        del existing['servers'][name]
        with open(self.yaml_path, "w") as f:
            yaml.safe_dump(existing, f,allow_unicode=True)

    def delete_command(self,name):
        existing = self.read_yaml()

        for i,command in enumerate(existing["commands"]):
            if command.get("name") == name:
                del existing["commands"][i]
                break
        else:
                raise ValueError(f"command with name '{name}' not found")

        with open(self.yaml_path,"w") as f:
            yaml.safe_dump(existing,f,allow_unicode=True)
        

    def read_yaml(self):
        try:
            with open(self.yaml_path, "r") as file:
                data = yaml.safe_load(file)
                return data if data else {}
        except FileNotFoundError:
            return {}
        except yaml.YAMLError:
            return {}

    def read_struct_yaml(self, section, item=None):
        data = self.read_yaml()
        if item:
            return data.get(section, {}).get(item)
        return data.get(section, {})

    def register_server(self, data):
        existing = self.read_yaml()

        if "servers" not in existing:
            existing["servers"] = {}
        if "servers_id" not in existing:
            existing["servers_id"] = 0

        new_id = existing["servers_id"]
        name_server = f"server_{new_id}"

        new_connection = {
            name_server: {
                "ip": data["ip"],
                "port": int(data["port"]),
                "name": data["name"],
                "password": data["password"],
                "log": False
            }
        }

        existing["servers"].update(new_connection)
        existing["servers_id"] += 1

        with open(self.yaml_path, "w") as f:
            yaml.dump(existing, f)

        return name_server
    
    def update_param(self,section,name,item,value):
        existing = self.read_yaml()
        existing[section][name][item] = value

        with open(self.yaml_path, "w") as f:
            yaml.dump(existing, f)

    def register_command(self,name,description,command):
        data = self.read_yaml()

        if "commands" not in data or data["commands"] is None:
            data["commands"] = []

        new_cmd = {
            "name": name,
            "description": description,
            "command": command
        }

        data["commands"].append(new_cmd)

        with open(self.yaml_path, "w") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)

    def paramiko_connect(self, name, command,connection_type):
        target = self.read_yaml()

        if name not in target.get("servers", {}):
            return f"Server {name} not found"

        server = target["servers"][name]
        print(server["name"])
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if not server.get("log", False) or connection_type == "password":
                client.connect(
                    hostname=server["ip"],
                    port=int(server["port"]),
                    username=server["name"],
                    password=server["password"],
                    look_for_keys=False,
                    allow_agent=False
                )
                self.update_param("servers",name,"log",True)
                print("conection by password")
            else:
                pkey = paramiko.RSAKey.from_private_key_file(self.private_key_path)
                client.connect(
                    hostname=server["ip"],
                    port=server["port"],
                    username=server["name"],
                    pkey=pkey
                )
                print("Conection by RSA key")

            stdin, stdout, stderr = client.exec_command(str(command))
            result = stdout.read().decode()
            print(result)
            return result

        except paramiko.AuthenticationException as e:
            print(f"Erro de autenticação: {e}")
            return str(e)
        except paramiko.SSHException as e:
            print(f"Erro de SSH: {e}")
            return str(e)
        except Exception as e:
            print(f"Erro geral: {type(e).__name__} - {e}")
            return str(e)        
        finally:
            client.close()

