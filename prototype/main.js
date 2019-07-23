/* SPEED 2019 WAR Baseball Visualization
Prototype - building off Nabil's example: https://gist.github.com/bulbil/474ed23ae7edf3f115aaf5ba18762376
Alice Huang 6/26/19
*/

/*****************************************************************************/
// VARIABLES
const width = window.innerWidth,
      height = window.innerHeight;

let data2 = [], cleanData = [], addData = [], // used in loading data
    highlightRows, allPlayers = [], // used in table
    sum, idArray = [], players2 = [], arr = [], kFiltered = [], warFiltered = [], finalDataArr = [], // used in calculateWar
    found, hof = [], allHOF = [], pos = [], allPos = [], allPosFilt = [];

/*****************************************************************************/
// D3 ELEMENTS
const svg = d3.select('svg')
              .attr('width', width)
              .attr('height', height)
              .attr('border', "1px solid #000");

// append d3 layers
let points = svg.append('g').attr('id','points');

/*****************************************************************************/
// LOAD DATA
loadBigData('data/top_300_players.csv'); // csv scraped by Bilal/Helen from fangraphs

// set domain and range for loaded data for curves
const xScale = d3.scaleLinear()
               .domain([-2,15])
               .range([50, 0.6 * width]);

const yScale = d3.scaleLinear()
               .domain([0, 220])
               .range([0.75 * height, 0]);

// create curve with k as the x value and cumulative war as the y value
 const lineFunction = d3.line()
      .x(function(d) { return xScale(d.k); })
      .y(function(d) { return yScale(d.war); })
      .curve(d3.curveMonotoneX); // turn line into curve

/*****************************************************************************/
// SET-UP
// create axes
const xscale = d3.scaleLinear()
                 .domain([-2,15]) // domain for k that code2.r uses
                 .range([50, 0.6 * width]) // positioning axis from edge of window

const yscale = d3.scaleLinear()
                 .domain([0, 220])
                 .range([0.75 * height, 0])

const x_axis = d3.axisBottom()
                 .scale(xscale)
                 .ticks(32); // set number of ticks, determines scale

const x_axis_translate = 0.75 * height // constant for moving x-axis

const y_axis = d3.axisLeft()
                 .scale(yscale)
                 .ticks(20);

const y_axis_translate = 50

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
   .attr('x', (0.6 * width)/2 + 50)
   .attr('y', (0.75 * height) + 50)
   .text('k (WAR/season)')

// add y-axis
svg.append("g")
   .attr("transform", "translate(" + y_axis_translate + ", 0)")
   .attr('stroke-width',2)
   .call(y_axis);

// add y-axis label
svg.append('text')
   .attr('class','y label')
   .attr('text-anchor','middle')
   .attr('font-size','16px')
   .attr('font-family','sans-serif')
   .attr('x',(-0.75*height)/2)
   .attr('y',20)
   .attr('transform','rotate(270)')
   .text('Wins Above k WAR')

/************************************/
// create data table
drawTable();

/*****************************************************************************/
// HELPER FUNCTIONS

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
      loadBigData2('data/top_300_additional_info_players.csv');
      getAllPlayers('data/top_300_additional_info_players.csv'); // load player names for name search
      cleanData = d; // save data to be accessed later
  });
}

/************************************/
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

/************************************/
// filter csv data to calculate cumulative war values
function calculateWar() {
  arr.push(idArray[0])

  // filter to get array with one entry per player id
  for (var i=1; i<5237; i++) {
    if (idArray[i] != idArray[i-1]){ // check if current id is same as previous one
      arr.push(idArray[i]) // if new array aka next player, add to array of players
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
        }
      }
      // if ids match for two datasets get the name, hof, pos for the player
      if (found >= 0) {
        finalData['name'] = addData[found].name;
        finalData['hof'] = addData[found].hof;
        finalData['pos'] = addData[found].pos;
      } else {
        finalData['name'] = arr[i];
        finalData['hof'] = 'not found';
        finalData['pos'] = 'not found';
      }

      finalDataArr.push(finalData); // create array of objects

  }

  data2 = finalDataArr;
  // filter for hof players
  hof = finalDataArr.filter(function(d) { return d.hof == 'TRUE'})
  // make array with all players that have a valid position
  pos = finalDataArr.filter(function(d) { return d.pos != 'not found'})
  // clear the object array
  finalDataArr = [];

  if (hof.length > 0) {
    allHOF.push(hof);
  }
  allPos.push(pos);

  // draw a curve using final clean data
  drawChart2('pink',data2);
}

}

/************************************/
// draw curves in appropriate color for parameter filters
function updateGraph(color,data) {
  for (var i=0; i<data.length; i++) {
    drawChart2(color,data[i]);
  }
}

