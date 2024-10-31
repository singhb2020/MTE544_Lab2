import matplotlib.pyplot as plt
from utilities import FileReader
from numpy import linspace, exp
import textwrap



def plot_errors(filename_e_l, filename_e_a, filename_pos):
    ###positon stuff
    headers, values=FileReader(filename_pos).read_file()
    
    time_list=[]
    
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)
    
    
    fig, axes = plt.subplots(1,2, figsize=(14,6))

    title = "Y-Position (m) vs. X-Position (m) for PID-control on a Sigmoid Trajectory"
    wrapped_title = "\n".join(textwrap.wrap(title, width=40))
    axes[0].set_title(wrapped_title)
    axes[0].set_xlabel(r'X-Position (m)')
    axes[0].set_ylabel(r'Y-Position (m)')
    axes[0].grid()
    axes[0].plot([lin[0] for lin in values], [lin[1] for lin in values])

    #Errors Linear
    headers, values_l=FileReader(filename_e_l).read_file()
    
    time_list_l=[]
    first_stamp_l=values_l[0][-1]
    for val in values_l:
        time_list_l.append(val[-1] - first_stamp_l)

    #Errors Angular
    headers, values_a=FileReader(filename_e_a).read_file()
    
    time_list_a=[]
    first_stamp_a=values_a[0][-1]
    for val in values_a:
        time_list_a.append(val[-1] - first_stamp_a)


    title = "Linear Error (m) / Angular Error (rad) vs Time (ns) for PID-control on a Sigmoid Trajectory"
    wrapped_title = "\n".join(textwrap.wrap(title, width=51))
    axes[1].set_title(wrapped_title)
    axes[1].plot(time_list_l, [lin[0] for lin in values_l], label=r"Linear Error (m)")
    axes[1].plot(time_list_a, [lin[0] for lin in values_a], label=r"Angular Error (rad)")


    axes[1].set_xlabel(r"Time (ns)")
    axes[1].set_ylabel(r"Linear Error (m) | Angular Error (rad)")
    axes[1].legend()
    axes[1].grid()

    plt.show()
    
    





import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    # for filename in filenames:
    plot_errors(filenames[0], filenames[1], filenames[2])



