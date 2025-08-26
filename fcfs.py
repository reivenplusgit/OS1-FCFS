import re

def fcfs(processes):
    """
    First Come First Serve (FCFS) Scheduling Algorithm
    """
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n

    current_time = 0

    for i, (pid, arrival, burst) in enumerate(processes):
        if current_time < arrival:  # CPU idle
            current_time = arrival
        
        start_time = current_time
        waiting_time[i] = start_time - arrival
        completion_time[i] = start_time + burst
        turnaround_time[i] = completion_time[i] - arrival

        current_time += burst  # move forward

    avg_waiting = sum(waiting_time) / n
    avg_turnaround = sum(turnaround_time) / n
    
    return {
        "processes": processes,
        "waiting_time": waiting_time,
        "turnaround_time": turnaround_time,
        "completion_time": completion_time,
        "avg_waiting": avg_waiting,
        "avg_turnaround": avg_turnaround
    }


def print_results(results):
    print("\nResults:")
    print("Process ID\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\tCompletion Time")
    for i, process in enumerate(results["processes"]):
        print(f"{process[0]}\t\t{process[1]}\t\t{process[2]}\t\t{results['waiting_time'][i]}\t\t{results['turnaround_time'][i]}\t\t{results['completion_time'][i]}")
    
    print(f"\nAverage Waiting Time: {results['avg_waiting']:.2f}")
    print(f"Average Turnaround Time: {results['avg_turnaround']:.2f}")


def validate_process_id(pid, existing_ids):
    """Validate process ID (must be unique, uppercase, alphanumeric, start with Letter+Number)"""
    if not pid:
        return False, "Process ID cannot be empty"
    if pid in existing_ids:
        return False, "Process ID must be unique"
    if not pid.isalnum():
        return False, "Process ID must be alphanumeric only (letters/numbers)"
    if not pid.isupper():
        return False, "Process ID must be in UPPERCASE letters"
    
    # Must start with a letter followed by at least one digit
    if not re.match(r"^[A-Z][0-9]+$", pid):
        return False, "Process ID must start with a LETTER followed by NUMBER(s) (e.g., P1, T2, X10)"
    
    return True, ""


def validate_time_value(value, name, allow_zero=True):
    """Validate arrival and burst times"""
    if not value.isdigit():
        return False, f"{name} must be a non-negative integer"
    val = int(value)
    if val < 0:
        return False, f"{name} cannot be negative"
    if not allow_zero and val == 0:
        return False, f"{name} must be greater than 0"
    return True, ""


def get_user_input():
    processes = []
    existing_ids = set()
    
    # Number of processes
    while True:
        num = input("Enter the number of processes (3-10) or type 'exit' to quit: ").strip()
        if num.lower() in ['exit', 'stop', 'quit']:
            return None  # Signal to quit
        if not num.isdigit():
            print("Error: Please enter a valid integer.")
            continue
        num = int(num)
        if num < 3 or num > 10:
            print("Error: Number of processes must be between 3 and 10.")
            continue
        break

    for i in range(1, num + 1):
        print(f"\n--- Process {i} ---")
        
        # Process ID
        while True:
            pid = input(f"Enter Process ID for Process {i} (e.g., P{i}, must be LETTER+NUMBER, uppercase): ").strip()
            valid_pid, msg = validate_process_id(pid, existing_ids)
            if not valid_pid:
                print(f"Error: {msg}")
                continue
            existing_ids.add(pid)
            break

        # Arrival Time
        while True:
            at = input(f"Enter Arrival Time for {pid}: ").strip()
            valid_at, msg = validate_time_value(at, "Arrival Time", allow_zero=True)
            if not valid_at:
                print(f"Error: {msg}")
                continue
            at = int(at)
            break

        # Burst Time
        while True:
            bt = input(f"Enter Burst Time for {pid}: ").strip()
            valid_bt, msg = validate_time_value(bt, "Burst Time", allow_zero=False)
            if not valid_bt:
                print(f"Error: {msg}")
                continue
            bt = int(bt)
            break

        processes.append((pid, at, bt))
        print(f"Process {pid} added successfully!")

    return processes


def main():
    while True:
        print("\n" + "="*60)
        print("First Come First Serve (FCFS) Scheduling Algorithm")
        print("="*60)
        
        try:
            user_processes = get_user_input()
            if user_processes is None:  # User chose to exit
                print("\nExiting program. Goodbye!")
                break
            
            results = fcfs(user_processes)
            print_results(results)
            
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
