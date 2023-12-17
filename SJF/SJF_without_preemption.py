def sjf_without_preemption(processes):
    # Sort the processes based on 'Arrival_Time' first
    processes = sorted(processes, key=lambda x: x['Arrival_Time'])
    # For the rest, sort by 'Burst_Time'
    processes[1:] = sorted(processes[1:], key=lambda x: x['Burst_Time'])
    current_time, waiting_times = 0, []
    gantt_chart = []
    for p in processes:
        if current_time < p['Arrival_Time']:
            gantt_chart.append(('Task No Task', p['Arrival_Time'] - current_time))
            current_time = p['Arrival_Time']

        waiting_times.append(current_time - p['Arrival_Time'])
        # Update Gantt chart with the current process
        gantt_chart.append((f'Task {p["Process_ID"]-1}', p['Burst_Time']))
        current_time += p['Burst_Time']
    return waiting_times, sum(waiting_times) / len(processes), gantt_chart
