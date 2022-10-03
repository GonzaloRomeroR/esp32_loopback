import time
from socket import timeout
from utils.communication_utils import UARTCommunication
import matplotlib.pyplot as plt

from utils.sound_utils import *


def communicate(communication):
    while True:
        value = input()
        if value == "q":
            break
        print("Writing bytes")
        communication.send_data(value)
        print("Reading bytes")
        print(communication.receive_data(len(value)).decode("utf-8"))


def send_extracted_data(communication, data):
    """
    ["Duracion", "Cruces", "Maximo", "Simetria", "Desvio"]
    """
    communication.send_data(f"::t{data[0]}")
    communication.send_data(f"::c{data[1]}")
    communication.send_data(f"::m{data[2]}")
    communication.send_data(f"::s{data[3]}")
    communication.send_data(f"::d{data[4]}")


def send_audio(communication):
    file_name = "audios_recording_01"
    sample_rate, data = upload_audio_file(f"../data/{file_name}.wav")
    noise_gate = NoiseGate(open_threshold=30000, close_threshold=20000, hold=1)
    audio_c = []
    audio_python = []
    for value in data:
        python_value = noise_gate.real_time_filter(value, sample_rate)
        audio_python.append(python_value)
        print(python_value)
        communication.send_data(f"::{value}")
        c_value = communication.receive_data(1).decode("utf-8")
        print(c_value)
        audio_c.append(c_value)
    plt.plot(audio_c)
    plt.show()

    plt.plot(audio_python)
    plt.show()


def main():
    uart = UARTCommunication()
    uart.configure(port="COM6", baudrate=115200, timeout=10)
    uart.open_communication()
    # communicate(uart)
    for i in range(10):
        send_extracted_data(uart, [1.1, 2.1, 3, 6, 4.1])
        time.sleep(1)
    # send_audio(uart)
    uart.close_communication()


if __name__ == "__main__":
    main()
