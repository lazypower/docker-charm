#!/usr/bin/env python
"""
Simple script to parse iperf transaction results
and reformat them as JSON for sending back to juju
"""
import sys
import subprocess
import json
from charmhelpers.contrib.benchmark import Benchmark


def action_set(key, val):
    action_cmd = ['action-set']
    if isinstance(val, dict):
        for k, v in val.iteritems():
            action_set('%s.%s' % (key, k), v)
        return

    action_cmd.append('%s=%s' % (key, val))
    subprocess.check_call(action_cmd)


def parse_stress_output():
    """
    Parse the output from iperf and set the action results:

                               self            server
    timestamp      self ip      port   server    port  interval   transfer    bandwidth
    20150513173902,172.17.0.19,40403,172.17.0.4,5001,3,0.0-1.0,3803054080,30424432640
    20150513173903,172.17.0.19,40403,172.17.0.4,5001,3,1.0-2.0,3286237184,26289897472
    20150513173904,172.17.0.19,40403,172.17.0.4,5001,3,2.0-3.0,3142320128,25138561024
    20150513173905,172.17.0.19,40403,172.17.0.4,5001,3,3.0-4.0,2916220928,23329767424
    20150513173906,172.17.0.19,40403,172.17.0.4,5001,3,4.0-5.0,2932867072,23462936576
    20150513173907,172.17.0.19,40403,172.17.0.4,5001,3,5.0-6.0,2926837760,23414702080
    20150513173908,172.17.0.19,40403,172.17.0.4,5001,3,6.0-7.0,3103653888,24829231104
    20150513173909,172.17.0.19,40403,172.17.0.4,5001,3,7.0-8.0,4666425344,37331402752
    20150513173910,172.17.0.19,40403,172.17.0.4,5001,3,8.0-9.0,4636934144,37095473152
    20150513173911,172.17.0.19,40403,172.17.0.4,5001,3,9.0-10.0,4206886912,33655095296
    20150513173911,172.17.0.19,40403,172.17.0.4,5001,3,0.0-10.0,35621568512,28497120873
    """

    # Throw away the header
    # 58bd4e2b-51d8-4c48-893d-0809d653c778

    sys.stdin.readline()
    header = ['timestamp',
              'self-ip',
              'self-port',
              'server-ip',
              'server-port',
              'thread',
              'interval',
              'transfer',
              'bandwidth'
              ]

    report_header = ['transfer', 'bandwidth']

    results = []
    for line in sys.stdin.readlines():
        fields = line.rstrip().split(',')
        if len(header) == len(fields):
            result = {}
            for idx, field in enumerate(header):
                result[field] = fields[idx]
            results.append(result)

    action_set("meta.raw", json.dumps(results))

    # results dict should model { 'id' : { 'item': 'result' }, ... }
    total = {}  # Compute totals
    thread_interval = {}  # Keep running tally of occurrence
    total_transfer = 0
    for result in results:
        if result['thread'] not in total:
            total[result['thread']] = dict.fromkeys(report_header, 0)
            thread_interval[result['thread']] = 1
        else:
            for key in report_header:
                total[result['thread']][key] += int(result[key])
                thread_interval[result['thread']] += 1
        total_transfer += int(result['transfer'])

    for result in total:
        action_set(
               "results.thread-{}-transfer".format(result),
               {
                   'value': total[result]['transfer'] / thread_interval[result],
                   'units': 'Kb/sec'
               }
       )

        action_set(
               "results.thread-{}-bandwidth".format(result),
               {
                   'value': total[result]['bandwidth'] / thread_interval[result],
                   'units': 'Kb'
               }
        )

    # set total of all transfer
    total_transfer = total_transfer / len(results)
    Benchmark.set_composite_score(total_transfer, 'Kbs/sec', 'desc')


if __name__ == "__main__":
        parse_stress_output()
