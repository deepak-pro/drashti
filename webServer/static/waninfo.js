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
            txt += "Wan IP : " + data.query + "<br>"
            txt += "Location : " + data.city + " , " + data.regionName + " , " + data.country + "<br>"
            txt += "ISP : " + data.isp + "<br>"
            txt += "Timezone : " + data.timezone + "<br>"
            document.getElementById('info').innerHTML = txt
        })
}