import re

from EventType import EventType
from LogColumn import LogColumn


def math_int_division(a, b):
    """ Divides a by b and rounds result to the nearest integer value using simple mathematical rules"""
    return int((a + b - 1) // b)


def percentile(sequence, k):
    """Counts k-th percentile in sequence"""
    sequence = sorted(sequence)
    index = k / 100 * len(sequence)
    if index.is_integer():
        index = int(index)
        return math_int_division(sequence[index] + sequence[index - 1], 2)
    else:
        index = math_int_division(index, 1)
        return sequence[index - 1]


with open('input.txt', 'r') as infile:
    requests = {}
    for line in infile:
        columns = re.split(r'\t+', line.strip())
        id_ = int(columns[LogColumn.ID.value])
        if columns[LogColumn.EVENT_TYPE.value] == EventType.START_REQUEST.value:
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
            requests[id_]['dt'] = int(columns[LogColumn.TIME.value]) - requests[id_]['dt']
        elif columns[LogColumn.EVENT_TYPE.value] == EventType.BACKEND_REQUEST.value:
            requests[id_]['replica_groups'].update(
                {
                    int(columns[LogColumn.ADDITIONAL_INFO.value]): False
                }
            )
        elif columns[LogColumn.EVENT_TYPE.value] == EventType.BACKEND_OK.value:
            requests[id_]['replica_groups'].update(
                {
                    int(columns[LogColumn.ADDITIONAL_INFO.value]): True
                }
            )

with open('output.txt', 'w') as outfile:
    time_deltas = []
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
