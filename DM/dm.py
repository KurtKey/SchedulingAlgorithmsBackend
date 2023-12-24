import random
from functools import reduce
from math import gcd

#A task instance
class TaskIns(object):

     #Constructor (should only be invoked with keyword parameters)
    def __init__(self, start, end, priority, name):
        self.start    = start
        self.end      = end
        self.usage    = 0
        self.priority = priority
        self.name     = name.replace("\n", "")
        self.id = int(random.random() * 10000)

    #Allow an instance to use the cpu (periodic)
    def use(self, usage):
        self.usage += usage
        if self.usage >= self.end - self.start:
            return True
        return False

    #Default representation
    def __repr__(self):
        return str(self.name) + "#" + str(self.id) + " - start: " + str(self.start) + " priority: " + str(self.priority) #+ budget_text

    #Get name as Name#id
    def get_unique_name(self):
        return str(self.name) + "#" + str(self.id)

#Task types (templates for periodic tasks)
class TaskType(object):

    #Constructor
    def __init__(self, period, release, execution, deadline, name):
        self.period    = period
        self.release   = release
        self.execution = execution
        self.deadline  = deadline
        self.name      = name

#Priority comparison
def priority_cmp(possible):
    return possible.priority

#Deadline monotonic comparison
def tasktype_cmp(task_type):
    return task_type.deadline


def _lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


def lcm(a):
    return reduce(_lcm, a)

# input_tasks = [
#     {"Task": 1, "Arrival_Time": 0, "Burst_Time": 3, "Deadline": 7, "Period": 20},
#     {"Task": 2, "Arrival_Time": 0, "Burst_Time": 2, "Deadline": 4, "Period": 5},
#     {"Task": 3, "Arrival_Time": 0, "Burst_Time": 2, "Deadline": 9, "Period": 10}
# ]

def dm_runner(input_tasks):
    task_types = []
    tasks = []
    hyperperiod = []
    gantt = []

    for input_task in input_tasks:
        task_types.append(TaskType(
            period=input_task["Period"],
            release=input_task["Arrival_Time"],
            execution=input_task["Burst_Time"],
            deadline=input_task["Deadline"],
            name=f'Task{input_task["Task"]}'
        ))

    # Calculate hyperperiod
    for task_type in task_types:
        hyperperiod.append(int(task_type.period))
    hyperperiod = lcm(hyperperiod)

    # Sort types rate monotonic
    task_types = sorted(task_types, key=tasktype_cmp)

    # Create task instances
    for i in range(0, hyperperiod):
        for task_type in task_types:
            if (i - task_type.release) % task_type.period == 0 and i >= task_type.release:
                start = i
                end = start + task_type.execution
                priority = task_type.deadline
                tasks.append(TaskIns(start=start, end=end, priority=priority, name=task_type.name))

    # Check utilization
    utilization = 0
    for task_type in task_types:
        utilization += float(task_type.execution) / float(task_type.period)
    if utilization > 1:
        print('Utilization error!')

    # Simulate clock
    clock_step = 1
    for i in range(0, hyperperiod, clock_step):
        # Fetch possible tasks that can use cpu and sort by priority
        possible = []
        for t in tasks:
            if t.start <= i:
                possible.append(t)
        possible = sorted(possible, key=priority_cmp)

        # Select task with the highest priority
        if len(possible) > 0:
            on_cpu = possible[0]
            print(on_cpu.get_unique_name(), " uses the processor. ", end=' ')
            gantt.append((on_cpu.name, clock_step))
            if on_cpu.use(clock_step):
                tasks.remove(on_cpu)
                print("Finish!", end=' ')
        else:
            print('No task uses the processor. ')
            gantt.append(('No Task', clock_step))
        print("\n")

    # Print remaining periodic tasks
    for p in tasks:
        print(p.get_unique_name() + " is dropped due to overload at time: " + str(i))
    print("Gantt chart:", gantt)
    return utilization, gantt

