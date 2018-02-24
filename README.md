# BSESTOCK-Zerodha
***Description:***

  This is python web app written using cherrypy and db as redis.

***1.*** Where downloaderbhavfile.py uses schedular which is more like a celery that runs every 30 minutes and stores the data in 
    Redis DB.
    
***2.*** Along with this it is mainly a CherryPy Web App:  
          Which shows the Top 10 stock of BSE and All stocks of BSE.

***Installation:*** 
    Use the "requirements.txt" with pip: 'pip install -r requirements.txt'

***Pre-Installation:*** 
    Install Redis DB from the official web page: https://redis.io/download

This project is on Demo at: http://13.126.120.225:5000

/* To test downloaderbhavfile.py, comment end of the code in downloaderbhavfile.py mentioned below part in :
```       
          schedule.every(30).minutes.do(getBhav)
          while 1:
              schedule.run_pending()
              time.sleep(1)
```              
   And Uncomment the :
      "#getBhav()"
*/

Author:
***Jeevan - G1***



