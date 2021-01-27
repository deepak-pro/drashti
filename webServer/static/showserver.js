window.onload = function load(){
    console.log("hello");
    fetchServers();
}

function removeserver(ip){
    console.log("Removing " + ip + " from server list")
    fetch('/removeserver/'+ip)
        .then(response => response.text())
        .then((response) => {
            console.log("Recieved response "+ response)
            if(response == 1){
                console.log(ip + " removed from server")
                //alert("Server Added Successfully")
            }
            else{
                console.log(ip + " does not exists")
                //alert("This host is already added to server")
            }
                
        }).catch(err => console.log(err))
}

function fetchServers(){
    fetch('/servers')
        .then(response => response.text())
        .then((response) => {
            console.log("Recieved response "+ response)
            var ele = document.getElementById("show")
            var txt = "<table border='1'><tr><th>Status</th><th>Name</th><th>IP</th><th>Description</th></tr>"
            obj = JSON.parse(response)
            for(x in obj){
                txt += "<tr><td>"+ obj[x].status + "</td><td>" + obj[x].name + "</td><td>" + obj[x].ip + "</td><td>"+ obj[x].description +"</td><td><input type='button' value='Remove Server' onclick='removeserver(\"" + obj[x].ip + "\")'></td></tr>";
            }
            txt += "</table>"
            ele.innerHTML = txt
        }).catch(err => console.log(err))
}