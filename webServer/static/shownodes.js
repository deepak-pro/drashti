window.onload = function load(){
    console.log("hello");
    fetchNodes();
}



function addToServer(ip){
    console.log("Adding " + ip + " to server list")
    fetch('/addserver/'+ip)
        .then(response => response.text())
        .then((response) => {
            console.log("Recieved response "+ response)
            if(response == 1){
                console.log(ip + " added to server successfully")
                //alert("Server Added Successfully")
            }
            else{
                console.log(ip + " already exists")
                //alert("This host is already added to server")
            }
                
        }).catch(err => console.log(err))
}

function fetchNodes(){
    fetch('/nodes')
        .then(response => response.text())
        .then((response) => {
            console.log("Recieved response "+ response)
            var ele = document.getElementById("show")
            var txt = "<table border='1'><tr><th>Name</th><th>IP</th><th>Description</th></tr>"
            obj = JSON.parse(response)
            for(x in obj){
                txt += "<tr><td>" + obj[x].name + "</td><td>" + obj[x].ip + "</td><td>" + obj[x].description + "</td><td><input type='button' value='Add to Server' onclick=addToServer('" + obj[x].ip + "')></td></tr>";
            }
            txt += "</table>"
            ele.innerHTML = txt
        }).catch(err => console.log(err))
}