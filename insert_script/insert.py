import os, cmd, re, mysql.connector, random, sys, paramiko, json, ast, html2text
from PIL import Image
from datetime import timedelta, datetime, date
 
 
def generating_thumbnail(rootdir):
    count = 0
    big = (448, 420)
    med = (300, 280)
    sma = (120, 98)
    print("Generating pictures... please wait!")
    for subdir, dirs, files in os.walk(rootdir):
        count = 0
        for file in files:
            myFile = os.path.join(subdir, file)
            if myFile.endswith('.jpg') or myFile.endswith('.JPG'):
                #print(myFile)
                image = Image.open(myFile)
                #print(image.format, image.size, image.mode)
                image.thumbnail(big)
                outfile = subdir + "/" + file.lower() + "b"
                image.save(outfile, "JPEG")
                image.thumbnail(med)
                outfile2 = subdir + "/" + file.lower() + "m"
                image.save(outfile2, "JPEG")
                image.thumbnail(sma)
                outfile3 = subdir + "/" + file.lower() + "s"
                image.save(outfile3, "JPEG")
                count +=1
    print("Pictures generated!")
 
 
def list_files(dir):                                                                                                  
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).__next__()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file in files:                                                                                        
                r.append(os.path.join(subdir, file))                                                                         
    return r
 
