import time
# hour 3600 seconds
# day 86400 seconds
# week 604800 seconds
# month (30.44 days) 2629743 seconds

def getepoch():
  return int(time.time())
def gethepoch():
  now = getepoch()
  hour = now - 3600
  return (now, hour)
def getdepoch():
  now = getepoch()
  day = now - 86400
  return (now, day)
def getwepoch():
  now = getepoch()
  week = now - 604800
  return (now, week)
epoch =  getepoch
last24hours =  getdepoch
lastweek =  getwepoch
onewk =  getwepoch
lastwk =  getwepoch

print(f"Current EPOCH: {epoch()}")
print(f"24hrs EPOCH: {last24hours()}")
print(f"one Wk EPOCH: {lastwk()}")
