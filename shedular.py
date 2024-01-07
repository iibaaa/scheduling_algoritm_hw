import os
import json
import copy
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


class Task:
    def __init__(self, t_name, t_config=None):
        self.name = t_name
        self.execution_time = t_config["execution_time"]
        self.period = t_config["period"]
        self.remain_runtime = -1
        self.execution_count = 0
        self.tasks_one_cycle_completed = False

    def reset(self):
        self.remain_runtime = self.execution_time

    def run(self):
        if self.tasks_one_cycle_completed:
            self.execution_count += 1
            self.tasks_one_cycle_completed = False

        self.remain_runtime -= 1

        if self.remain_runtime == 0:
            self.tasks_one_cycle_completed = True

    def get_remain_runtime(self):
        return self.remain_runtime


class SchedulingStrategy(ABC):
    @abstractmethod
    def find_next_running_task(self, ready_to_run_tasks_queue):
        pass

    @abstractmethod
    def check_schedulability(self, tasks):
        pass


class RateMonotonicStrategy(SchedulingStrategy):
    def find_next_running_task(self, ready_to_run_tasks_queue):
        # Find the task with the highest priority in ready_to_run_tasks_queue
        # The task with the highest priority is the task with the shortest period
        next_running_task = ready_to_run_tasks_queue[0]
        for task in ready_to_run_tasks_queue:
            if task.period < next_running_task.period:
                next_running_task = task

        return next_running_task

    def check_schedulability(self, tasks):
        number_of_tasks = len(tasks)
        utilization = sum([task.execution_time / task.period for task in tasks])
        # bound = number_of_tasks * (2 ** (1 / number_of_tasks) - 1)
        ## TODO: update this part later
        bound = 1.0  # Hocaya sorulan sorudan dolayı bu şekilde değiştirildi
        if utilization <= bound:
            return True
        else:
            return False


class EarliestDeadLineFirstStrategy(SchedulingStrategy):
    def find_next_running_task(self, ready_to_run_tasks_queue):
        # Find the task earliest deadline in ready_to_run_tasks_queue
        # The task with the earliest deadline is the task with the shortest remain_runtime
        next_running_task = ready_to_run_tasks_queue[0]
        for task in ready_to_run_tasks_queue:
            if task.remain_runtime < next_running_task.remain_runtime:
                next_running_task = task

        return next_running_task

    def check_schedulability(self, tasks):
        utilization = sum([task.execution_time / task.period for task in tasks])
        if utilization <= 1:
            return True
        else:
            return False


class Schedular:

    def __init__(self, tasks=None, scheduling_strategy=None):
        self.tasks = copy.deepcopy(tasks)
        self.sim_time = 0

        self.ready_to_run_tasks_queue = []
        self.time_line = []
        self.scheduling_strategy = scheduling_strategy
        self.algorithm_name = self.scheduling_strategy.__class__.__name__

    def calculate_which_task_ready_to_run(self, t):
        for task in self.tasks:
            if t % task.period == 0:
                task.reset()
                self.ready_to_run_tasks_queue.append(task)

    def lcm_of_periods(self):
        periods = [task.period for task in self.tasks]
        lcm = periods[0]
        for i in periods[1:]:
            lcm = lcm * i // self.gcd(lcm, i)
        return lcm

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def get_output(self):
        return self.time_line

    def schedule(self):
        # Check if the tasks are schedulable
        if not self.scheduling_strategy.check_schedulability(self.tasks):
            msg = f"Tasks are not schedule with {self.scheduling_strategy.__class__.__name__} algorithm"
            raise Exception(msg)

        # Calculate the max time
        self.sim_time = self.lcm_of_periods() + 1  # +1 time unit for see the complete cycle start again

        for time in range(self.sim_time):
            # Find which task is ready to run at this time
            self.calculate_which_task_ready_to_run(time)

            # Check if there is any task ready to run
            if len(self.ready_to_run_tasks_queue) == 0:
                out = {"time": time, "task": "Idle", "execution_count": 0}
                self.time_line.append(out)
                continue

            # Find the task with the highest priority in ready_to_run_tasks_queue
            next_running_task = self.scheduling_strategy.find_next_running_task(self.ready_to_run_tasks_queue)
            next_running_task.run()
            out = {"time": time, "task": next_running_task.name, "execution_count": next_running_task.execution_count}
            self.time_line.append(out)
            if next_running_task.get_remain_runtime() == 0:
                self.ready_to_run_tasks_queue.remove(next_running_task)


def display_schedular_output(shed, task_names=None):
    colors = ["tab:gray", "tab:blue", "tab:orange", "tab:green"]

    fig, ax = plt.subplots(figsize=(10, 5))
    if task_names is None:
        ax.set_title(shed.algorithm_name)
    else:
        ax.set_title(f"{task_names} - {shed.algorithm_name}")

    task_names = [task.name for task in shed.tasks] + ["Idle"]

    for i, task_name in enumerate(task_names):
        task_time_line = [out["time"] for out in shed.time_line if out["task"] == task_name]
        task_execution_count = [out["execution_count"] for out in shed.time_line if out["task"] == task_name]
        for ttl, tec in zip(task_time_line, task_execution_count):
            ax.broken_barh([(ttl, 1)], ((i - 0.4), 0.8), facecolors=colors[tec % len(colors)])

    # Set Labels
    ax.set_xlabel("Time")
    ax.set_ylabel("Tasks")

    # Set X ticks
    ax.set_xticks(range(shed.sim_time))
    ax.set_xticklabels(range(shed.sim_time))

    # Set Y ticks
    ax.set_yticks(range(len(task_names)))
    ax.set_yticklabels(task_names)

    ax.grid(True, axis="x")
    ax.grid(True, axis="y", linestyle="--")

    return fig


def load_tasks_from_json(file_name):
    with open(file_name) as f:
        tasks_config = json.load(f)

    tasks = []
    for idx, task_config in enumerate(tasks_config["tasks"]):
        task_name = f"Task{idx + 1}"
        tasks.append(Task(task_name, task_config))

    return tasks


def main(args):
    tasks = load_tasks_from_json(args.taskset)

    schedules = [
        Schedular(tasks=tasks, scheduling_strategy=RateMonotonicStrategy()),
        Schedular(tasks=tasks, scheduling_strategy=EarliestDeadLineFirstStrategy())
    ]

    for shed in schedules:
        try:
            shed.schedule()
        except Exception as e:
            print(e)
            continue

        fig = display_schedular_output(shed, args.taskset.split(".json")[0])

        if args.save_location != "None":
            if not os.path.exists(args.save_location):
                os.makedirs(args.save_location)

            task_name = args.taskset.split(".json")[0]
            output_name = f"{task_name}_{shed.algorithm_name}.png"
            file_name = os.path.join(args.save_location, output_name)
            fig.savefig(file_name)

    if args.show_plots:
        plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run Schedular')
    parser.add_argument('--taskset', type=str, default="Test4.json", help='tasks config file name')
    parser.add_argument('--save_location', type=str, default="outputs", help='save location')
    parser.add_argument('--show_plots', type=bool, default=True, help='show Schedular output')
    args = parser.parse_args()

    main(args)
