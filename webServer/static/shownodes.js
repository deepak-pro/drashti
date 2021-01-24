window.onload = function load(){
    console.log("hello");
    fetchNodes();
}

function fetchNodes(){
    fetch('/nodes')
        .then(response => response.text())
        .then((response) => {
            console.log("Recieved response "+ response)
            var ele = document.getElementById("show")
            var txt = "<table border='1'><tr><th>Name</th><th>IP</th></tr>"
            obj = JSON.parse(response)
            for(x in obj){
                txt += "<tr><td>" + obj[x].name + "</td><td>" + obj[x].ip + "</td></tr>";
            }
            txt += "</table>"
            ele.innerHTML = txt
        }).catch(err => console.log(err))
}