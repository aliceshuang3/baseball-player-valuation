/* SPEED 2019 WAR Baseball Visualization
Prototype - building off Nabil's example: https://gist.github.com/bulbil/474ed23ae7edf3f115aaf5ba18762376
Alice Huang 6/26/19
*/

// set up variables
const width = window.innerWidth,
      height = window.innerHeight;

let data = [],
    currData = [],
    data2 = [],
    chartData = [],
    cleanData = [],
    addData = [],
    currData2 = [],
    currFilter;

// d3 elements
const svg = d3.select('svg')
              .attr('width', width)
              .attr('height', height)
              .attr('border', "1px solid #000");

// append d3 layers
let players = svg.append('g').attr('id','players');
let points = svg.append('g').attr('id','points');
let charts = svg.append('g').attr('id','charts');
let checkboxes = svg.append('g').attr('id','checkboxes');

// create axes
const xscale = d3.scaleLinear()
                 .domain([-2,15]) // domain for k that code2.r uses
                 .range([50, width]) // positioning axis from edge of window

const yscale = d3.scaleLinear()
                 .domain([0, 220])
                 .range([height - 50, 0])

const x_axis = d3.axisBottom()
                 .scale(xscale)
                 .ticks(32); // set number of ticks, determines scale

const x_axis_translate = height - 50 // constant for moving x-axis

// add x-axis
svg.append("g")
    .attr("transform", "translate(0, " + x_axis_translate +")")
    .attr('stroke-width',2)
    .call(x_axis);

// add x-axis label
svg.append('text')
   .attr('class','x label')
   .attr('text-anchor','end')
   .attr('font-size','16px')
   .attr('font-family','sans-serif')
   .attr('x',width/2 + 50)
   .attr('y',height - 15)
   .text('k (WAR/season)')

const y_axis = d3.axisLeft()
                 .scale(yscale)
                 .ticks(20);

// add y-axis
svg.append("g")
   .attr("transform", "translate(50, 0)")
   .attr('stroke-width',2)
   .call(y_axis);

// add y-axis label
svg.append('text')
   .attr('class','y label')
   .attr('text-anchor','middle')
   .attr('font-size','16px')
   .attr('font-family','sans-serif')
   .attr('x',-height/2)
   .attr('y',20)
   .attr('transform','rotate(270)')
   .text('Wins Above k WAR')

var highlightTable;
var highlightRows;
// make chart
d3.text("data/tableData.csv").then(function(datasetText) {
  var rows  = d3.csvParseRows(datasetText),
      table = d3.select('body').append('table')
                .style("border-collapse", "collapse")
                .style("border", "2px black solid");
      highlightTable = table;
      highlightRows = rows;

  // headers
  table.append("thead").append("tr")
    .selectAll("th")
    .data(rows[0])
    .enter().append("th")
    .text(function(d) { return d; })
    .style("border", "1px black solid")
    .style("padding", "5px")
    .style("background-color", "lightgray")
    .style("font-weight", "bold")
    .style("text-transform", "uppercase");
  console.log(rows[1][0]);
  // data
  table.append("tbody")
    .selectAll("tr").data(rows.slice(1))
    .enter().append("tr")
    .on('click', function(d) {
      let r = d3.select(this).data()[0][0];
      let x = d3.selectAll('path').data();

      for (var i = 0; i < 54; i+=18) {
        //console.log(r);
        //console.log(d3.selectAll('path').data()[i].name);
        if (r == d3.selectAll('path').data()[i].name) {
          console.log('yes'); // do something when the names match for row clicked and curve
          console.log(i);

        }
      }
    })
    .selectAll("td")
    .data(function(d){return d;})
    .enter().append("td")
    .style("border", "1px black solid")
    .style("padding", "5px")
    .text(function(d){return d;})
    .style("font-size", "12px");

});

// load csv files
// loadData('data/ruthData.csv');
// loadData('data/cleanJeter.csv');
// loadData('data/cleanYastrzemski.csv');

loadBigData('data/top_300_players.csv');


// set domain and range for loaded data for curves
const xScale = d3.scaleLinear()
               .domain([-2,15])
               .range([50, width]);

const yScale = d3.scaleLinear()
               .domain([0, 220])
               .range([height - 50, 0]);

// create curve with k as the x value and cumulative war as the y value
 const lineFunction = d3.line()
      .x(function(d) { return xScale(d.k); })
      .y(function(d) { return yScale(d.war); })
      .curve(d3.curveMonotoneX); // turn line into curve

