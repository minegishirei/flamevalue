
  var theme = {
    color: [
      '#26B99A', '#34495E', '#BDC3C7', '#3498DB',
      '#9B59B6', '#8abb6f', '#759c6a', '#bfd3b7'
    ],

    title: {
      itemGap: 8,
      textStyle: {
        fontWeight: 'normal',
        color: '#408829'
      }
    },

    dataRange: {
      color: ['#1f610a', '#97b58d']
    },

    toolbox: {
      color: ['#408829', '#408829', '#408829', '#408829']
    },

    tooltip: {
      backgroundColor: 'rgba(0,0,0,0.5)',
      axisPointer: {
        type: 'line',
        lineStyle: {
          color: '#408829',
          type: 'dashed'
        },
        crossStyle: {
          color: '#408829'
        },
        shadowStyle: {
          color: 'rgba(200,200,200,0.3)'
        }
      }
    },

    dataZoom: {
      dataBackgroundColor: '#eee',
      fillerColor: 'rgba(64,136,41,0.2)',
      handleColor: '#408829'
    },
    grid: {
      borderWidth: 0
    },

    categoryAxis: {
      axisLine: {
        lineStyle: {
          color: '#408829'
        }
      },
      splitLine: {
        lineStyle: {
          color: ['#eee']
        }
      }
    },

    valueAxis: {
      axisLine: {
        lineStyle: {
          color: '#408829'
        }
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: ['rgba(250,250,250,0.1)', 'rgba(200,200,200,0.1)']
        }
      },
      splitLine: {
        lineStyle: {
          color: ['#eee']
        }
      }
    },
    timeline: {
      lineStyle: {
        color: '#408829'
      },
      controlStyle: {
        normal: { color: '#408829' },
        emphasis: { color: '#408829' }
      }
    },

    k: {
      itemStyle: {
        normal: {
          color: '#68a54a',
          color0: '#a9cba2',
          lineStyle: {
            width: 1,
            color: '#408829',
            color0: '#86b379'
          }
        }
      }
    },
    map: {
      itemStyle: {
        normal: {
          areaStyle: {
            color: '#ddd'
          },
          label: {
            textStyle: {
              color: '#c12e34'
            }
          }
        },
        emphasis: {
          areaStyle: {
            color: '#99d2dd'
          },
          label: {
            textStyle: {
              color: '#c12e34'
            }
          }
        }
      }
    },
    force: {
      itemStyle: {
        normal: {
          linkStyle: {
            strokeColor: '#408829'
          }
        }
      }
    },
    chord: {
      padding: 4,
      itemStyle: {
        normal: {
          lineStyle: {
            width: 1,
            color: 'rgba(128, 128, 128, 0.5)'
          },
          chordStyle: {
            lineStyle: {
              width: 1,
              color: 'rgba(128, 128, 128, 0.5)'
            }
          }
        },
        emphasis: {
          lineStyle: {
            width: 1,
            color: 'rgba(128, 128, 128, 0.5)'
          },
          chordStyle: {
            lineStyle: {
              width: 1,
              color: 'rgba(128, 128, 128, 0.5)'
            }
          }
        }
      }
    },
    gauge: {
      startAngle: 225,
      endAngle: -45,
      axisLine: {
        show: true,
        lineStyle: {
          color: [[0.2, '#86b379'], [0.8, '#68a54a'], [1, '#408829']],
          width: 8
        }
      },
      axisTick: {
        splitNumber: 10,
        length: 12,
        lineStyle: {
          color: 'auto'
        }
      },
      axisLabel: {
        textStyle: {
          color: 'auto'
        }
      },
      splitLine: {
        length: 18,
        lineStyle: {
          color: 'auto'
        }
      },
      pointer: {
        length: '90%',
        color: 'auto'
      },
      title: {
        textStyle: {
          color: '#333'
        }
      },
      detail: {
        textStyle: {
          color: 'auto'
        }
      }
    },
    textStyle: {
      fontFamily: 'Arial, Verdana, sans-serif'
    }
  };



  //TODO: 場所移動
  if ($('#echart_line').length) {

    json_data = JSON.parse(`
    {{ score_graph_json | safe }}
    `)
    date_list = []
    money_list = []
    overtime_list = []
    count_list = []
    remote_list = []
    for (k in json_data) {
      row = json_data[k]
      date_list.push(row.date)
      money_list.push(row.values.money)
      overtime_list.push(row.values.overtime)
      count_list.push(row.values.count)
      remote_list.push(row.values.remote)
    }
    console.log(date_list)
    console.log(money_list)
    console.log(count_list)
    console.log(remote_list)

    var echartLine = echarts.init(document.getElementById('echart_line'), theme);

    echartLine.setOption({
      title: {
        text: 'Django',
        subtext: 'ー Django'
      },
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        x: 220,
        y: 40,
        data: ['最低年収', '最大年収', '求人数', 'リモート率']
      },
      toolbox: {
        show: true,
        feature: {
          magicType: {
            show: true,
            title: {
              line: 'Line',
              bar: 'Bar',
              stack: 'Stack',
              tiled: 'Tiled'
            },
            type: ['line', 'bar', 'stack', 'tiled']
          },
          restore: {
            show: true,
            title: "Restore"
          },
          saveAsImage: {
            show: true,
            title: "Save Image"
          }
        }
      },
      calculable: true,
      xAxis: [{
        type: 'category',
        boundaryGap: false,
        data: date_list
      }],
      yAxis: [{
        type: 'value'
      }],
      series: [{
        name: '最低年収',
        type: 'line',
        smooth: true,
        itemStyle: {
          normal: {
            areaStyle: {
              type: 'default'
            }
          }
        },
        data: money_list
      }, {
        name: '最大年収',
        type: 'line',
        smooth: true,
        itemStyle: {
          normal: {
            areaStyle: {
              type: 'default'
            }
          }
        },
        data: overtime_list
      }, {
        name: '求人数',
        type: 'line',
        smooth: true,
        itemStyle: {
          normal: {
            areaStyle: {
              type: 'default'
            }
          }
        },
        data: count_list.map((row) => row * 100)
      }, {
        name: 'リモート率',
        type: 'line',
        smooth: true,
        itemStyle: {
          normal: {
            areaStyle: {
              type: 'default'
            }
          }
        },
        data: remote_list.map((row) => row == undefined ? 0 : row)
      }]
    });

  }



