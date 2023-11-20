from googleapiclient.discovery import build #import the googleapiclient for the api key to request

import pymongo #Is used to connect, insert and migrate the Mongo DB elements

import pandas as pd

import mysql.connector #It is used to connect the mysql workbench to create, insert and selecting the records

import re  #Regular expression is used to seprate the digits from the string

import streamlit as st #It is used to create the streamlit application
from streamlit_option_menu import option_menu
st.set_page_config(layout='wide',page_title="Youtube_Dataharvesting")

#Connecting to the mysql workbench
connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
mycursor=connect.cursor()

#It is used to connect the mongodb and collection
url="mongodb://localhost:27017"
db_connect=pymongo.MongoClient(url)
db="Youtube"
connect=db_connect[db]
col="Youtube_Datas"
col_c=connect[col]

#It is used to connect thee googleapiclient by using api key
youtube = build("youtube", "v3", developerKey="AIzaSyDPxJY_yFjNX0aN0s-MPwa9ozOjAFL5j5M")

st.markdown("<h2><FONT COLOR='red'>Youtube Data Harvesting</h2>",unsafe_allow_html=True)
select = option_menu(None,["About","Task to Do"],orientation="horizontal")

if select=="About":
    st.markdown("<h4><FONT COLOR='#D2042D'>Intoduction</h4>",unsafe_allow_html=True)
    st.write("""YouTube Data Harvesting and Warehousing is a project aimed 
             at developing a user-friendly Streamlit application that leverages 
             the power of the Google API to extract valuable information from 
             YouTube channels. The extracted data is then stored in a MongoDB database, 
             subsequently migrated to a SQL data warehouse, and made accessible for analysis and exploration within the Streamlit app.""")
    st.markdown("<h4><FONT COLOR='#D2042D'>Storing data in MongoDB</h4>",unsafe_allow_html=True)
    st.write("""The retrieved data is stored in a MongoDB database based on 
             user authorization. If the data already exists in the database, 
             it can be overwritten with user consent. This storage process ensures 
             efficient data management and preservation, allowing for seamless handling of the collected data.
             """)
    st.markdown("<h4><FONT COLOR='#D2042D'>Migrating data from Mongo DB to MYSQL</h4>",unsafe_allow_html=True)
    st.write("""The application allows users to migrate data from MongoDB 
             to a SQL data warehouse. Users can choose which channel's data 
             to migrate. To ensure compatibility with a structured format, 
             the data is cleansed using the powerful pandas library. Following data cleaning, the information is segregated into separate tables, including channels, playlists, videos, and comments, utilizing SQL queries.
             """)
        
