window.onload = function load() {
    console.log("Dashboard")
    getstats()
    getnodes()
}

function getstats(ip) {
    console.log("Gettings Stats")
    fetch('stats')
        .then(response => response.text())
        .then((response) => {
            console.log("Recieved response " + response)
            var data = response.split(" ")

            document.getElementById("totalnodes").innerHTML = data[0]
            document.getElementById("totalservers").innerHTML = data[1]
            document.getElementById("activeservers").innerHTML = data[2]
            document.getElementById("inactiveservers").innerHTML = data[3]

            pieChart(data[2], data[3])

        }).catch(err => console.log(err))
}

function getnodes() {
    console.log("Getting nodes")
    fetch('getnodes')
        .then(response => response.text())
        .then((response) => {
            console.log("Recieved response " + response)
            var data = response.split(";")
            console.log(data)
            graph(data)
        }).catch(err => console.log(err))
}

function graph(list) {
    am4core.ready(function () {

        c = []
        var i = 0;
        for (i = 0; i < list.length; ++i) {
            console.log(list[i])
            obj = { name: list[i], value: 100 }
            c.push(obj)
        }

        console.log(c)
        am4core.useTheme(am4themes_animated);

        var chart = am4core.create("graphdiv", am4plugins_forceDirected.ForceDirectedTree);
        var networkSeries = chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())

        chart.data = [
            {
                name: "Router",
                children: c
            }

        ];

        networkSeries.dataFields.value = "value";
        networkSeries.dataFields.name = "name";
        networkSeries.dataFields.children = "children";
        networkSeries.nodes.template.tooltipText = "{name}:{value}";
        networkSeries.nodes.template.fillOpacity = 1;

        networkSeries.nodes.template.label.text = "{name}"
        networkSeries.fontSize = 20;

        networkSeries.links.template.strokeWidth = 1;

        var hoverState = networkSeries.links.template.states.create("hover");
        hoverState.properties.strokeWidth = 3;
        hoverState.properties.strokeOpacity = 1;

        networkSeries.nodes.template.events.on("over", function (event) {
            event.target.dataItem.childLinks.each(function (link) {
                link.isHover = true;
            })
            if (event.target.dataItem.parentLink) {
                event.target.dataItem.parentLink.isHover = true;
            }

        })

        networkSeries.nodes.template.events.on("out", function (event) {
            event.target.dataItem.childLinks.each(function (link) {
                link.isHover = false;
            })
            if (event.target.dataItem.parentLink) {
                event.target.dataItem.parentLink.isHover = false;
            }
        })

    }); 
}

function pieChart(a, i) {
    am4core.ready(function () {
        am4core.useTheme(am4themes_animated);
        var chart = am4core.create("chartdiv", am4charts.PieChart);
        chart.data = [{
            "status": "Active Server",
            "numbers": a
        }, {
            "status": "Inactive Server",
            "numbers": i
        }];
        var pieSeries = chart.series.push(new am4charts.PieSeries());
        pieSeries.dataFields.value = "numbers";
        pieSeries.dataFields.category = "status";
        pieSeries.slices.template.stroke = am4core.color("#fff");
        pieSeries.slices.template.strokeWidth = 2;
        pieSeries.slices.template.strokeOpacity = 1;

        pieSeries.hiddenState.properties.opacity = 1;
        pieSeries.hiddenState.properties.endAngle = -90;
        pieSeries.hiddenState.properties.startAngle = -90;

    });
}