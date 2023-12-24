# main.py
from FCFS.FCFS import fcfs
from LLF.llf import llf_function
from EDF.edf import edf_function
from SJF.SJF_without_preemption import sjf_without_preemption
from preemptif_SJF.SJF_with_preemption import sjf_with_preemption
from RM.rm import rm_runner
from DM.dm import dm_runner

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple

app = FastAPI()


class Task(BaseModel):
    Process_ID: int
    Task: int
    Arrival_Time: int
    Burst_Time: int
    Deadline: int
    Period: int


class SchedulingRequest(BaseModel):
    algorithm: str
    table: List[Task]


class SchedulingResponse(BaseModel):
    wts: List[float]
    awt: float
    cpu_utz: float
    gantt: List[Tuple[str, float]]


@app.post("/schedule")
async def schedule_table(request: SchedulingRequest):
    algorithm = request.algorithm.lower()
    table = request.table
    cpu_utz = 0
    awt = 0
    wts = []
    gantt = []

    # Transform data to match the expected format
    transformed_table = [
        {
            "Process_ID": task.Process_ID,
            "Task": task.Process_ID,
            "Arrival_Time": task.Arrival_Time,
            "Burst_Time": task.Burst_Time,
            "Deadline": task.Deadline,
            "Period": task.Period,
        }
        for task in table
    ]
    if algorithm == "edf" or algorithm == "dm" or algorithm == "rm" or algorithm == "llf":
        if algorithm == "edf":
            cpu_utz, gantt = edf_function(transformed_table)
        elif algorithm == "dm":
            cpu_utz, gantt = dm_runner(transformed_table)
        elif algorithm == "rm":
            cpu_utz, gantt = rm_runner(transformed_table)
        elif algorithm == "llf":
            cpu_utz, gantt = llf_function(transformed_table)
        return SchedulingResponse(wts=wts, awt=awt, cpu_utz=cpu_utz, gantt=gantt)

    elif algorithm == "fcfs" or algorithm == "sjf without preemption" or algorithm == "sjf with preemption":
        if algorithm == "fcfs":
            wts, awt, gantt = fcfs(transformed_table)
        elif algorithm == "sjf without preemption":
            wts, awt, gantt = sjf_without_preemption(transformed_table);
        elif algorithm == "sjf with preemption":
            wts, awt, gantt = sjf_with_preemption(transformed_table);
        return SchedulingResponse(wts=wts, awt=awt, cpu_utz=cpu_utz, gantt=gantt)
    else:
        return {"error": "Invalid sorting algorithm"}