if select=="Task to Do":  
    st.markdown("<h4><FONT COLOR='#D2042D'>Getting Channel Id</h4>",unsafe_allow_html=True)
    st.write("""Here, you can give the channel Id as an input that should be in the format of
             Example: (UC4FBxFkPYBi-xxAgUb8ekhA UCDidq1Sr-hcobhcuVfHFwOA). So in this format you 
             have to enter the channel id as input.""")
    st.write(""" It can helps you to take the the channel id from the youtube""")
    st.write("""URL - https://www.youtube.com/watch?v=3mrKjzrIiq4""")

    #Getting the channel id details
    channel_id=st.text_input("Enter the channel id: ").split()
    st.markdown("<h4><FONT COLOR='#D2042D'>Queries Details:</h6>",unsafe_allow_html=True)
    st.write("Query1:  What are the names of all the videos and their corresponding channels?")
    st.write("Query2:  Which channels have the most number of videos, and how many videos do they have?")
    st.write("Query3:  What are the top 10 most viewed videos and their respective channels?")
    st.write("Query4:  How many comments were made on each video, and what are their corresponding video names?")
    st.write("Query5:  Which videos have the highest number of likes, and what are their corresponding channel names?")
    st.write("Query6:  What is the total number of likes and dislikes for each video, and what are their corresponding video names?")
    st.write("Query7:  What is the total number of views for each channel, and what are their corresponding channel names?")
    st.write("Query8:  What are the names of all the channels that have published videos in the year 2022?")
    st.write("Query9:  What is the average duration of all videos in each channel, and what are their corresponding channel names?")
    st.write("Query10:  Which videos have the highest number of comments, and what are their corresponding channel names?")
    l=["Query1","Query2","Query3","Query4","Query5","Query6","Query7","Query8","Query9","Query10"]
    r=st.multiselect("Select the query to display:",l)
    if st.button("Submit"):
        
        #it will return the playlist details
        def playlist_details(channel_id):
            channel_id=channel_id
            request = youtube.playlists().list(part="snippet,contentDetails",channelId=channel_id,
                    maxResults=50
                )
            response = request.execute()
            playlist_count=response['pageInfo']['totalResults']
            play_list={}
            playlist={}
            if(playlist_count<=50):
                for i in range(playlist_count):
                    playid=response['items'][i]['id']
                    playname=response['items'][i]['snippet']['title']
                    playpublished=response['items'][i]['snippet']['publishedAt']
                    playvideocount=response['items'][i]['contentDetails']['itemCount']
                    playlist={"Playlist Id":playid,"Playlist_Name":playname,"Playlist_Published":playpublished,"Playlist_VideoCount":playvideocount}
                    play_list[str(i+1)]=playlist
            else:
                w=length(playlist_count)
                q=0
                for i in range(len(w)):
                    if(i==0):
                        request = youtube.playlists().list(part="snippet,contentDetails",
                                                        channelId=channel_id,maxResults=50)
                        response = request.execute()
                        nextpage=response['nextPageToken']
                        for i in range(50):
                            playid=response['items'][i]['id']
                            playname=response['items'][i]['snippet']['title']
                            playpublished=response['items'][i]['snippet']['publishedAt']
                            playvideocount=response['items'][i]['contentDetails']['itemCount']
                            playlist={"Playlist Id":playid,"Playlist_Name":playname,"Playlist_Published":playpublished,"Playlist_VideoCount":playvideocount}
                            play_list[str(q+1)]=playlist
                            q+=1
        
                    else:
                        request = youtube.playlists().list(part="snippet,contentDetails",
                                                        channelId=channel_id,pageToken=nextpage,maxResults=50)
                        response = request.execute()
                        if(i==len(w)-1):
                            for i in range(w[i]):
                                playid=response['items'][i]['id']
                                playname=response['items'][i]['snippet']['title']
                                playpublished=response['items'][i]['snippet']['publishedAt']
                                playvideocount=response['items'][i]['contentDetails']['itemCount']
                                playlist={"Playlist Id":playid,"Playlist_Name":playname,"Playlist_Published":playpublished,"Playlist_VideoCount":playvideocount}
                                play_list[str(q+1)]=playlist
                                q+=1
        
                        else:
                            nextpage=response['nextPageToken'] 
                            for i in range(50):
                                playid=response['items'][i]['id']
                                playname=response['items'][i]['snippet']['title']
                                playpublished=response['items'][i]['snippet']['publishedAt']
                                playvideocount=response['items'][i]['contentDetails']['itemCount']
                                playlist={"Playlist Id":playid,"Playlist_Name":playname,"Playlist_Published":playpublished,"Playlist_VideoCount":playvideocount}
                                play_list[str(q+1)]=playlist
                                q+=1
            return play_list
        
        #it will divide the given number into 50 and return
        
        def length(count):
            a=int(count)
            w=[]
            while(a>50):
                if(a>50):
                    w.append(50)
                    a=a-50
            w.append(a)
            return w
        
        #it will return the videoids
        def videoids(playlistforallvideo):
            playlistforallvideo=playlistforallvideo
            request = youtube.playlistItems().list(part="contentDetails",
                                                       playlistId=playlistforallvideo,maxResults=50)
            response = request.execute()
            count=int(response['pageInfo']['totalResults'])
            videoid=[]
            if(count<=50):
                request = youtube.playlistItems().list(part="contentDetails",
                                                       playlistId=playlistforallvideo,maxResults=50)
                response = request.execute()
                for i in range(count):
                    ids=response['items'][i]['contentDetails']['videoId']
                    videoid.append(ids)
            else:
                l=length(count)
                for i in range(len(l)):
                    if(i==0):
                        request = youtube.playlistItems().list(part="contentDetails",
                                                       playlistId=playlistforallvideo,maxResults=50)
                        response = request.execute()
                        nextpage=response['nextPageToken']
                        for i in range(50):
                            ids=response['items'][i]['contentDetails']['videoId']
                            videoid.append(ids)
                    else:
                        if(i==len(l)-1):
                            request = youtube.playlistItems().list(part="contentDetails",
                                                       playlistId=playlistforallvideo,pageToken=nextpage,maxResults=50)
                            response = request.execute()
                            for i in range(l[i]):
                                ids=response['items'][i]['contentDetails']['videoId']
                                videoid.append(ids)
                        else:
                            request = youtube.playlistItems().list(part="contentDetails",
                                                       playlistId=playlistforallvideo,pageToken=nextpage,maxResults=50)
                            response = request.execute()
                            nextpage=response['nextPageToken']
                            for i in range(50):
                                ids=response['items'][i]['contentDetails']['videoId']
                                videoid.append(ids)
            return videoid
        
        #it will return the video details
        def videos_details_of_channel(videoid):
            video_details={}
            video={}
            videoid=videoid
            if(len(videoid)<=50):
                request = youtube.videos().list(part="snippet,contentDetails,statistics",id=videoid)
                response = request.execute()
                for i in range(len(videoid)):
                    vid=response['items'][i]['id']
                    vdate=response['items'][i]['snippet']['publishedAt']
                    vname=response['items'][i]['snippet']['title']
                    vdes=response['items'][i]['snippet']['description']
                    vtime=response['items'][i]['contentDetails']['duration']
                    vcap=response['items'][i]['contentDetails']['caption']
                    views=int(response['items'][i]['statistics']['viewCount'])
                    if("likeCount" in response['items'][i]['statistics'].keys()):
                        likes=int(response['items'][i]['statistics']['likeCount'])
                    else:
                        likes=0
                    if("commentCount" in response['items'][i]['statistics'].keys()):
                        vcom=int(response['items'][i]['statistics']['commentCount'])
                    else:
                        vcom=0
                    video_details={"Video_Id":vid,"Video_Name":vname,"Video_Description":vdes,"Video_PublishedAt":vdate,"Video_Duration":vtime,
                                  "Video_Caption_Status":vcap,"Video_Views_Count":views,"Video_Likes_count":likes,"Video_Comment_Count":vcom
                                  }
                    video[str(i+1)]=video_details
                    
                        
            else:
                q=0
                a=0
                vi=[]
                l=length(len(videoid))
                for i in range(len(l)):
                    vi=videoid[q:l[i]+q]
                    q=l[i]+q
                    request = youtube.videos().list(part="snippet,contentDetails,statistics",id=vi)
                    response = request.execute()
                    for i in range(len(vi)):
                        vid=response['items'][i]['id']
                        vdate=response['items'][i]['snippet']['publishedAt']
                        vname=response['items'][i]['snippet']['title']
                        vdes=response['items'][i]['snippet']['description']
                        vtime=response['items'][i]['contentDetails']['duration']
                        vcap=response['items'][i]['contentDetails']['caption']
                        views=int(response['items'][i]['statistics']['viewCount'])
                        if("likeCount" in response['items'][i]['statistics'].keys()):
                            likes=int(response['items'][i]['statistics']['likeCount'])
                        else:
                            likes=0
                        if("commentCount" in response['items'][i]['statistics'].keys()):
                            vcom=int(response['items'][i]['statistics']['commentCount'])
                        else:
                            vcom=0
                        video_details={"Video_Id":vid,"Video_Name":vname,"Video_Description":vdes,"Video_PublishedAt":vdate,"Video_Duration":vtime,
                                      "Video_Caption_Status":vcap,"Video_Views_Count":views,"Video_Likes_count":likes,"Video_Comment_Count":vcom
                                      }
                        video[str(a+1)]=video_details
                        a+=1
            return video
                
        #It will extract the comments details
        def comments(videoids):
            comments={}
            com={}
            a=0
            for i in range(len(videoids)):
                try:
                    request = youtube.commentThreads().list(
                    part="snippet,replies",videoId=videoids[i],maxResults=10)
                    response = request.execute()
                    for j in range(10):
                        cid=response['items'][j]['id']
                        vid=response['items'][j]['snippet']['videoId']
                        text=response['items'][j]['snippet']['topLevelComment']['snippet']['textOriginal']
                        author=response['items'][j]['snippet']['topLevelComment']['snippet']['authorDisplayName']
                        date=response['items'][j]['snippet']['topLevelComment']['snippet']['publishedAt']
                        date=date[:10]
                        com={"Comments_Id":cid,"Comments_Text":text,"Comment_Author":author,"Video_Id":vid,"Comments_PublisheddAt":date}
                        comments[str(a+1)]=com
                        a+=1
                except:
                    pass
            return comments
    
        #it will return the channel details
        def channel_details(channel_id):
            channel_id
            request = youtube.channels().list(part="snippet,contentDetails,statistics",id=channel_id)
            response = request.execute()
            channel={}
            cid=response['items'][0]['id']
            cname=response['items'][0]['snippet']['title']
            cdes=response['items'][0]['snippet']['description']
            cdate=response['items'][0]['snippet']['publishedAt']
            cuploads=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            cview=int(response['items'][0]['statistics']['viewCount'])
            csub=int(response['items'][0]['statistics']['subscriberCount'])
            videocount=int(response['items'][0]['statistics']['videoCount'])
            channel={"Channel_Id":cid,"Channel_Name":cname,"Channel_Description":cdes,"Channel_PublishedAt":cdate,"Channel_Uploads":cuploads,
                    "Channel_Views":cview,"Channel_Subcriber_Count":csub,"Channel_Video_Count":videocount}
            return channel,cuploads
        
        def channel_ids():
            channel_id=[]
            a=list(col_c.find({}))
            for i in range(len(a)):
                channel_id.append(a[i]["Channel"]["Channel_Id"])
            channel_id=list(set(channel_id))
            return channel_id
        #It is used to create the tables in mysql
        def creating_table():
            try:
                connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
                mycursor=connect.cursor()
                mycursor.execute("use youtube")
                mycursor.execute("CREATE TABLE channel1 (Channel_Id VARCHAR(50) PRIMARY KEY,Channel_Name VARCHAR(1000),Channel_PublishedAt DATE,Channel_Views INT(255),Channel_Subscriber_Count INT(255),Channel_Video_Count INT(255))")
                mycursor.execute("CREATE TABLE video1 (Video_Id VARCHAR(50) PRIMARY KEY,Video_Name VARCHAR(1000),Video_PublishedAt VARCHAR(50),Video_Views INT(255),Video_Duration INT(255),Video_Likes_Count INT(255),Video_Comment_Count INT(255),Channel_id VARCHAR(50),FOREIGN KEY (Channel_id) REFERENCES channel1(Channel_Id))")
                mycursor.execute("CREATE TABLE comment1 (Comment_Id VARCHAR(50) PRIMARY KEY,Comment_Text VARCHAR(1000),Comment_Author VARCHAR(50),Comments_PublishedAt VARCHAR(30),Video_id VARCHAR(50),FOREIGN KEY (Video_id) REFERENCES video1(Video_Id))")
            except:
               pass
            
            
        def adding_record():
                connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
                mycursor=connect.cursor()
                mycursor.execute("use youtube")
                datas=list(col_c.find({}))
                for i in range(len(datas)):
                    val=[]
                    cid=datas[i]["Channel"]["Channel_Id"]
                    name=datas[i]["Channel"]["Channel_Name"]
                    date=datas[i]["Channel"]["Channel_PublishedAt"]
                    date=date[:10]
                    views=datas[i]["Channel"]["Channel_Views"]
                    sub=datas[i]["Channel"]["Channel_Subcriber_Count"]
                    video=datas[i]["Channel"]["Channel_Video_Count"]
                    val=[[cid,name,date,views,sub,video]]
                    query="insert into channel1 values(%s,%s,%s,%s,%s,%s)"
                    try:
                        mycursor.executemany(query,val)
                    except:
                        continue 
                    for j in range(len(datas[i]['Videos'])):
                        val1=[]
                        vid=datas[i]['Videos'][str(j+1)]['Video_Id']
                        vname=datas[i]['Videos'][str(j+1)]['Video_Name']
                        date=datas[i]['Videos'][str(j+1)]['Video_PublishedAt']
                        date=date[:10]
                        strin=datas[i]['Videos'][str(j+1)]['Video_Duration']
                        str1=re.findall('\d+',strin)
                        sec=0
                        if(len(str1)==3):
                            sec=int(str1[0])*3600
                            sec=(int(str1[1])*60)+sec
                            sec=(int(str1[2]))+sec
                        elif(len(str1)==2):
                            sec=(int(str1[0])*60)
                            sec=(int(str1[1]))+sec
                        else:
                            if('M' in strin):
                                sec=int(str1[0])*60
                            else:
                                sec=int(str1[0])
                        view=datas[i]['Videos'][str(j+1)]['Video_Views_Count']
                        likes=datas[i]['Videos'][str(j+1)]['Video_Likes_count']
                        comment=datas[i]['Videos'][str(j+1)]['Video_Comment_Count']
                        cid=datas[i]["Channel"]["Channel_Id"]
                        val1=[[vid,vname,date,view,sec,likes,comment,cid]]
                        query="insert into video1 values(%s,%s,%s,%s,%s,%s,%s,%s)"
                        mycursor.executemany(query,val1)
                    for k in range(len(datas[i]["Comments"])):
                        val2=[]
                        cid=datas[i]['Comments'][str(k+1)]['Comments_Id']
                        text=datas[i]['Comments'][str(k+1)]['Comments_Text']
                        aut=datas[i]['Comments'][str(k+1)]['Comment_Author']
                        vid=datas[i]['Comments'][str(k+1)]['Video_Id']
                        date=datas[i]['Comments'][str(k+1)]['Comments_PublisheddAt']
                        val2=[[cid,text,aut,date,vid]]
                        query="insert into comment1 values(%s,%s,%s,%s,%s)"
                        mycursor.executemany(query,val2)
            
        def execute_query(channel_id,r):
            for i in r:
                if(i=="Query1"):
                    channel=[]
                    video1=[]
                    connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
                    mycursor=connect.cursor()
                    mycursor.execute("use youtube")
                    st.markdown("<h6><FONT COLOR='#D2042D'>QUERY_1 RESULT:</h6>",unsafe_allow_html=True)
                    st.write("Displays video names and their corresponding channel names")
                    for i in range(len(channel_id)):
                        query=f"""select Channel_Name from channel1 where Channel_Id = '{channel_id[i]}'"""
                        mycursor.execute(query)
                        name=mycursor.fetchall()
                        query=f"""select Video_Name from video1 where Channel_id = '{channel_id[i]}'"""
                        mycursor.execute(query)
                        video=mycursor.fetchall()
                        channel.append(name)
                        video1.append(video)
                    for i in range(len(channel)):
                        df=pd.DataFrame(data=video1[i],columns=["Video Title"])
                        st.write("Channel Name: ",channel[i][0])
                        st.dataframe(df)
                if(i=="Query2"):
                    query="""select Channel_Name,Channel_Video_Count from channel1 order by Channel_Video_Count desc"""
                    connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
                    mycursor=connect.cursor()
                    mycursor.execute("use youtube")
                    mycursor.execute(query)
                    result=mycursor.fetchall()
                    df=pd.DataFrame(data=result,columns=["Channel_Name","Channel_Video_Count"])
                    st.markdown("<h6><FONT COLOR='#D2042D'>QUERY_2 RESULT:</h6>",unsafe_allow_html=True)
                    st.write("Displays channel name and their video counts")
                    st.dataframe(df)
                if(i=="Query3"):
                    cha=[]
                    count=[]
                    connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
                    mycursor=connect.cursor()
                    mycursor.execute("use youtube")
                    for i in range(len(channel_id)):
                        query=f"""select max(video1.Video_Views) as Maximum_Views,channel1.Channel_Name from video1 join channel1 where video1.Channel_id = '{channel_id[i]}' and channel1.Channel_Id = '{channel_id[i]}'"""
                        mycursor.execute(query)
                        vmax=mycursor.fetchall()
                        count.append(vmax[0][0])
                        cha.append(vmax[0][1])
                    
                    df=pd.DataFrame(data=(cha,count),index=["Channel_Name","Maximum_View_Count"])
                    st.markdown("<h6><FONT COLOR='#D2042D'>QUERY_3 RESULT:</h6>",unsafe_allow_html=True)
                    st.write("Displays the channel names and their maximum view counts on each channel")
                    st.dataframe(df)
                if(i=="Query4"):
                    query="""select Video_Name,Video_Comment_Count from video1"""
                    connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
                    mycursor=connect.cursor()
                    mycursor.execute("use youtube")
                    mycursor.execute(query)
                    result=mycursor.fetchall()
                    df=pd.DataFrame(data=result,columns=["Video_Name","Comments_Count"])
                    st.markdown("<h6><FONT COLOR='#D2042D'>QUERY_4 RESULT:</h6>",unsafe_allow_html=True)
                    st.write("Displays all the video names in the table and their comment count")
                    st.dataframe(df)
                if(i=="Query5"):
                    lmax=[]
                    name=[]
                    connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
                    mycursor=connect.cursor()
                    mycursor.execute("use youtube")
                    for i in range(len(channel_id)):
                        query=f"""select max(video1.Video_Likes_Count) as Maximum_Views,channel1.Channel_Name from video1 join channel1 where video1.Channel_id = '{channel_id[i]}' and channel1.Channel_Id = '{channel_id[i]}'"""
                        mycursor.execute(query)
                        details=mycursor.fetchall()
                        lmax.append(details[0][0])
                        name.append(details[0][1])
                    df=pd.DataFrame(data=(name,lmax),index=["Channel_Name","Likes_Count"])
                    st.markdown("<h6><FONT COLOR='#D2042D'>QUERY_5 RESULT:</h6>",unsafe_allow_html=True)
                    st.write("Displays the channel name and maximum likes count on each channel")
                    st.dataframe(df)
                if(i=="Query6"):
                    query="""select Video_Name,Video_Likes_Count from video1"""
                    connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
                    mycursor=connect.cursor()
                    mycursor.execute("use youtube")
                    mycursor.execute(query)
                    result=mycursor.fetchall()
                    df=pd.DataFrame(data=result,columns=["Video_Name","Video_Likes_Count"])
                    st.markdown("<h6><FONT COLOR='#D2042D'>QUERY_6 RESULT:</h6>",unsafe_allow_html=True)
                    st.write("Displays the video names and their likes count")
                    st.dataframe(df)
                if(i=="Query7"):
                    query="""select Channel_Name,Channel_Views from channel1"""
                    connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
                    mycursor=connect.cursor()
                    mycursor.execute("use youtube")
                    mycursor.execute(query)
                    result=mycursor.fetchall()
                    df=pd.DataFrame(data=result,columns=["Channel_Name","Channel_Total_Views"])
                    st.markdown("<h6><FONT COLOR='#D2042D'>QUERY_7 RESULT:</h6>",unsafe_allow_html=True)
                    st.write("Displays the channel name and total views for each channel")
                    st.dataframe(df)
                if(i=="Query8"):
                    query="""select channel1.Channel_Name from channel1 join video1 where video1.Video_PublishedAt between "2022-01-01" and "2023-01-01";"""        
                    connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
                    mycursor=connect.cursor()
                    mycursor.execute("use youtube")
                    mycursor.execute(query)
                    result=mycursor.fetchall()
                    result=list(set(result))
                    df=pd.DataFrame(data=result,columns=["Channel_Name"])
                    st.markdown("<h6><FONT COLOR='#D2042D'>QUERY_8 RESULT:</h6>",unsafe_allow_html=True)
                    st.write("Displays the channel name in which videos are published at the year of 2022")
                    st.dataframe(df)
                if(i=="Query9"):
                    avgtime=[]
                    name=[]
                    connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
                    mycursor=connect.cursor()
                    mycursor.execute("use youtube")
                    for i in range(len(channel_id)):
                        query=f"""select avg(video1.Video_Duration),channel1.Channel_Name from video1 join channel1 where video1.Channel_id = '{channel_id[i]}' and channel1.Channel_Id = '{channel_id[i]}'"""
                        mycursor.execute(query)
                        details=mycursor.fetchall()
                        avgtime.append(details[0][0])
                        name.append(details[0][1])
                    df=pd.DataFrame(data=(name,avgtime),index=['Channel_Name','Average_Duration(In seconds)'])
                    st.markdown("<h6><FONT COLOR='#D2042D'>QUERY_9 RESULT:</h6>",unsafe_allow_html=True)
                    st.write("Displays the Channel name and their average duration of all videos in eeach channel in seconds")
                    st.dataframe(df)
                if(i=="Query10"):
                    name=[]
                    maxcomment=[]
                    connect= mysql.connector.connect(host="localhost",user="root",password="Mouleesh@009",autocommit=True)
                    mycursor=connect.cursor()
                    mycursor.execute("use youtube")
                    for i in range(len(channel_id)):
                        query=f"""select max(video1.Video_Comment_Count),channel1.Channel_Name from video1 join channel1 where video1.Channel_id = '{channel_id[i]}' and channel1.Channel_Id = '{channel_id[i]}';"""
                        mycursor.execute(query)
                        details=mycursor.fetchall()
                        maxcomment.append(details[0][0])
                        name.append(details[0][1])
                    df=pd.DataFrame(data=(name,maxcomment),index=["Channel_Name","Comment_Max_Count"])
                    st.markdown("<h6><FONT COLOR='#D2042D'>QUERY_10 RESULT:</h6>",unsafe_allow_html=True)
                    st.write("Displays the channel name and the maximum comment count on each channel")
                    st.dataframe(df)
        #it is used to call the functions and insert the values in mongodb
        def main(channel):
            for i in range(len(channel_id)):
                channel,uploads=channel_details(channel_id[i])
                playlist=playlist_details(channel_id[i])
                videoid=videoids(uploads)
                comment=comments(videoid)
                videos=videos_details_of_channel(videoid)
                details={"Channel":channel,"PlayList":playlist,"Videos":videos,"Comments":comment}
                col_c.insert_one(details)
            return True
        
        #It is a function used to calll the orther functions
        def main_sql():
            creating_table()
            adding_record()
            return True
        
        
        a=main(channel_id)
        st.markdown("<h6><FONT COLOR='#32CD32'>Datas are successfully uploaded in Mongo DB</h6>",unsafe_allow_html=True)
        a=main_sql()
        st.markdown("<h6><FONT COLOR='#32CD32'>Datas are successfully updated in MYSQL from Mongo DB</h6>",unsafe_allow_html=True)
        channel_Id=channel_ids()
        execute_query(channel_Id,r)
        st.markdown("<h2><FONT COLOR='#D2042D'>Thank You! !</h6>",unsafe_allow_html=True)

                