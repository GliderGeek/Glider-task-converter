from aerofiles import FlarmConfigWriter


class FlarmWriter(FlarmConfigWriter):

    """
    This class is an extension to the FlarmConfigWriter from aerofiles
    It adds the following functionality:
    - convert SeeYou task (see TaskReader) to Flarm waypoint format
    - write to flarm config file using dictionary

    """

    type_dict = {
        "competition_class": str,
        "competition_id": str,
        "pilot": str,
        "glider_id": str,
        "glider_type": str,
        "logger_interval": int,
        "task_declaration": str,
        "waypoints": list,
        "waypoint": [float, float, str],
        "task_name": str
    }

    # Write reference to source code of this tool
    def write_header_info(self, fp):
        fp.write_line("//FLARM configuration file created with the open source tool Glider-task-converter")
        fp.write_line("//for information and development: github.com/GliderGeek/Glider-task-converter")
        fp.write_line("//!filename should be flarmcfg.txt to function")

    # Convert SeeYou_task to the flarm waypoints format (only lat, lon and name)
    def get_flarm_waypoints(self, SeeYou_task):
        flarm_waypoints = []
        for taskpoint in SeeYou_task:
            flarm_waypoints.append([
                taskpoint["latitude"],
                taskpoint["longitude"],
                taskpoint["name"]
            ])
        return flarm_waypoints

    # Check whether no invalid keys are used and values are of expected type
    def check_input(self, key, value):
        if key == "waypoints":

            if len(value) < 5:
                print "waypoints index should have at least 5 entries (takeoff, start, taskpoint, finish, landing)"
                exit(1)

            for waypoint_index in range(len(value)):
                for input_index in range(3):
                    if type(value[waypoint_index][input_index]) != self.type_dict["waypoint"][input_index] and\
                                    value[waypoint_index][input_index] is not None and\
                                    waypoint_index in[0, len(value)-1] and\
                                    input_index in [0, 1]:
                        print "Wrong formatting of waypoint %d (take-off = 0)" % waypoint_index
                        exit(1)
        elif type(value) != self.type_dict[key] and value is not None:
            print "Wrong formatting of %s: should be %s" % (key, str(self.type_dict[key]))
            exit(1)

    # Write flarm config file, using a dictionary as input
    def write_flarm_task(self, fp, task_dict):

        # check if waypoints are present
        if "waypoints" not in task_dict:
            print "There is no task provided to write_flarm_task!"
            exit(1)

        # check info input
        for key in task_dict.iterkeys():
            if key not in self.type_dict.iterkeys() or key == "waypoint":
                # key doesn't exist
                print "Incorrect function call on write_flarm_info(fp, key, value): %s is not an option" % key
                exit(1)
            else:
                # check input format of value
                self.check_input(key, task_dict[key])

        # write information
        else:

            self.write_header_info(fp)

            fp.write_line("")

            if "pilot" in task_dict and task_dict["pilot"] is not None:
                fp.write_pilot(task_dict["pilot"])
            if "competition_class" in task_dict and task_dict["competition_class"] is not None:
                fp.write_competition_class(task_dict["competition_class"])
            if "glider_type" in task_dict and task_dict["glider_type"] is not None:
                fp.write_glider_type(task_dict["glider_type"])
            if "glider_id" in task_dict and task_dict["glider_id"] is not None:
                fp.write_glider_id(task_dict["glider_id"])
            if "competition_id" in task_dict and task_dict["competition_id"] is not None:
                fp.write_competition_id(task_dict["competition_id"])

            fp.write_line("")
            if "logger_interval" in task_dict and task_dict["logger_interval"] is not None:
                fp.write_logger_interval(task_dict["logger_interval"])
            else:
                fp.write_logger_interval(1)

            fp.write_line("")
            fp.write_task_declaration(task_dict["task_name"])
            fp.write_waypoints(task_dict["waypoints"])