// load baseball csv, from Nabil's example

// d3.csv('fangraphs-leaderboard.csv', function(d){
//
//     return {
//         name: d.Name.trim(),
//         team: d.Team.trim(),
//         war: Number(d.WAR.trim()),
//         playerid: Number(d.playerid.trim())
//     }
// }).then( function(d) {
//
//     data = d;
//     currData = data;
//     console.log("Baseball currData");
//     console.log(currData);
//
//     drawChart();
// });
//
// // register any listeners
// d3.select('#team-filter input').on('change', function(){
//
//     currFilter = d3.select(this).node().value;
//     currData = currFilter.trim() !== '' ?
//         data.filter( d => d.team == currFilter ) : data;
//
//     // update
//     drawChart();
//
// });




/* HELPER FUNCTIONS */

// loads data for a given csv data file
function loadData(file) {
  d3.csv(file, function(d){
      return {
          k: Number(d.K.trim()),
          war: Number(d.WAR.trim()),
          name: d.NAME
      }
  }).then(function(d){
      console.log(d);
      data2 = d;
      drawChart2();
  });
}

let sum;
let idArray = [],
    players2 = [],
    arr = [],
    kFiltered = [],
    warFiltered = [],
    finalDataArr = [];


// loads data for a big csv data file
function loadBigData(file) {
  d3.csv(file, function(d){
    // put all player ids in an array for parsing
    idArray.push(Number(d.id));

      return {
          id: Number(d.id.trim()),
          season: Number(d.season.trim()),
          war: Number(d.war.trim())
      }
  }).then(function(d){
      //console.log(d);
      loadBigData2('data/top_300_additional_info_players.csv');
      cleanData = d;

  });
}

// load additional top 300 player data
function loadBigData2(file) {
  d3.csv(file, function(d) {

    return {
      name: d.Name.trim(),
      id1: Number(d.FGL.trim()),
      id2: Number(d.MLB.trim()),
      team: d.Team.trim(),
      pos: d.Position.trim(),
      hof: d.IN_HOF.trim()
    }
  }).then(function(d) {
    addData = d;
    calculateWar();
  })

}


let found;
let hof = [];
let checked = false;
let allHOF = [],
    pos = [],
    allPos = [],
    allPosFilt = [];
// filter csv data to calculate cumulative war values
function calculateWar() {
  arr.push(idArray[0])
  for (var i=1; i<5237; i++) {
    if (idArray[i] != idArray[i-1]){
      arr.push(idArray[i])
    }
  }

  // loop through each of the 300 players
  for (var i=0; i<arr.length-1; i++) {
    // put all rows for 1 player in players2 array
    players2 = cleanData.filter(function(d) { return d.id == arr[i]})
    // for each k value, filter out the rows with war > k for that 1 player
    for (var k=-2; k<16; k++) {
      kFiltered = players2.filter(function(d) { return d.war > k});
      warFiltered = kFiltered.map(function(d) { return d.war - k}); // subtract k from each season war
      sum = (warFiltered.reduce(function(total,num) { return total + num}, 0)).toFixed(1); // sum all the season wars

      // construct object with cumulative war values for graphing
      let finalData = {};
      finalData['k'] = k;
      finalData['war'] = sum;

      let found = -1;
      // if player id is in additional players data get index in that data
      for (var n=0; n<addData.length; n++) {
        if (arr[i] == addData[n].id1) {
          found = n;
          // console.log('yes');
          // console.log(n);
        }
      }
      // if ids match for two datasets get the name for the player
      if (found >= 0) {
        finalData['name'] = addData[found].name;
        finalData['hof'] = addData[found].hof;
        finalData['pos'] = addData[found].pos;
      } else {
        finalData['name'] = arr[i];
        finalData['hof'] = 'not found';
        finalData['pos'] = 'not found';
      }

      finalDataArr.push(finalData);

  }

  currData2 = finalDataArr;
  data2 = currData2;
  hof = finalDataArr.filter(function(d) { return d.hof == 'TRUE'})
  pos = finalDataArr.filter(function(d) { return d.pos != 'not found'})
  finalDataArr = [];
  if (hof.length > 0) {
    allHOF.push(hof);
  }
  allPos.push(pos);

  drawChart2('pink',data2);
}

}

// hof listener for checkbox
d3.select('#hof-filter input').on('change', function() {
  cb = d3.select(this);
  if(cb.property('checked')) {
    updateGraph('turquoise',allHOF);
  } else {
    updateGraph('pink',allHOF);
  }
})

