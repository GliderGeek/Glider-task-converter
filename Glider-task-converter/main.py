import csv
import os
from TaskReader import TaskReader
from FlarmWriter import FlarmWriter
from Tkinter import Label, Tk, Button, Entry, W
import tkFileDialog

cup_file_chosen = False
flarm_directory_chosen = False

root = Tk()

def start_conversion():
    global complete_cup_filename, flarm_directory

    short_flarm_filename = "flarmcfg.txt"
    complete_flarm_filename = os.path.join(flarm_directory, short_flarm_filename)

    SeeYou_waypoints, SeeYou_task, task_name, task_options = read_SeeYou_file(complete_cup_filename)
    write_flarm_cfg(complete_flarm_filename, SeeYou_task, task_name)

    conversion_status.configure(text="done")
    conversion_status.update()


def get_cup_filename():
    global complete_cup_filename, cup_file_chosen

    complete_cup_filename = tkFileDialog.askopenfilename()
    short_cup_filename = complete_cup_filename.split("/")[-1]
    cup_filename.configure(text=short_cup_filename)
    cup_filename.update()

    if short_cup_filename != "":
        cup_file_chosen = True
    else:
        cup_file_chosen = False

    if cup_file_chosen and flarm_directory_chosen:
        convert.config(state="normal")
        convert.update()
    else:
        convert.config(state="disabled")
        convert.update()
        conversion_status.config(text="")
        conversion_status.update()


def get_flarm_directory():
    global complete_cup_filename, flarm_directory, flarm_directory_chosen

    flarm_directory = tkFileDialog.askdirectory()
    flarm_directory_short = flarm_directory.split("/")[-1]
    flarm_directory_name.configure(text=flarm_directory_short)
    flarm_directory_name.update()

    if flarm_directory != "":
        flarm_directory_chosen = True
    else:
        flarm_directory_chosen = False

    if cup_file_chosen and flarm_directory_chosen:
        convert.config(state="normal")
        convert.update()
    else:
        convert.config(state="disabled")
        convert.update()
        conversion_status.config(text="")
        conversion_status.update()


def read_SeeYou_file(filename):
    # Reading information from cup file

    _SeeYou_waypoints = []
    _SeeYou_task = None
    _task_name = ""
    _task_options = None

    with open(filename, 'r') as fp:
        reader = TaskReader(fp)

        in_header = True
        for fields in csv.reader(fp):
            if fields[0].startswith("-----Related Tasks"):              # dividing line between header and body
                in_header = False
                continue
            elif in_header:                                             # waypoints info in header
                waypoint = reader.decode_waypoint(fields)
                if waypoint is not None:
                    _SeeYou_waypoints.append(waypoint)
            elif not in_header and fields[0] == "Options":              # lines with options for task
                _task_options = reader.decode_options(fields)
            elif not in_header and fields[0].startswith("ObsZone"):     # taskpoint
                reader.decode_taskpoint(fields, _SeeYou_task)
            else:                                                       # list of turnpoints
                _SeeYou_task = reader.decode_taskList(fields, _SeeYou_waypoints)
                _task_name = reader.decode_taskName(fields)

    return _SeeYou_waypoints, _SeeYou_task, _task_name, _task_options


def write_flarm_cfg(filename, _SeeYou_task, _task_name):
    # Writing information to flarm config file
    with open(filename, 'w') as fp:
        writer = FlarmWriter(fp)

        Flarm_waypoints = writer.get_flarm_waypoints(_SeeYou_task)

        task_info = {
            # "competition_class": "Clubclass",
            # "competition_id": "GO4",
            # "pilot": "GliderGeek",
            # "glider_id": "PH-790",
            # "glider_type": "LS4",
            # "logger_interval": 1,
            "waypoints": Flarm_waypoints,
            "task_name": _task_name
        }

        writer.write_flarm_task(writer, task_info)

title = Label(root, text="Glider-task-converter", font=("Helvetica", 30))
load_cup = Button(root, text="Load .cup file", command=get_cup_filename)
cup_filename = Label(root, text="")
write_flarm = Button(root, text="Destination folder", command=get_flarm_directory)
flarm_directory_name = Label(root, text="")
convert = Button(root, text="Convert", command=start_conversion, state="disabled")
conversion_status = Label(root, text="")

title.grid(row=0, column=0)
load_cup.grid(row=1, column=0)
cup_filename.grid(row=1, column=1)
write_flarm.grid(row=2, column=0)
flarm_directory_name.grid(row=2, column=1)
convert.grid(row=3, column=0)
conversion_status.grid(row=3, column=1)

root.mainloop()
