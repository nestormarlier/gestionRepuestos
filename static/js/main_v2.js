// Data retrieved from https://www.ssb.no/energi-og-industri/olje-og-gass/statistikk/sal-av-petroleumsprodukt/artikler/auka-sal-av-petroleumsprodukt-til-vegtrafikk
Highcharts.chart('container', {
    title: {
        text: 'Repuestos por debajo del stock mínimo',
        align: 'left'
    },
    xAxis: {
        categories: [
            'Cambaceres', 'Quilmes', 'Rivadavia'
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
            name: 'Cambaceres',
            color: '#00FF00',
            y: totalesCambaceres
        }, {
            name: 'Quilmes',
            color: 'red',
            y: totalesQuilmes
        },
        {
            name: 'Rivadavia',
            color: 'yellow',
            y: totalesRivadavia
        }],
    }, {
        type: 'line',
        step: 'center',
        name: 'Total',
        data: [totalesCambaceres, totalesQuilmes,totalesRivadavia],
        marker: {
            lineWidth: 2,
            lineColor: Highcharts.getOptions().colors[3],
            fillColor: 'white'
        }
    }, {
        type: 'pie',
        name: '',
        data: [{
            name: 'Cambaceres',
            y: totalesCambaceres,
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
            name: 'Quilmes',
            y: totalesQuilmes,
            color: 'red'
        }, {
            name: 'Rivadavia',
            y: totalesRivadavia,
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