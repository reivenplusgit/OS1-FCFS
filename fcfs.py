def fcfs(processes):
    """
    First Come First Serve (FCFS) Scheduling Algorithm
    
    Parameters:
    processes (list of tuples): List of processes where each tuple contains 
                               (process_id, arrival_time, burst_time)
                               
    Returns:
    dict: A dictionary containing waiting times, turnaround times, and averages
    """
    # Step 1: Sort processes by arrival time (FCFS)
    processes.sort(key=lambda x: x[1])
    
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    
    # Step 2: Calculate waiting time for each process
    waiting_time[0] = 0  # First process has 0 waiting time
    
    for i in range(1, n):
        # Waiting time is previous process's finish time - current arrival time
        waiting_time[i] = max(0, (processes[i-1][2] + waiting_time[i-1] + processes[i-1][1] - processes[i][1]))
    
    # Step 3: Calculate turnaround time for each process
    for i in range(n):
        turnaround_time[i] = processes[i][2] + waiting_time[i]
    
    # Step 4: Calculate average times
    avg_waiting = sum(waiting_time) / n
    avg_turnaround = sum(turnaround_time) / n
    
    # Step 5: Return results
    return {
        "processes": processes,
        "waiting_time": waiting_time,
        "turnaround_time": turnaround_time,
        "avg_waiting": avg_waiting,
        "avg_turnaround": avg_turnaround
    }

def print_results(results):
    """Helper function to print the results in a readable format"""
    print("\nResults:")
    print("Process ID\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time")
    for i, process in enumerate(results["processes"]):
        print(f"{process[0]}\t\t{process[1]}\t\t{process[2]}\t\t{results['waiting_time'][i]}\t\t{results['turnaround_time'][i]}")
    
    print(f"\nAverage Waiting Time: {results['avg_waiting']:.2f}")
    print(f"Average Turnaround Time: {results['avg_turnaround']:.2f}")

def validate_process_id(pid, existing_ids):
    """Validate process ID"""
    if not pid.isdigit():
        return False, "Process ID must be a positive integer"
    if int(pid) <= 0:
        return False, "Process ID must be greater than 0"
    if int(pid) in existing_ids:
        return False, "Process ID must be unique"
    return True, ""

def validate_time_value(value, name):
    """Validate arrival and burst times"""
    if not value.isdigit():
        return False, f"{name} must be a non-negative integer"
    if int(value) < 0:
        return False, f"{name} cannot be negative"
    return True, ""

def get_user_input():
    """Gets and validates process details from user input"""
    processes = []
    existing_ids = set()
    print("\nEnter process details (enter 'done' when finished):")
    
    while True:
        user_input = input("Enter Process ID, Arrival Time, Burst Time (comma separated): ").strip()
        
        # Check for completion command
        if user_input.lower() == 'done':
            if not processes:
                print("Error: Please enter at least one process!")
                continue
            break
            
        # Split and validate input format
        parts = [part.strip() for part in user_input.split(',')]
        if len(parts) != 3:
            print("Error: Please enter exactly 3 values separated by commas!")
            continue
            
        pid, at, bt = parts
        
        # Validate Process ID
        valid_pid, pid_msg = validate_process_id(pid, existing_ids)
        if not valid_pid:
            print(f"Error: {pid_msg}")
            continue
            
        # Validate Arrival Time
        valid_at, at_msg = validate_time_value(at, "Arrival Time")
        if not valid_at:
            print(f"Error: {at_msg}")
            continue
            
        # Validate Burst Time
        valid_bt, bt_msg = validate_time_value(bt, "Burst Time")
        if not valid_bt:
            print(f"Error: {bt_msg}")
            continue
            
        # All validations passed
        pid_int = int(pid)
        existing_ids.add(pid_int)
        processes.append((pid_int, int(at), int(bt)))
        print(f"Process {pid} added successfully!")
    
    return processes

def main():
    while True:
        print("\n" + "="*50)
        print("First Come First Serve (FCFS) Scheduling Algorithm")
        print("="*50)
        
        try:
            # Get user input for processes
            user_processes = get_user_input()
            
            # Calculate and display results
            results = fcfs(user_processes)
            print_results(results)
            
            # Ask if user wants to try again
            while True:
                choice = input("\nDo you want to calculate again? (yes/no): ").strip().lower()
                if choice in ['yes', 'no']:
                    break
                print("Invalid choice! Please enter 'yes' or 'no'")
            
            if choice == 'no':
                print("\nThank you for using the FCFS scheduler. Goodbye!")
                break
                
        except KeyboardInterrupt:
            print("\n\nProgram terminated by user.")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {str(e)}")
            retry = input("Do you want to try again? (yes/no): ").strip().lower()
            if retry != 'yes':
                break

if __name__ == "__main__":
    main()