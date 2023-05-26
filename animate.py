import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def animate(i, dataList, ser):
    # ser.write(b'g')  # Transmit the char 'g' to receive the Arduino data point
    data = ser.read(10)

    try:
        # Convert the received data to hexadecimal
        hex_data = data.hex()
        res = hex_data.split('8002')[-1][:4]
        if len(res) == 4:
            # Print the buffered data as a packet
            byte1 = res[:2]
            byte2 = res[2:]

            raw = int(byte1, 16) * 256 + int(byte2, 16)
            if (raw >= 32768):
                raw = raw - 65536

            dataList.append(raw)
            print(raw)
        # arduinoData_float = float(arduinoData_string)  # Convert to float
        # dataList.append(arduinoData_float)  # Add to the list holding the fixed number of points to animate

    except:  # Pass if data point is bad
        pass

    dataList = dataList[-100:]  # Fix the list size so that the animation plot 'window' is x number of points

    ax.clear()  # Clear last data frame
    ax.plot(dataList)  # Plot new data frame

    ax.set_ylim([-3000, 3000])  # Set Y axis limit of plot
    ax.set_title("Arduino Data")  # Set title of figure
    ax.set_ylabel("Value")  # Set title of y axis


dataList = []  # Create empty list variable for later use

fig = plt.figure()  # Create Matplotlib plots fig is the 'higher level' plot window
ax = fig.add_subplot(111)  # Add subplot to main fig window

port = '/dev/cu.usbmodem14201'

ser = serial.Serial(port, 57600)  # Establish Serial object with COM port and BAUD rate to match Arduino Port/rate
time.sleep(2)  # Time delay for Arduino Serial initialization

# Matplotlib Animation Fuction that takes takes care of real time plot.
# Note that 'fargs' parameter is where we pass in our dataList and Serial object.
ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(dataList, ser), interval=100)

plt.show()  # Keep Matplotlib plot persistent on screen until it is closed
ser.close()