/************************************/
// draws curves of wins above k WAR vs. k
function drawChart2(color, array){
  let currVals = points.append("g")

  // makes sure not to draw multiple paths per player
  const nestedArray = d3.nest()
    .key(function(d) { return d.name})
    .entries(array);

  currVals.append("path").data(nestedArray)
          .attr('class','curves')
          .attr('id', function(d) { return 'a-' + d.values[0].id;})
          .attr("d", function(d) { return lineFunction(d.values);}) // call earlier curve function
          .attr("stroke", color)
          .attr("stroke-width", 1)
          .attr("fill", "none")
          .on('mouseover', function(d) { // mouseover changes color of curve, shows tooltip with name of player
            makeToolTip();
            tooltip.transition().duration(200)
            .attr('id','tool1')
            .style('opacity', .9)
            tooltip.html(d.values[0].name)
            .style('left', (d3.event.pageX+10) + 'px')
            .style('top', (d3.event.pageY-50) + 'px')
            d3.select(this)
              .style('stroke', 'blue')
          })
          .on('mouseout', function(d) {
            tooltip.transition().duration(200)
              .style('opacity', 0)
            d3.select(this)
              .style('stroke', color)
          })
          .on('click', function(d) { // clicking on each curve highlights corresponding row in table
            for (var i = 0; i < 276; i++) {
              if (d.values[0].name == highlightRows[i][0]) {
                d3.selectAll('tbody tr:nth-child(' + i + ')').style('background-color','turquoise');
              }
            }
          })



  // draws dots along curve for data points
  currVals.selectAll('.point').data(array)
        .enter().append('circle')
        .attr('class','curves')
        .attr('id','dots')
        .attr('cx', d => xScale(d.k))
        .attr('cy', d => yScale(d.war))
        .attr('r', 3)
        .attr('fill', color)
        .on('mouseover', function(d) { // mouseover changes color + size + shows coordinates
          makeToolTip();
          tooltip.transition().duration(50)
          .attr('id','tool2')
            .style('opacity', .9)
          tooltip.html(d.k + ', ' + d.war)
            .style('left', (d3.event.pageX+10) + 'px')
            .style('top', (d3.event.pageY-50) + 'px')
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

/************************************/
let tooltip;
function makeToolTip() {
  // create tooltip for the curve and dots
  tooltip = d3.select('body')
                    .append('span')
}

/************************************/
// create data table
function drawTable() {
  d3.text("data/tableData.csv").then(function(datasetText) {
    let rows  = d3.csvParseRows(datasetText),
        table = d3.select('#table').append('table')

        highlightRows = rows; // use for highlighting pattern on click for curves

    // headers
    table.append("thead").append("tr")
      .selectAll("th")
      .data(rows[0])
      .enter().append("th")
      .text(function(d) { return d; })

    // data
    table.append("tbody")
      .selectAll("tr").data(rows.slice(1))
      .enter().append("tr")
      .on('click', function(d) {
        // search through all curves to find matching name, highlight curve
        let n = d3.select(this).data()[0][0];
        for (var i=0; i<allPos.length; i++) {
          let temp = allPos[i].filter(function(d) { return d.name == n});
          if (temp.length > 0) {
            allPosFilt.push(temp);
          }
        }
        updateGraph('red', allPosFilt)
        allPosFilt = []
      })
      .selectAll("td")
      .data(function(d){return d;})
      .enter().append("td")
      .text(function(d){return d;})

  });
}

/************************************/
// add names to name search drop down
function getAllPlayers(file){
  d3.csv(file, function(d){
    allPlayers.push(d.Name);
  }).then(function(){
    var select = d3.select('datalist')
      .append('select')
        .attr('class','select')
        .on('change',onchange);
    var options = select
      .selectAll('option')
        .data(allPlayers).enter()
        .append('option')
            .text(function (d) { return d; });
  })
}

/*****************************************************************************/
// LISTENERS
// hof listener for checkbox
d3.select('#hof-filter input').on('change', function() {
  cb = d3.select(this);
  if(cb.property('checked')) {
    updateGraph('turquoise',allHOF); // if checkbox checked, draw hof players in turquoise
  } else {
    updateGraph('pink',allHOF);
  }
})

// position listener for drop-down
d3.select('#pos-filter select').on('change', function() {
  item = d3.select(this).property('value'); // get drop-down selection
  if(item != '') {
    for (var i=0; i<allPos.length; i++) {
      let temp = allPos[i].filter(function(d) { return d.pos == item});
      if (temp.length > 0) {
        allPosFilt.push(temp); // array of all players of that position
      }

    }
    updateGraph('pink',allPos);
    updateGraph('turquoise',allPosFilt);
    allPosFilt = [];
  } else {
    updateGraph('pink',allPos);
  }
})

// name listener for search bar
d3.select("#name-filter input").on("change", function(){
   let txt = document.getElementById("player-choice").value;
   if (txt){
     console.log("EXISTS! "+txt);
   }else{
     console.log("DNE")
   }
   for (var i=0; i<allPos.length; i++) {
     let temp = allPos[i].filter(function(d) { return d.name == txt});
     if (temp.length > 0) {
       allPosFilt.push(temp);
     }
   }
   updateGraph('red', allPosFilt)
   allPosFilt = []

 });
