
import sys
from Wrapper_API import Wrapper_API

server = "http://192.168.128.106:6080"
usrPass = "admin:WWTwwt1!"


ourRequest = Wrapper_API(server, usrPass)

# Generate daily report for incoming traffic 
ourRequest.GetDaily("/mail_incoming_traffic_summary?1d")

print("Successfully retrieve Daily report")

# Generate summary for incomfing traffic
ourRequest.GetIncomSum("/mail_incoming_traffic_summary/help")

print("Successfully generate incoming summary")

# Generate summary for incomfing traffic that affected by virus
ourRequest.GetVirus("/mail_incoming_traffic_summary/detected_virus/help")

print("Successfully retrieve emails affected by virus")
