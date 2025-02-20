import docker
from datetime import datetime
from typing import Optional


class ContainerManager:

    def __init__(self) -> None:
        self.client = docker.from_env()
        self.container = None
        self.removing_in_progress = False

    def is_running(self) -> bool:
        try:
            if docker.from_env().containers.get(
                    self.container_name).status == 'running':
                self.is_already_setup = True
                return True
        except:
            return False

    def execute_script_in_container(self, script_path):
        if self.container:
            exec_log = self.container.exec_run(f"/bin/bash {script_path}",
                                               tty=True)
            return exec_log.output.decode()
        else:
            return "Container is not running."

    def create_scenario_running_script(self, container_id: str,
                                       script_dir: str,
                                       scenario_file_path: str,
                                       rviz_config_path: Optional[str],
                                       log_dir_path: str, record: bool,
                                       confVE_path: str):
        script_path = f"{script_dir}/run_scenario_{container_id}.sh"
        record_scenario = "true" if record else "false"

        with open(f"{script_path}", "w") as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"source /autoware/install/setup.bash\n")
            f.write(
                f"ros2 launch scenario_test_runner scenario_test_runner.launch.py \\\n"
            )
            f.write(f"architecture_type:=awf/universe/20230906 \\\n")
            f.write(f"record:={record_scenario} \\\n")
            f.write(f"scenario:={scenario_file_path} \\\n")
            f.write(f"output_directory:={log_dir_path} \\\n")
            f.write(f"global_timeout:=120 \\\n")
            if rviz_config_path is not None:
                f.write(f"rviz_config:={rviz_config_path} \\\n")
            f.write(f"global_timeout:=120 \\\n")
            f.write(f"sensor_model:=sample_sensor_kit \\\n")
            f.write(f"vehicle_model:=sample_vehicle")
        return script_path

    def create_env_setup_script(self, container_id: str, script_dir: str,
                                confVE_path: str):
        script_path = f"{script_dir}/setup_env_{container_id}.sh"

        with open(f"{script_path}", "w") as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"sudo cp -f {confVE_path}/bashrc ~/.bashrc \n")
            f.write("source ~/.bashrc\n")
            f.write("echo $CYCLONEDDS_URI\n")
            f.write("echo $RMW_IMPLEMENTATION\n")
            f.write("cat $(echo $CYCLONEDDS_URI)\n")

        return script_path

    def create_scenario_analyzing_script(self, container_id: str,
                                         script_dir: str, record_path: str,
                                         confVE_path: str,
                                         violation_analyzer_path: str,
                                         log_dir_path: str,
                                         map_path: str) -> str:
        script_path = f"{script_dir}/analyze_scenario_{container_id}.sh"

        with open(f"{script_path}", "w") as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"source /autoware/install/setup.bash\n")
            f.write(f"cd {confVE_path} \n")
            f.write(f"source venv/bin/activate \n")
            f.write(f"poetry install --no-root \n")
            f.write(
                f"poetry run python3 {violation_analyzer_path} {record_path} {log_dir_path} {map_path} \n"
            )

        return script_path

    def start_instance(self, container_id: str, container_name: str,
                       map_path: str, scenario_path: str, script_path: str,
                       log_path: str, project_path: str, docker_image_id: str,
                       display_gui: bool):
        print("Start instance")
        print("container name:", container_name)
        print("container id:", container_id)

        display = ':0' if display_gui else ''

        self.container = self.client.containers.run(
            docker_image_id,
            name=container_name,
            detach=True,  # Corresponds to '-d'
            tty=True,  # Corresponds to '-t'
            stdin_open=True,  # Corresponds to '-i'
            privileged=True,
            device_requests=[
                docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])
            ],  # '--gpus all'
            environment={
                'DISPLAY': display,
                'TERM': '',
                'QT_X11_NO_MITSHM': '1'
            },
            volumes={
                '/tmp/.X11-unix': {
                    'bind': '/tmp/.X11-unix',
                    'mode': 'rw'
                },
                map_path: {
                    'bind': map_path,
                    'mode': 'rw'
                },
                scenario_path: {
                    'bind': scenario_path,
                    'mode': 'rw'
                },
                log_path: {
                    'bind': log_path,
                    'mode': 'rw'
                },
                script_path: {
                    'bind': script_path,
                    'mode': 'rw'
                },
                project_path: {
                    'bind': project_path,
                    'mode': 'rw'
                },
                '/etc/localtime': {
                    'bind': '/etc/localtime',
                    'mode': 'ro'
                }
            })

    def remove_instance(self):
        if self.removing_in_progress:
            return
        print(f"Remove {self.container}")
        self.removing_in_progress = True
        self.container.stop()
        self.container.remove()
        self.container = None
        self.removing_in_progress = False

    def stop_container_if_timeout(self, timeout_sec: float):
        if not self.container:
            return

        result_dict = self.client.api.inspect_container(self.container.id)
        created_timestamp_str = result_dict["Created"]

        created_timestamp = datetime.fromisoformat(created_timestamp_str[:26])
        current_utc_time = datetime.utcnow()

        time_difference = current_utc_time - created_timestamp

        if timeout_sec <= time_difference.seconds:
            print(
                f"Stop Container since it is running for more than {timeout_sec} sec"
            )
            self.remove_instance()
