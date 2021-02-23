window.onload = function load(){
    console.log("Show Nodes");
    fetchNodes();
    setInterval(fetchNodes,5000) ;
}

function socketRun(){
	var socket = io.connect('http://127.0.0.1:4000');

    socket.on('connect', function() {
        console.log("Socket is connected");
        socket.send("User has connected");
        socket.send("run")
    });

    socket.on('message',function(msg){
        //console.log("Message Recieved:" + msg)
        document.getElementById('m').innerHTML += msg + "<br>"
    });

}

function removeNode(ip){
    console.log("Removing node "+ ip)
    fetch('/removenode/'+ip)
        .then(response => response.text())
        .then((response) => {
            if(response == "1"){
                alert("Node Removed : "+ip)
            }else{
                alert("Error removing node")
            }
        })
}

function addToServer(ip){
    console.log("Adding " + ip + " to server list")
    fetch('/addserver/'+ip)
        .then(response => response.text())
        .then((response) => {
            console.log("Recieved response "+ response)
            if(response == "1"){
                //console.log(ip + " added to server successfully")
                alert("Server Added Successfully")
            }
            else{
                //console.log(ip + " already exists")
                alert("This host is already added to server")
            }
                
        }).catch(err => console.log(err))
}

function fetchNodes(){
    var ele = document.getElementById("shownodes")
    fetch('/nodes')
        .then(response => response.text())
        .then((response) => {
            //console.log("Recieved response "+ response)
            ele.innerHTML = ""
            var txt = "<table border='1'><tr><th>Status</th><th>Name</th><th>IP</th><th>Description</th><th>RTT</th></tr>"
            obj = JSON.parse(response)
            for(x in obj){
                var st = "🔴"
                if(obj[x].status == "1")
                    st = "🟢"
                var rtt = ""
                if(obj[x].status == "0")
                    rtt = "∞"
                else
                    rtt = obj[x].rtt
                txt += "<tr><td>" + st + "</td><td>" +obj[x].name + "</td><td>" + obj[x].ip + "</td><td>" + obj[x].description + "</td><td>" + rtt + "</td><td><input type='button' value='Add to Server' onclick=addToServer('" + obj[x].ip + "')></td>" + "</td><td><input type='button' value='Remove Node' onclick=removeNode('" + obj[x].ip + "')></td>" + "</tr>";
            }
            txt += "</table>"
            ele.innerHTML = txt
        }).catch(err => console.log(err))
}