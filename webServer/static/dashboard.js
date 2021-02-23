window.onload = function load(){
    console.log("Dashboard")
    getstats()
}

function getstats(ip){
    console.log("Gettings Stats")
    fetch('stats')
        .then(response => response.text())
        .then((response) => {
            console.log("Recieved response "+ response)
            var data = response.split(" ")

            document.getElementById("totalnodes").innerHTML = data[0]
            document.getElementById("totalservers").innerHTML = data[1]
            document.getElementById("activeservers").innerHTML = data[2]
            document.getElementById("inactiveservers").innerHTML = data[3]

        }).catch(err => console.log(err))
}
