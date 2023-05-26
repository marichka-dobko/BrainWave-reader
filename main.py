import serial
import pandas as pd
from matplotlib.pyplot import figure, imshow, axis, savefig
import matplotlib.pyplot as plt
import ast
from numpy.fft import fft, ifft
import numpy as np


port = '/dev/cu.usbmodem14201'
baudrate = 57600

# Open the serial port
ser = serial.Serial(port, baudrate)

# Wait for the serial connection to be established
# ser.open()
if not ser.is_open:
    print(f"Failed to open port {port}")
    exit(1)

raw_waveform = []

try:
    packet_buffer = []  # Buffer to store received data for each packet
    i = 0
    while True:
        # Read data from the serial port
        data = ser.read()

        # Convert the received data to hexadecimal
        hex_data = data.hex()

        # Print the hexadecimal data
        # print(hex_data, end=' ')
        # Check for packet delimiter (0xAA)
        if hex_data == 'aa':
            if packet_buffer:
                # Print the buffered data as a packet
                if len(packet_buffer) == 6:
                    byte1 = packet_buffer[3]
                    byte2 = packet_buffer[4]

                    raw = int(byte1, 16) * 256 + int(byte2, 16)
                    if (raw >= 32768):
                        raw = raw - 65536

                    if i %10 ==0:
                        raw_waveform.append(raw)
                        print(raw)
                    i += 1
                # print("\nPacket:", ' '.join(packet_buffer))
                packet_buffer = []  # Reset the packet buffer
        else:
            # Add the non-delimiter data to the packet buffer
            packet_buffer.append(hex_data)

except KeyboardInterrupt:
    # Save collected data to csv
    pd.DataFrame({'signal': raw_waveform}).to_csv('wave.csv')
    # raw_waveform = raw_waveform[::10]

    fig, ax = plt.subplots()
    plt.plot(raw_waveform, color="blue")
    ax.set_title("Brain Wave")
    plt.tight_layout()
    savefig('wave.png', bbox_inches='tight')

    # fig, ax = plt.subplots()
    # plt.plot(np.abs(fft(raw_waveform)), color="blue")
    # ax.set_title("Brain Wave")
    # plt.tight_layout()
    # savefig('fft_wave.png', bbox_inches='tight')

    pass

# Close the serial port
ser.close()