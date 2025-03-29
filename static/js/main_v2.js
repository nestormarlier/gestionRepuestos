// Data retrieved from https://www.ssb.no/energi-og-industri/olje-og-gass/statistikk/sal-av-petroleumsprodukt/artikler/auka-sal-av-petroleumsprodukt-til-vegtrafikk
Highcharts.chart('container', {
    title: {
        text: 'Repuestos por debajo del stock mínimo',
        align: 'left'
    },
    xAxis: {
        categories: [
            'Planta A', 'Planta B', 'Planta C'
        ]
    },
    yAxis: {
        title: {
            text: 'Cantidad'
        }
    },
    tooltip: {
        valueSuffix: ' Código/s de repuesto'
    },
    plotOptions: {
        series: {
            borderRadius: '25%'
        }
    },
    series: [{
        type: 'column',
        name: '',
        data: [{
            name: 'Planta A',
            color: '#00FF00',
            y: totalesPlantaA
        }, {
            name: 'Planta B',
            color: 'red',
            y: totalesPlantaB
        },
        {
            name: 'Planta C',
            color: 'yellow',
            y: totalesPlantaC
        }],
    }, {
        type: 'line',
        step: 'center',
        name: 'Total',
        data: [totalesPlantaA, totalesPlantaB,totalesPlantaC],
        marker: {
            lineWidth: 2,
            lineColor: Highcharts.getOptions().colors[3],
            fillColor: 'white'
        }
    }, {
        type: 'pie',
        name: '',
        data: [{
            name: 'Planta A',
            y: totalesPlantaA,
            color: '#00FF00',
            dataLabels: {
                enabled: true,
                distance: -50,
                format: '{point.total}',
                style: {
                    fontSize: '15px'
                }
            }
        }, {
            name: 'Planta B',
            y: totalesPlantaB,
            color: 'red'
        }, {
            name: 'Planta C',
            y: totalesPlantaC,
            color: 'yellow'
        }],
        center: [15, 15],
        size: 100,
        innerSize: '70%',
        showInLegend: false,
        dataLabels: {
            enabled: false
        }
    }]
});