#!/usr/bin/env python
import sys
from marsmission.twmission import TWMission

twm = TWMission(sys.stdin)
print "waiting for input"
twm.execute()
print twm.report()
