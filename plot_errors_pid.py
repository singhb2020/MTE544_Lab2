import matplotlib.pyplot as plt
from utilities import FileReader
from numpy import linspace, exp
import textwrap



def plot_errors(filename_e, filename_pos):
    full_range = linspace(start=0, stop=2.5, num=20)
    sig = [[i, 2 * (1 + exp(-2 * i)) - 1] for i in full_range]
    
    headers, values=FileReader(filename_e).read_file()
    
    time_list=[]
    
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    
    
    fig, axes = plt.subplots(1,2, figsize=(14,6))

    #axes[0].scatterplot(sig[0], sig[1])

    title = "Derivative Error (m/s) vs. Error (m) for PID-control"

    wrapped_title = "\n".join(textwrap.wrap(title, width=40))
    axes[0].set_title(wrapped_title)
    axes[0].set_xlabel(r'Error (m)')
    axes[0].set_ylabel(r'Derivative Error (m/s)')
    axes[0].grid()
    axes[0].plot([lin[0] for lin in values], [lin[1] for lin in values])

    
    title = "Error (m) / Derivative Error (m/s) vs Time (ns) for PID-control"
    wrapped_title = "\n".join(textwrap.wrap(title, width=47))
    axes[1].set_title(wrapped_title)
    axes[1].plot(time_list, [lin[0] for lin in values], label=r"Error (m)")
    axes[1].plot(time_list, [lin[1] for lin in values], label=r"Derivative Error (m/s)")

    axes[1].set_xlabel(r"Time (ns)")
    axes[1].set_ylabel(r"Error (m) | Derivative Error (m/s)")
    axes[1].legend()
    axes[1].grid()

    ###positon stuff
    headers, values=FileReader(filename_pos).read_file()
    
    time_list=[]
    
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    fig2, axes2 = plt.subplots(1,2, figsize=(14,6))

    title = "Y-Position (m) vs. X-Position (m) for PID-control"

    wrapped_title = "\n".join(textwrap.wrap(title, width=40))
    axes2[0].set_title(wrapped_title)
    axes2[0].set_xlabel(r'X-Position (m)')
    axes2[0].set_ylabel(r'Y-Position (m)')
    axes2[0].grid()
    axes2[0].plot([lin[0] for lin in values], [lin[1] for lin in values])

    
    title = r"X (m) / Y (m) / $\theta$ (rad) vs Time (ns) for PID-control"
    wrapped_title = "\n".join(textwrap.wrap(title, width=47))
    axes2[1].set_title(wrapped_title)
    axes2[1].plot(time_list, [lin[0] for lin in values], label=r"X (m)")
    axes2[1].plot(time_list, [lin[1] for lin in values], label=r"Y (m)")
    axes2[1].plot(time_list, [lin[2] for lin in values], label=r"$\theta$ (rad)")

    axes2[1].set_xlabel(r"Time (ns)")
    axes2[1].set_ylabel(r"X (m) | Y (m) | $\theta$ (rad)")
    axes2[1].legend()
    axes2[1].grid()

    plt.show()
    
    





import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    # for filename in filenames:
    plot_errors(filenames[0], filenames[1])