// position listener for drop-down
d3.select('#pos-filter select').on('change', function() {
  item = d3.select(this).property('value');
  if(item != '') {
    for (var i=0; i<allPos.length; i++) {
      let temp = allPos[i].filter(function(d) { return d.pos == item});
      if (temp.length > 0) {
        allPosFilt.push(temp);
      }

    }
    console.log(allPosFilt);
    updateGraph('pink',allPos);
    updateGraph('turquoise',allPosFilt);
    allPosFilt = [];
  } else {
    updateGraph('pink',allPos);
  }
})

function updateGraph(color,data) {
  for (var i=0; i<data.length; i++) {
    drawChart2(color,data[i]);
  }
}


// draws rectangles viz, adapted from Nabil's circle example
function drawChart(){

    let currPlayers = players.selectAll('.player')
            .data(currData)

    currPlayers.enter()
        .append('rect')
        .attr('class','player')
        .attr('x', function(d,i) { return Math.random() * width; } )
        .attr('y', function(d,i) { return Math.random() * height; } )
        //.attr('r', function(d,i) { return 15; } )
        .attr('opacity', d => d.war/75 )
        .attr('fill', d => d3.interpolateSpectral( d.war/75 ))
        .attr('width', 10)
        .attr('height', 10);

    currPlayers.exit()
        .transition(500)
        .attr('opacity',0)
        .remove();

    d3.selectAll('.player').on('click', function(d){
        console.log(d.name)
        console.log(d.team)
        console.log(d.playerid)
        console.log('\n')
    });

}

// draws curves of wins above k WAR vs. k
function drawChart2(color, array){
  let currVals = points.append("g")

  // create tooltip for the curve
  const tooltipLine = d3.select('body')
                    .append('div')
                    .style('position', 'absolute')
                    .style('padding', '0 10px')
                    .style('background', 'white')
                    .style('opacity', 0)

  // create tooltip for dots on curve
  const tooltip = d3.select('body')
                    .append('div')
                    .style('position', 'absolute')
                    .style('padding', '0 10px')
                    .style('background', 'white')
                    .style('opacity', 0)

  // draw curves, mousing over shows name of player + changes color

  currVals.append("path").data(array)
          .attr('id','foo')
          .attr("d", lineFunction(array))
          .attr("stroke", color)
          .attr("stroke-width", 1)
          .attr("fill", "none")
          .on('mouseover', function(d) {
            tooltipLine.transition().duration(200)
            .style('opacity', .9)
            tooltipLine.html(d.name)
            .style('left', (d3.event.pageX+10) + 'px')
            .style('top', (d3.event.pageY-50) + 'px')
            .style('width','150px').style('height','18px')
            .style('border-style','solid').style('border-color','blue')
            .style('text-align','center').style('font-family','sans-serif')
            .style('font-size','14px')
            d3.select(this)
              .style('stroke', 'blue')
          })
          .on('mouseout', function(d) {
            tooltipLine.transition().duration(200)
              .style('opacity', 0)
            d3.select(this)
              .style('stroke', color)
          })
          .on('click', function(d) { // clicking on each curve highlights corresponding row in table
            for (var i = 0; i < 7; i++) {
              if (d.name == highlightRows[i][0]) {
                d3.selectAll('tr:nth-child(' + i + ')').style('background-color','turquoise');
              }
            }
          })


  // draws dots along curve for data points, mouseover changes color + size + shows coordinates
  currVals.selectAll('.point').data(array)
        .enter().append('circle')
        .attr('cx', d => xScale(d.k))
        .attr('cy', d => yScale(d.war))
        .attr('r', 3)
        .attr('fill', color)
        .on('mouseover', function(d) {
          tooltip.transition().duration(50)
            .style('opacity', .9)
          tooltip.html(d.k + ', ' + d.war)
            .style('left', (d3.event.pageX+10) + 'px')
            .style('top', (d3.event.pageY-50) + 'px')
            .style('width','70px').style('height','18px')
            .style('border-style','solid').style('border-color','blue')
            .style('text-align','center').style('font-family','sans-serif')
            .style('font-size','14px')
          d3.select(this)
            .style('fill','blue')
            .style('r', 5)
        })
        .on('mouseout', function(d) {
          tooltip.transition().duration(50)
            .style('opacity', 0)
          d3.select(this)
            .style('fill', color)
            .style('r', 3)
        })

currVals.exit()
        .attr('opacity',0)
        .remove();


}