def main():
          #generating_thumbnail(rootdir)
          #sys.exit(0)
          fileCredentials = open('credentials.json', 'r').read()          
          credential = ast.literal_eval(fileCredentials)
          numberOfPictures = int(credential['number_of_pictures'])
          listingNumberOfDays = int(credential['expiration_days'])
          user_id = int(credential['user_id'])
          categories_id = int(credential['categories_id'])
          statesFile = 'states.json'
          rootdir = credential['localhost_location']
          pictureStatus = credential['picture_status']
          if pictureStatus == "True":
              generating_thumbnail(rootdir)
          elif pictureStatus == "False":
              print("No pictures will be generated!")
          todays_date = date.today()
          currentYear = str(todays_date.year) 
          currentMonth = '{:02d}'.format(int(todays_date.month))
          currentFolder = currentYear + "-" + str(currentMonth)
          try:
              mydb = mysql.connector.connect(
                                      host = credential['db_hostname'],
                                      user = credential['db_username'],
                                      password = credential['db_password'],
                                      database = credential['db_name'],
                                      port = int(credential['db_port'])
                                    )
          except mysql.connector.Error as err:
              print("Something went wrong: {}".format(err))
              sys.exit(16)
          ssh_client = paramiko.SSHClient()
          ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
          ssh_client.connect(hostname = credential['sftp_hostname'], username = credential['sftp_username'], password = credential['sftp_password'] , port = int(credential['sftp_port']) )
          sftp = ssh_client.open_sftp()
          imageRoot = credential['sftp_location'] + currentFolder + "/"
          items = list_files(rootdir)
          countFilesHtm = 0
          countFilesTxt = 0
          openJsonStates = open(statesFile)
          jsonStates = json.load(openJsonStates)
          for item in items:
              if item.endswith('htm'):
                  countFilesHtm +=1
                  allFile = open(item, 'r', encoding='utf-8').read()
                  h = html2text.HTML2Text()
                  h.ignore_links = True
                  content = h.handle(allFile)
                  start = 'DESCRIPTION:'
                  end = 'CATEGORY:'
                  title = os.path.dirname(item).replace(rootdir,"")
                  price = content.splitlines()[2][7:-5]
                  print(f"--> [Creating] - ItemNo: {countFilesHtm} - Item: {title} - Price: {price}")
                  description = content[content.find(start) + len(end):content.rfind(end)]
                  year = title[0:4]
                  make = title[5:].split()[0]
                  model = title[5:].split()[1]
                  data = random.choice(jsonStates)                   
                  state = data['state']
                  zipCode = str(data['zip'])
                  city = data['city']
                  data_added = str(datetime.today())
                  date_expires = str(datetime.today() + timedelta(listingNumberOfDays))
                  mycursor = mydb.cursor()                  
                  select = ("SELECT id FROM class_ads WHERE id = (SELECT MAX(id) FROM class_ads)")
                  mycursor.execute(select)
                  idArray = []
                  for row in mycursor:  # type: ignore
                      idArray = str(row)
                  myId = idArray[1:-2]
                  ids = int(myId)  # type: ignore
                  ids +=1 
                  sqlId = ids
                  #print(sqlId)
                  query = (" INSERT INTO class_ads (id, user_id, category_id, package_id, usr_pkg, date_added, date_expires, title, description, price, currency, country, region, city, zip, lat, lng,meta_description, meta_keywords, sold, rented, viewed, user_approved, active, pending, featured, highlited, priority, video, rating, language, unique_id, auction, make, motorcycle_make, make_rvs, make1, model, model1, bodystyle, year, mileage, transmission, fuel, doors, color, engine_size, horsepower, condition_vehicles, length, vehicle_features, rv_features) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                  data = (sqlId,user_id,categories_id,1,1, data_added[:-7], date_expires[:-7], title, description, price, '$', 'USA', state, city, zipCode,'','','','',0,0,0,1,1,0,0,0,0,"",0.0,'eng','', 0, make, '', '', '', model, '', '', '', year, '', '', '', '', '', '', 'Used', '', '', '')
                  mycursor.execute(query, data)
                  mydb.commit()                 
                  for i in range(1,numberOfPictures):
                      ts = str(datetime.timestamp(datetime.now()))
                      imageName = title.replace(" ","_") + "_"  + ts.replace(".","_") + ".jpg"
                      imagePath = imageRoot + imageName
                      myPics = str(os.path.dirname(item) + "/" +  str(i) + ".jpg")
                      if os.path.isfile(myPics):
                          #print(f"FTP: {imagePath}")
                          #print(f"Localhost: {myPics}")
                          print("Creating & Uploading: Normal Images")
                          try:
                              sftp.put(myPics, imagePath, callback=None, confirm=True)  
                          except:
                              sftp.put(myPics[:-3]+ "JPG", imagePath, callback=None, confirm=True)                          
                          print("Creating & Uploading: bigThmb Images")
                          imagePath = imageRoot + "/bigThmb/" + imageName
                          a = str(myPics + "b")
                          sftp.put(a, imagePath, callback=None, confirm=True)                          
                          print("Creating & Uploading: medThmb Images")
                          imagePath = imageRoot + "/medThmb/" + imageName
                          sftp.put(str(myPics + "m"), imagePath, callback=None, confirm=True)
                          print("Creating & Uploading: thmb Images")
                          imagePath = imageRoot + "/thmb/" + imageName
                          sftp.put(str(myPics + "s"), imagePath, callback=None, confirm=True)
                          select = ("SELECT id FROM class_ads_pictures WHERE id = (SELECT MAX(id) FROM class_ads_pictures)")
                          mycursor.execute(select)
                          idPicArray = []
                          for row in mycursor:  # type: ignore
                              idPicArray = str(row)
                          myId = idPicArray[1:-2]
                          ids = int(myId)  # type: ignore
                          ids +=1
                          sqlIdPic = ids
                          #print(sqlIdPic)
                          queryImg = ("INSERT INTO class_ads_pictures (id, ad_id, picture, folder, order_no) VALUES (%s,%s,%s,%s,%s)")
                          data = (sqlIdPic,sqlId,imageName,str(currentFolder),i)
                          mycursor.execute(queryImg, data)
                          mydb.commit()
                  print(f"--> [Done] - ItemNo: {countFilesHtm} - Item: {title} - Price: {price}")                  
                  #print(description)
                  #print(os.path.dirname(item))
              elif item.endswith('txt'):
                  countFilesTxt +=1
                  print(f"= File type: txt - Nr: {countFilesTxt}")                  
                  fline = open(item).readline().rstrip()                  
                  flinePrice = re.split(r'\s',fline)
                  price = "".join(flinePrice[-1:]).replace("$","").replace(",","")                  
                  title = os.path.dirname(item).replace(rootdir,"")
                  print(f"--> [Creating] - ItemNo: {countFilesHtm} - Item: {title} - Price: {price}")
                  year = title[0:4]
                  make = title[5:].split()[0]
                  model = title[5:].split()[1]                  
                  data = random.choice(jsonStates)                   
                  state = data['state']
                  zipCode = str(data['zip'])
                  city = data['city']
                  f1 = open(item, 'r').readlines()
                  description = "".join(f1[-4:])
                  data_added = str(datetime.today())
                  date_expires = str(datetime.today() + timedelta(listingNumberOfDays)) 
                  #print(type(description))
                  #print(description)
                  #plm = re.sub(r'^US \$','', last_lines)   
                  mycursor = mydb.cursor()                  
                  select = ("SELECT id FROM class_ads WHERE id = (SELECT MAX(id) FROM class_ads)")
                  mycursor.execute(select)
                  idArray = []
                  for row in mycursor:  # type: ignore
                      idArray = str(row)
                  myId = idArray[1:-2]
                  ids = int(myId)  # type: ignore
                  ids +=1 
                  sqlId = ids
                  print(sqlId)
                  query = (" INSERT INTO class_ads (id, user_id, category_id, package_id, usr_pkg, date_added, date_expires, title, description, price, currency, country, region, city, zip, lat, lng,meta_description, meta_keywords, sold, rented, viewed, user_approved, active, pending, featured, highlited, priority, video, rating, language, unique_id, auction, make, motorcycle_make, make_rvs, make1, model, model1, bodystyle, year, mileage, transmission, fuel, doors, color, engine_size, horsepower, condition_vehicles, length, vehicle_features, rv_features) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                  data = (sqlId,user_id,categories_id,1,1, data_added[:-7], date_expires[:-7], title, description, price, '$', 'USA', state, city, zipCode,'','','','',0,0,0,1,1,0,0,0,0,"",0.0,'eng','', 0, make, '', '', '', model, '', '', '', year, '', '', '', '', '', '', 'Used', '', '', '')
                  mycursor.execute(query, data)
                  mydb.commit()                 
                  for i in range(1,numberOfPictures):
                      ts = str(datetime.timestamp(datetime.now()))
                      imageName = title.replace(" ","_") + "_"  + ts.replace(".","_") + ".jpg"
                      imagePath = imageRoot + imageName
                      myPics = str(os.path.dirname(item) + "/" +  str(i) + ".jpg")
                      if os.path.isfile(myPics):
                          print(f"FTP: {imagePath}")
                          print(f"Localhost: {myPics}")
                          print("Creating & Uploading: Normal Images")
                          try:
                              sftp.put(myPics, imagePath, callback=None, confirm=True)  
                          except:
                              sftp.put(myPics[:-3]+ "JPG", imagePath, callback=None, confirm=True)                          
                          print("Creating & Uploading: bigThmb Images")
                          imagePath = imageRoot + "/bigThmb/" + imageName
                          a = str(myPics + "b")
                          sftp.put(a, imagePath, callback=None, confirm=True)                          
                          print("Creating & Uploading: medThmb Images")
                          imagePath = imageRoot + "/medThmb/" + imageName
                          sftp.put(str(myPics + "m"), imagePath, callback=None, confirm=True)
                          print("Creating & Uploading: thmb Images")
                          imagePath = imageRoot + "/thmb/" + imageName
                          sftp.put(str(myPics + "s"), imagePath, callback=None, confirm=True)
                          select = ("SELECT id FROM class_ads_pictures WHERE id = (SELECT MAX(id) FROM class_ads_pictures)")
                          mycursor.execute(select)
                          idPicArray = []
                          for row in mycursor:  # type: ignore
                              idPicArray = str(row)
                          myId = idPicArray[1:-2]
                          ids = int(myId)  # type: ignore
                          ids +=1
                          sqlIdPic = ids
                          queryImg = ("INSERT INTO class_ads_pictures (id, ad_id, picture, folder, order_no) VALUES (%s,%s,%s,%s,%s)")
                          data = (sqlIdPic,sqlId,imageName,str(currentFolder),i)
                          mycursor.execute(queryImg, data)
                          mydb.commit()
                  print(f"--> [Done] - ItemNo: {countFilesTxt} - Item: {title} - Price: {price}")
 
          sftp.close()
          ssh_client.close()
          print(f"--> [SUCCESS] Total Listings added: {countFilesHtm + countFilesTxt}")
if __name__ == '__main__':
    main()