from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.183"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("sh ip int br", use_textfsm=True)
        for status in result:
            pprint(status)
            print("Keys in status dictionary:", status.keys())

            # Adjust key names based on observed output
            interface = status.get("interface", "")
            status_value = status.get("status", "")
            if "GigabitEthernet" in status:
                if status["status"] == "up":
                    up += 1
                elif status["status"] == "down":
                    down += 1
                elif status["status"] == "administratively down":
                    admin_down += 1
                ans += f"{interface} is {status_value}, "

        #output GigabitEthernet1 up, GigabitEthernet2 up, GigabitEthernet3 down, GigabitEthernet4 administratively down -> 2 up, 1 down, 1 administratively down
        ans += f"-> {up} up, {down} down, {admin_down} administratively down"
        pprint(ans)
        return ans
