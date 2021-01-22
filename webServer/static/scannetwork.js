window.onload = function load(){
    console.log("hello");
}

function scan(){
    document.getElementById("ips").innerHTML = ""
    var prefix = "192.168.1."
    var i ;
    for (i=1; i<=10 ;++i){
        check(prefix+i)
    }
}

function addip(ip){
    console.log("Adding ip " + ip)
    title = prompt("Please enter a name for this host") ;
    fetch('addip/'+ip+ '/' + title)
        .then(response => response.text())
        .then((response) => {
            if(response == 1)
                console.log(ip + " added successfully")
            else
                console.log(ip + " already exists")
        }).catch(err => console.log(err))
}

async function check(ip){
    var url = "/scanip/" + ip
    var ips = document.getElementById('ips');
    fetch(url)
        .then(response => response.text())
        .then((response) => {
            if(response == "1"){
                console.log(ip  +" is up")
                var button = '<button onclick="addip(\'' + ip +'\')">Add</button>'
                ips.innerHTML = ips.innerHTML + "<li>" + ip + button + "</li>"
            }    
            else
                console.log(ip +" is down") ;
        }).catch(err => console.log(err))
}
