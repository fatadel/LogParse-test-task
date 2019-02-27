import re

from EventType import EventType
from LogColumn import LogColumn


def math_int_division(a, b):
    """
    Divides a by b and rounds result to the nearest integer value using simple mathematical rules
    """
    return int((a + b - 1) // b)


def percentile(sequence, k):
    """
    Counts k-th percentile in sequence
    Find more on
    https://www.dummies.com/education/math/statistics/how-to-calculate-percentiles-in-statistics/
    """
    sequence = sorted(sequence)
    index = k / 100 * len(sequence)
    if index.is_integer():
        index = int(index)
        return math_int_division(sequence[index] + sequence[index - 1], 2)
    else:
        index = math_int_division(index, 1)
        return sequence[index - 1]


with open('input.txt', 'r') as infile:
    # Dictionary of requests to frontend
    requests = {}
    for line in infile:
        # Split columns by one or more tabs
        # Stripping whitespaces from left and right of each line
        columns = re.split(r'\t+', line.strip())
        id_ = int(columns[LogColumn.ID.value])
        if columns[LogColumn.EVENT_TYPE.value] == EventType.START_REQUEST.value:
            # Save to dict request (to frontend) id as key
            # dt - start request event time (will be time delta after request finishes)
            # replica_groups - dictionary of replica groups (RG), number of RG as keys and
            # True/False depending if request to particular RG was successful or not
            requests.update(
                {
                    id_:
                        {
                            'dt': int(columns[LogColumn.TIME.value]),
                            'replica_groups': {}
                        }
                }
            )
        elif columns[LogColumn.EVENT_TYPE.value] == EventType.FINISH_REQUEST.value:
            # Turn dt into time delta for the request
            requests[id_]['dt'] = int(columns[LogColumn.TIME.value]) - requests[id_]['dt']
        elif columns[LogColumn.EVENT_TYPE.value] == EventType.BACKEND_REQUEST.value:
            # Add/update a request to RG
            requests[id_]['replica_groups'].update(
                {
                    int(columns[LogColumn.ADDITIONAL_INFO.value]): False
                }
            )
        elif columns[LogColumn.EVENT_TYPE.value] == EventType.BACKEND_OK.value:
            # Mark off successful requests
            requests[id_]['replica_groups'].update(
                {
                    int(columns[LogColumn.ADDITIONAL_INFO.value]): True
                }
            )

with open('output.txt', 'w') as outfile:
    # List of time deltas for each request to frontend
    time_deltas = []
    # Counter of requests to frontend that could not get data from all RGs
    count = 0
    for request in requests:
        time_deltas.append(requests[request]['dt'])
        for replica_group in requests[request]['replica_groups']:
            if not requests[request]['replica_groups'][replica_group]:
                count += 1
                break

    outfile.write('The 95-th percentile of frontend request processing time is '
                  f'{percentile(time_deltas, 95)} microsecond(s)\n')
    outfile.write(f'{count} request(s) to frontend could not get data from all replica groups\n')