//echart Bar

var money_list_dict = JSON.parse(`
  {{ money_countlist | safe }}
  `)

var upper_money_list = money_list_dict.upper
var lower_money_list = money_list_dict.lower

if ($('#mainb').length) {

  var echartBar = echarts.init(document.getElementById('mainb'), theme);

  echartBar.setOption({
    title: {
      text: '{{ name }}',
      subtext: '単位：件/万円'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['下限', '上限']
    },
    toolbox: {
      show: false
    },
    calculable: false,
    xAxis: [{
      type: 'category',
      data: ['0', '100', '200', '300', '400', '500', '600', '700', '800', '900']
    }],
    yAxis: [{
      type: 'value'
    }],
    series: [{
      name: '下限',
      type: 'bar',
      data: lower_money_list,
      markPoint: {
        data: [{
          type: 'max',
          name: '???'
        }]
      },
      markLine: {
        data: [{
          type: 'average',
          name: '???'
        }]
      }
    }, {
      name: '上限',
      type: 'bar',
      data: upper_money_list,
      markPoint: {
        data: [{
          type: 'max',
          name: '???'
        }]
      },
      markLine: {
        data: [{
          type: 'average',
          name: '???'
        }]
      }
    }
    ]
  });

}




const query = document.getElementById("query_text_box")
query.addEventListener('focus', function (event) {
  function popup_candidate_list(candidate_list) {
    document.getElementById("candidate_list").innerHTML = (`<option value="${candidate_list.join('"><option value="')}"</li>`)
  }
  url = `https://${location.hostname}/api/candidate/?unfinished_title=rub`
  fetch(url)
    .then(response => response.json())
    .then(function (json) {
      console.log(json)
      popup_candidate_list(json.candidate)
    });
});
function transition() {
  query_text = document.getElementById("query_text_box").value
  location.href = ("/" + query_text)
}

document.getElementById("query_text_box").onkeydown = function (event) {
  if (event.key === 'Enter') {
    query_text = document.getElementById("query_text_box").value
    location.href = ("/" + query_text)
  }
}


if (window.innerWidth < 700) {
  document.getElementById("js_hidden").innerHTML = ""
}