from aerofiles import SeeYouReader


class TaskReader(SeeYouReader):
    """
    This class is an extension to SeeYouReader from aerofiles
    It adds functionality to read tasks instead of only waypoints
    """

    # Information about orientation, size and shape of taskpoint
    def decode_taskpoint(self, fields, task):
        taskpoint_info = {
            "Style": None,
            "R1": None,
            "A1": None,
            "R2": None,
            "A2": None,
            "A12": None,
            "Line": False,
            "Move": False,
            "Reduce": False
            # is this everything?
        }

        for field in fields:
            if field.split("=")[0] == "ObsZone":
                ObsZone = int(field.split("=")[1])
            elif field.split("=")[0] in ["Style", "A1", "A2", "A12"]:
                taskpoint_info[field.split("=")[0]] = field.split("=")[1]
            elif field.split("=")[0] in ["R1", "R2"]:
                taskpoint_info[field.split("=")[0]] = field.split("=")[1][0:-1]  # taking off m
            elif (field.split("=")[0] in ["Line", "Move", "Reduce"]) and (field.split("=")[1] == "1"):
                taskpoint_info[field.split("=")[0]] = True

        return task[ObsZone+1].update(taskpoint_info)

    # Information about task as a whole
    def decode_options(self, fields):
        if not fields[0] == "Options":
            return
        task_options = {
            "TaskTime": None,
            "WpDis": False,
            "MinDis": False,
            "RandomOrder": False,
            "MaxPts": None
            # what else needs in here?
        }

        for field in fields:
            if field == "Options":
                continue
            elif field.split("=")[0] in ["TaskTime"]:                                # string
                task_options[field.split("=")[0]] = field.split("=")[1]
            elif field.split("=")[0] in ["WpDis", "MinDis", "RandomOrder"]:          # boolean
                task_options[field.split("=")[0]] = bool(field.split("=")[1])
            elif field.split("=")[0] in ["MaxPts"]:                                  # int
                task_options[field.split("=")[0]] = int(field.split("=")[1])
            else:
                print "Missing option in options line!"
                exit(1)

        return task_options

    # Name and order of used waypoints
    def decode_taskList(self, fields, waypoints):
        task_list = fields[1::]

        task = []
        for index in range(len(task_list)):
            for waypoint in waypoints:
                if waypoint["name"] == task_list[index]:
                    taskpoint = {
                        "ObsZone": index-1,  # since take-off is -1
                        "name": waypoint["name"],
                        "latitude": waypoint["latitude"],
                        "longitude": waypoint["longitude"]
                    }
                    task.append(taskpoint)
                    break

        return task

    # Name of the task
    def decode_taskName(self, fields):
        return fields[0]
