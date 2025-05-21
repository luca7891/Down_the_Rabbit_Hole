from multiprocessing import Process
import time
import subprocess
import os

# === CONFIG === #
VPN_SERVICE_NAME = "995F3290-DDCD-41B8-B2F6-3F4B98E0C1ED"
STATUS_FILE = "/Users/lucadutu/PycharmProjects/Programming for AI/BAP /Maintenance /status_file.lock"
# ============== #
def switch_vpn():
    print("Switching VPN...")
    subprocess.run(["scutil", "--nc", "stop", VPN_SERVICE_NAME])
    time.sleep(5)
    subprocess.run(["scutil", "--nc", "start", VPN_SERVICE_NAME])
    print("Waiting for VPN to stabilize...")

    # Check connection status up to 10 times
    for i in range(10):
        result = subprocess.run(
            ["scutil", "--nc", "status", VPN_SERVICE_NAME],
            capture_output=True, text=True
        )
        if "Connected" in result.stdout:
            print("VPN connected.")
            return
        print(f"[{i + 1}/10] VPN not ready yet...")
        time.sleep(2)

    print("Warning: VPN might not be connected.")


def run_bot1():
    import bot1
    bot1.start_scraping()


def run_bot2():
    import bot2
    bot2.start_scraping()


if __name__ == "__main__":
    if os.path.exists(STATUS_FILE):
        os.remove(STATUS_FILE)

    while True:
        switch_vpn()
        print("Launching bots...")

        p1 = Process(target=run_bot1)
        time.sleep(5)
        p2 = Process(target=run_bot2)


        p1.start()
        p2.start()


        time.sleep(1200)

        print("Terminating bots...")
        p2.terminate()
        p1.terminate()

        p2.join()
        p1.join()
