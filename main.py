# fogreport main script
# https://github.com/avlg/fogreport

import mysql.connector
from mysql.connector import errorcode
import numpy as np
import matplotlib.pyplot as plt
import configparser
import sys

cfg = configparser.ConfigParser()
cfg.read('config-my.ini')
fog_db_user = cfg.get('database', 'user')
fog_db_password = cfg.get('database', 'password')
fog_db_host = cfg.get('database', 'host')
fog_db_name = cfg.get('database', 'database')

config = {
  'user': fog_db_user,
  'password': fog_db_password,
  'host': fog_db_host,
  'database': fog_db_name,
  'raise_on_warnings': True,
}
print ('CONFIG:\n  Host {}\n  Database {}\n  User {}\n  Password ***\n'\
       .format(config['host'], config['database'], config['user']))

print('Connecting...')
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = ("SELECT hostName, hostDesc, hostIP, hostImage, "
             "iMbman, iMbproductname, iMbversion, iMbserial, iMem, "
             "iCpuversion, iHdmodel, iHdserial, "
             "hostUseAD, hostADDomain, hostADOU, hostADUser, "
             "hostADPass, hostADPassLegacy, hostProductKey "
             "FROM hosts LEFT JOIN inventory ON hostID=iHostID")

    cursor.execute(query)

    IntelMBCount = 0
    AsusMBCount = 0
    OtherMBCount = 0
    ram_sizes = []

    for (hostName, hostDesc, hostIP, hostImage, \
        iMbman, iMbproductname, iMbversion, iMbserial, iMem, \
        iCpuversion, iHdmodel, iHdserial, \
        hostUseAD, hostADDomain, hostADOU, hostADUser, \
        hostADPass, hostADPassLegacy, hostProductKey \
        ) in cursor:

        if iMbman == None:
            OtherMBCount += 1
        elif iMbman.upper()=='INTEL CORPORATION':
            IntelMBCount += 1
        elif iMbman.upper()=='ASUSTEK COMPUTER INC.':
            AsusMBCount += 1
        else:
            OtherMBCount += 1

        if iMem != None:
            mem = iMem.replace('MemTotal: ','')
            mem = mem.replace(' kB','')
            memGb = round(int(mem)/(1024*1024),1)
        else:
            memGb = 0.0

        ram_sizes.append(memGb)
                
        print("HOST {} ({}) IP={} Image={}\n"
            "  MB {} {} ver.{} serial {}\n"
            "  RAM {}Gb, CPU {}, HDD {} {}\n"
            "  AD: {} {} {} {} {} {} {}".format(
        hostName, hostDesc, hostIP, hostImage, \
        iMbman, iMbproductname, iMbversion, iMbserial, memGb, \
        iCpuversion, iHdmodel, iHdserial, \
        hostUseAD, hostADDomain, hostADOU, hostADUser, \
        hostADPass, hostADPassLegacy, hostProductKey \
        ))

    cursor.close()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
    sys.exit()
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
    sys.exit()
  else:
    print(err)
    sys.exit()
else:
    cnx.close()
    sys.exit()
##finally:
##    sys.exit()

print('Asus:{}, Intel:{}, Other:{}'.format(
    AsusMBCount, IntelMBCount, OtherMBCount))
print(ram_sizes)

mb_data = (AsusMBCount, IntelMBCount, OtherMBCount)
# http://matplotlib.org/users/pyplot_tutorial.html
#plt.plot(x_data, 'cd')
#plt.plot(AsusMBCount, IntelMBCount, OtherMBCount, 'cd')
#sns.barplot(x="MB manufacturers", y="host count", hue="class", data=x_data);
##plt.xlabel('MB manufacturers')
##plt.ylabel('host count')

#https://matplotlib.org/examples/api/barchart_demo.html

N = 3
ind = np.arange(N)  # the x locations for the groups
width = 0.1       # the width of the bars

fig, ax = plt.subplots()
rects = ax.bar(left=ind, height=mb_data, width=width, color='g')

# add some text for labels, title and axes ticks
ax.set_ylabel('Hosts count')
ax.set_title('CPUs and Motherboards')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('Asus', 'Intel', 'Other'))

#ax.legend((rects[0]), ('MB manufacturers'))

#Attach a text label above each bar displaying its height
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.0*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects)

#plt.savefig('plot.png')
plt.show()
print('FINISH')
