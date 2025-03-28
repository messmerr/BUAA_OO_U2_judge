import re

def calculate_performance_score(input_file="input.txt", output_file="output.txt"):
    """
    Calculates the performance score based on the given input and output files.
    """

    # 1. Parse input.txt
    passenger_requests = {}
    with open(input_file, "r") as f:
        for line in f:
            match = re.match(r"\[(\d+\.\d+)\](\d+)-PRI-\d+-FROM-\w+-TO-\w+-BY-\d+", line)
            if match:
                timestamp = float(match.group(1))
                passenger_id = int(match.group(2))
                passenger_requests[passenger_id] = timestamp

    # 2. Parse output.txt
    final_timestamp = 0
    arrive_count = 0
    open_count = 0
    close_count = 0
    passenger_arrival_times = {}
    with open(output_file, "r") as f:
        for line in f:
            match_arrive = re.match(r"\[\s*(\d+\.\d+)\]ARRIVE-\w+-\d+", line)
            if match_arrive:
                arrive_count += 1
                final_timestamp = max(final_timestamp, float(match_arrive.group(1)))
                continue

            match_open = re.match(r"\[\s*(\d+\.\d+)\]OPEN-\w+-\d+", line)
            if match_open:
                open_count += 1
                final_timestamp = max(final_timestamp, float(match_open.group(1)))
                continue

            match_close = re.match(r"\[\s*(\d+\.\d+)\]CLOSE-\w+-\d+", line)
            if match_close:
                close_count += 1
                final_timestamp = max(final_timestamp, float(match_close.group(1)))
                continue

            match_in = re.match(r"\[\s*(\d+\.\d+)\]IN-(\d+)-\w+-\d+", line)
            if match_in:
                final_timestamp = max(final_timestamp, float(match_in.group(1)))
                continue

            match_out = re.match(r"\[\s*(\d+\.\d+)\]OUT-(\d+)-\w+-\d+", line)
            if match_out:
                timestamp = float(match_out.group(1))
                passenger_id = int(match_out.group(2))
                passenger_arrival_times[passenger_id] = timestamp
                final_timestamp = max(final_timestamp, timestamp)
                continue

    # 3. Calculate Trun
    trun = final_timestamp

    # 4. Calculate WT
    weighted_time_sum = 0
    total_weight = 0
    for passenger_id, request_time in passenger_requests.items():
        if passenger_id in passenger_arrival_times:
            arrival_time = passenger_arrival_times[passenger_id]
            completion_time = arrival_time - request_time
            weighted_time_sum += completion_time * 1  # Assuming weight = 1
            total_weight += 1

    wt = weighted_time_sum / total_weight if total_weight > 0 else 0

    # 5. Calculate W
    w_arrive = 0.4
    w_open = 0.1
    w_close = 0.1
    w = w_open * open_count + w_close * close_count + w_arrive * arrive_count

    # 6. Print the raw metrics
    print(f"Trun: {trun:.4f}")
    print(f"WT: {wt:.4f}")
    print(f"W: {w:.4f}")

if __name__ == "__main__":
    calculate_performance_score()
