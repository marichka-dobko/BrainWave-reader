import pandas as pd
from matplotlib.pyplot import figure, imshow, axis, savefig
import matplotlib.pyplot as plt

packet_buffer = ['04', '80', '02', '00', '3a', '43']
raw_form = [3, 4]
if len(packet_buffer) == 6:
    raw_encoded = packet_buffer[2]
    raw = int(raw_encoded[0]) * 256 + int(raw_encoded[1])
    if (raw >= 32768):
        raw = raw - 65536
    raw_form.append(raw)

pd.DataFrame({'signal': raw_form}).to_csv('wave.csv')
fig, ax = plt.subplots()
plt.plot(range(len(raw_form)), raw_form, color="blue")
ax.set_title("Brain Wave")
axis('off')
plt.tight_layout()

savefig('wave-1.png', bbox_inches='tight')