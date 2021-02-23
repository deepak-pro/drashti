window.onload = function load(){
    console.log("Show Server");
    fetchServers();
    setInterval(fetchServers,1000);
}

function socketRun(){
	var socket = io.connect('http://127.0.0.1:4000');

    socket.on('connect', function() {
        console.log("Socket is connected");
        socket.send("User has connected");
        //socket.send("run")
    });

    socket.on('message',function(msg){
        //console.log("Message Recieved:" + msg)
        document.getElementById('m').innerHTML += msg + "<br>"
    });

}

function removeserver(ip){
    console.log("Removing " + ip + " from server list")
    fetch('/removeserver/'+ip)
        .then(response => response.text())
        .then((response) => {
            console.log("Recieved response "+ response)
            if(response == 1){
                //console.log(ip + " removed from server")
                alert("Removed from server")
            }
            else{
                //console.log(ip + " does not exists")
                alert("This ip does not exists in server list")
            }
                
        }).catch(err => console.log(err))
    fetchServers();
}

function fetchServers(){
    var ele = document.getElementById("showserver")
    fetch('/servers')
        .then(response => response.text())
        .then((response) => {
            //console.log("Recieved response "+ response)
            ele.innerHTML = ""
            //var txt = "<table border='1'><tr><th>Status</th><th>Name</th><th>IP</th><th>Description</th></tr>"
            var txt = ""
            obj = JSON.parse(response)
            for(x in obj){
                var rtt = "∞"
                var st = '<h4><span class="badge badge-dot mr-10"><i class="bg-danger"></i><span>Not Active</span></h4>'
                if(obj[x].status == "1"){
                    st = '<h4><span class="badge badge-dot mr-10"><i class="bg-success"></i><span>Active</span></h4>'
                    rtt = obj[x].rtt
                } 
                txt += "<tr><td>"+ st + "</td><td>" + obj[x].name + "</td><td>" + obj[x].ip + "</td><td>"+ obj[x].description + "<td> "+ rtt +  "</td><td><input type='button' class='btn btn-primary' value='Remove Server' onclick='removeserver(\"" + obj[x].ip + "\")'></td></tr>";
                
            }
            txt += "</table>"
            ele.innerHTML = txt
        }).catch(err => console.log(err))
}