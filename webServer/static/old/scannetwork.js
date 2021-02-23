window.onload = function load(){
    console.log("Scan Network");
    scan();
}

function scan(){
    document.getElementById("ips").innerHTML = ""
    var prefix = "192.168.1."
    var i ;
    for (i=1; i<=21 ;++i){
        check(prefix+i)
    }
}

function addip(ip){
    console.log("Adding ip " + ip)
    title = prompt("Please enter a name for this host") ;
    des = prompt("Please enter a short description") ;
    fetch('addip/'+ip+ '/' + title + '/' + des)
        .then(response => response.text())
        .then((response) => {
            //console.log("Recieved response "+ response)
            if(response == 1){
                //console.log(ip + " added successfully")
                alert("Record Added Successfully")
            }
            else{
                //console.log(ip + " already exists")
                alert("This host is already added, Click on nodes settings to change")
            }
                
        }).catch(err => console.log(err))
}

async function check(ip){
    var url = "/scanip/" + ip
    var ips = document.getElementById('ips');
    fetch(url)
        .then(response => response.text())
        .then((response) => {
            if(response == "1"){
                //console.log(ip  +" is up")
                var button = '<button onclick="addip(\'' + ip +'\')">Add</button>'
                ips.innerHTML = ips.innerHTML + "<li>" + ip + button + "</li>"
            }    
            //else
                //console.log(ip +" is down") ;
        }).catch(err => console.log(err))
}
