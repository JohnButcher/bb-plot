import csv,sys,datetime
now = datetime.datetime.now().isoformat()
with open(sys.argv[1],'rb') as speedcsv:
     # Server ID,Sponsor,Server Name,Timestamp,Distance,Ping,Download,Upload,Share,IP Address
     # ...we only need Timestamp,Ping,Download,Upload
     speedreader = csv.reader(speedcsv,delimiter=',',quotechar='"')
     n = 0
     for r in speedreader:
         if r[0].upper().startswith('SERVER'): continue
         if len(r[3]) < 19: timestamp = now
         else: timestamp = r[3]
         ping = float(r[5])
         download = float(r[6])
         upload = float(r[7])
         if download > 1024: download = download/1048576
         if upload > 1024: upload = upload/1048576
         try:
            print ("%s,%.1f,%.2f,%.2f") % (timestamp,ping,download,upload)
         except:
            sys.stderr.write(str(r)+"\n")
            sys.stderr.write(str(sys.exc_info()[0]))
            sys.stderr.write("\n")
