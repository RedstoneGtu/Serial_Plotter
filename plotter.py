import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep
import serial
import sys
import glob

filename = input('Enter filename to save: ')
f = open(filename, 'w+')
f.close()

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*') + glob.glob('/dev/cu.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

ports = serial_ports()
for i, s in enumerate(ports):
    print('{:d}. port: {:s}'.format(i + 1, s))

sp = int(input('Enter the number of the serial port: '))
ser = serial.Serial()
ser.port = ports[sp - 1]
ser.baudrate = 115200
ser.timeout = 10
ser.open()
while not ser.is_open:
    print('Serial port could not open!\n')
    sleep(1)

print('Serial port open! Configuration:\n')
print(ser, "\n")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ys = [[], [], [], []]
xs = []

t = 0
def animate(i, xs, ys):
    line = ser.readline().decode("utf-8").strip()
    values = line.split(',')
    f = open(filename, 'a+')
    f.write(line + '\n')
    print(line)
    f.close()
	
    xs.append(i)
    global t
    t += 1

    ax.clear()
    for i in range(4):
        ys[i].append(int(values[i].strip()))
        ax.plot(xs, ys[i], label='{:d}. Photodiode'.format(i + 1))

    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Group 2 RedStone')
    plt.ylabel('RAW Values')
    plt.xlabel('Time')
    plt.legend()

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10)
plt.show()