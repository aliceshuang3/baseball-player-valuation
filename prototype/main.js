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
    currFilter;

// d3 elements
const svg = d3.select('svg')
              .attr('width', width)
              .attr('height', height)
              .attr('border', "1px solid #000");

// append d3 layers
let players = svg.append('g').attr('id','players');
let points = svg.append('g').attr('id','points');

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

// load csv files
loadData('data/ruthData.csv');
loadData('data/cleanJeter.csv');
loadData('data/cleanYastrzemski.csv');

loadFiles(); // to be implemented

// set domain and range for loaded data for curves
var xScale = d3.scaleLinear()
               .domain([-2,15])
               .range([50, width]);

var yScale = d3.scaleLinear()
               .domain([0, 220])
               .range([height - 50, 0]);

// create curve with k as the x value and cumulative war as the y value
 var lineFunction = d3.line()
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

// calls loadData on every file in a given folder
function loadFiles(folder) {
  // d3.csv('/data', function(error, fileArray) {
  //   var q = d3.queue();
  //   fileArray.forEach(function(d) {
  //     q = q.defer(d3.csv, d);
  //   });
  //   q.await(loadData(fileArray[0]));
  // });
}

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
function drawChart2(){
  let currVals = points.selectAll('.point')
          .data(data2)

  // create tooltip for the curve
  const tooltipLine = d3.select('body')
                    .append('div')
                    .style('position', 'absolute')
                    .style('padding', '0 10px')
                    .style('background', 'white')
                    .style('opacity', 0)

  // draw curves, mousing over shows name of player + changes color
  currVals.enter()
          .append("path")
          .attr("d", lineFunction(data2))
          .attr("stroke", "turquoise")
          .attr("stroke-width", 2)
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
              .style('stroke', 'turquoise')
          })

// create tooltip for dots on curve
const tooltip = d3.select('body')
                  .append('div')
                  .style('position', 'absolute')
                  .style('padding', '0 10px')
                  .style('background', 'white')
                  .style('opacity', 0)

// draws dots along curve for data points, mouseover changes color + size + shows coordinates
currVals.enter()
        .append('circle')
        .attr('cx', d => xScale(d.k))
        .attr('cy', d => yScale(d.war))
        .attr('r', 5)
        .attr('fill', 'turquoise')
        .on('mouseover', function(d) {
          tooltip.transition().duration(200)
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
            .style('r', 7)
        })
        .on('mouseout', function(d) {
          tooltip.transition().duration(200)
            .style('opacity', 0)
          d3.select(this)
            .style('fill', 'turquoise')
            .style('r', 5)
        })

  currVals.exit()
    .remove();

}
