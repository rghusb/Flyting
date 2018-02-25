#!/usr/bin/env python
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Flyting.settings")

# Import django to manipulate databases
import django
django.setup()

# Run commands from command line
def runCommand(cur_command):
    # List of commands with functions to run
    results = "Command not found"
    if cur_command == 'clearvotes':
        results = clearVotes()
    if cur_command == 'clearRebuttalVotes':
        results = clearRebuttalVotes()
    print(results)

# Functions
from Articles.models import Vote, Choice
from Soapbox.models import Rebuttal, RebuttalVote

def clearVotes():
    print("Clearing Votes...")
    if len(Vote.objects.all()) > 0:
        for vote in Vote.objects.all():
            vote.delete()
    if len(Choice.objects.all()) > 0:
        for choice in Choice.objects.all():
            choice.votes = 0
            choice.save()
    return "Cleared Votes"

def clearRebuttalVotes():
    print("Clearing Rebuttal Votes...")
    if len(RebuttalVote.objects.all()) > 0:
        for vote in RebuttalVote.objects.all():
            vote.delete()
        for rebuttal in Rebuttal.objects.all():
            rebuttal.points = 0
            rebuttal.save()
    return "Cleared Rebuttal Votes"

# End Functions



# Check if this file is running as main and execute commands
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cur_command = sys.argv[1]
        runCommand(cur_command)
    else:
        print("No Command...")
