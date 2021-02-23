window.onload = function load(){
    console.log("Wan Info");
    getInfo();
}

function getInfo(){
    fetch('http://ip-api.com/json/')
        .then(response => response.json())
        .then(data => {
            if(data.status == 'success'){
                document.getElementById('info').innerHTML = "Cannot Query Wan IP"
            }
            //console.log(data)
            var txt = ""
            txt += "<tr><td>Location</td><td>" + data.city + " , " + data.regionName + " , " + data.country + "</td></tr>"
            txt += "<tr><td>Wan IP</td><td>" + data.query + "</td></tr>"
            txt += "<tr><td>ISP</td><td>" + data.as + "</td></tr>"
            txt += "<tr><td>Timezone</td><td>" + data.timezone + "</td></tr>"
            txt += "<tr><td>Wan IP</td><td>" + data.query + "</td></tr>"
            console.log(txt)
            document.getElementById('info').innerHTML = txt
        })
}