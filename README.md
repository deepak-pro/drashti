# Drashti

### A network monitoring tool

![demo](https://raw.githubusercontent.com/deepak-pro/drashti/main/assets/Screenshot%202021-02-24%20at%2010.09.49%20AM.png?token=AEZOEVGTBE5K35HCXFZAWSTAYNKEO)

### Abstract

The purpose of this application is to collect useful information from various parts of the network so that the network can be managed and controlled using the collected information.The goal of this application is to monitor every device on the network and show complete information in real time to the administrator. This application also deals with fault monitoring in the network.

### Importance

Faulty network devices impact network performance. This can be eliminated through early detection and this is why continuous monitoring of network and related devices is essential. In effective network monitoring, the first step is to identify the devices and the related performance metrics to be monitored. The second step is enable frequent monitoring on device like servers, routers and switches because they perform business critical tasks but at the same time have specific parameters that can be selectively monitored.

### Key features

- Monitoring the essentials
- Listing entire Infrastructure
- Keep track of Outages
- Helps to Fix issue
- Provide Real Time information
- Visualization
- Manage growing network

### Implementation

1. Active Scan - This feature allows the user to identify all the network devices with easy of clicking on a button. This feature uses ping functionality provided by the operating system to send ICMP packets to all the nodes and receive response. Those devices who reply to the ICMP message are listed to be used on a single page with a button to add a device to the list of known devices calles nodes list.

   ![activeScan](https://raw.githubusercontent.com/deepak-pro/drashti/main/assets/Screenshot%202021-02-24%20at%209.42.55%20AM.png?token=AEZOEVEYVCH2DSPUFNCN2YDAYNI3Q)

2. Nodes - Nodes This gives list of all the devices that are added after scanning of network with all the following information

   - Status (Active or Inactive)

   - Name

   - IP address

   - Description

   - Round Trip time(in ms)

     With a button to easily add any node to the server list and another button to delete the node from the list of known devices.

     ![Nodes](https://raw.githubusercontent.com/deepak-pro/drashti/main/assets/Screenshot%202021-02-24%20at%209.49.44%20AM.png?token=AEZOEVECA72YZUSSEYQGR63AYNJF4)

3. Servers - This is the list of nodes that are explicitly marked as servers for actively monitoring. If any of the servers is unable to reach the network or is experiencing a downtime. The administrator of the network will be immediately notified via email.

   ![server](https://raw.githubusercontent.com/deepak-pro/drashti/main/assets/Screenshot%202021-02-24%20at%209.53.02%20AM.png?token=AEZOEVHWNOJHO6KITGGMOSLAYNJMA)

4. Notification - This feature allows the admin to add email that should be notified for important alerts. It provides you the list and a field to add new email. Also there is test notification button which sends a test email to all the emails listed.

   ![notification](https://raw.githubusercontent.com/deepak-pro/drashti/main/assets/Screenshot%202021-02-24%20at%209.56.13%20AM.png?token=AEZOEVEBDMWDACYG2G7YUILAYNJSO)

### Requirements

- Operating System - Any 32 bit or 64 bit operating system running Linux or UNIX based operating system on which all the required applications can be installed. This can also be a guest operating system in a virtualized environment.
- Browser - Any modern web browser last updated in 2018 or later with JavaScript enabled with HTML5 compatibility.
- Python3 Interpreter - Python3 should be installed on the host system as the core functionality is written in Python.
- Flask - It is a micro web framework written in Python. This framework is used for web servers.
- Database - This application keeps all the information in a single database on MySQL. The MySQL server should be installed on the host machine .

### Network Design

![networkDesign](https://raw.githubusercontent.com/deepak-pro/drashti/main/assets/5.jpg?token=AEZOEVEMXWMOQEPFOJUTM7DAYNISK)

All the devices including the client and web application server are connected to tha main router on the same level.

### FAQ

![faq](https://raw.githubusercontent.com/deepak-pro/drashti/main/assets/Screenshot%202021-02-24%20at%209.57.13%20AM.png?token=AEZOEVEEBTWMSJCYQEHK2MLAYNJ4O)



### Conclusion

Managing a network is a very big functional area along with performance, device maintenance, performance monitoring, troubleshooting, plan of change and etc.Monitoring is a very important issue in an organization network which arose over the time. Monitoring is the only way to find out whether the network is functioning according to plan. In order to know what is happening in a network,how it is functioning at any given time. This activity can be easily done by the Drashti Network Monitoring tool. It lets the user know the status of the network at any given time. This logging can give the user a wide view what can’t be seen in general.The purpose of this project is to get an overall idea about the importance of network monitoring and what are the facts need to be considered while monitoring a network.Monitoring a network with the least effects on network performance is the best solution in case of monitoring.The outcome from these monitoring tools is a wide range of useful data and integration of these data produces the status of the network at any given time.Moreover these data will be logged to create a statistical report. Different users such as a network admin and organization can use this information from different perspectives to make a network more efficient for users.