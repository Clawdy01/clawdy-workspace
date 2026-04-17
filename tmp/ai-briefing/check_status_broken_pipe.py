#!/usr/bin/env python3
import subprocess
import sys

cmd = ['python3', 'scripts/ai-briefing-status.py', '--json']
producer = subprocess.Popen(cmd, cwd='/home/clawdy/.openclaw/workspace', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
consumer = subprocess.Popen(['head', '-n', '1'], stdin=producer.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
producer.stdout.close()
consumer_out, consumer_err = consumer.communicate()
producer_stderr = producer.stderr.read()
producer.wait()
print(f'producer_returncode={producer.returncode}')
print(f'consumer_returncode={consumer.returncode}')
print(f'consumer_first_line={consumer_out.strip()!r}')
print(f'producer_stderr_empty={not producer_stderr.strip()}')
if producer_stderr.strip():
    print('producer_stderr=' + producer_stderr.strip())
if producer.returncode != 0:
    sys.exit(producer.returncode)
