function graphState(id) {
  var counter = 0;
  var data = {};

  $.getJSON("http://api.census.gov/data/timeseries/asm/state?get=NAICS_TTL,EMP,GEO_TTL&for=state:" + id + "&YEAR=2005,2006,2007,2008,2009,2010,2011,2012,2013,2014&NAICS=31-33&key=81cdc733d3ac0f3496a88eebbed0a31478c403c6")
  .then(convertResultsToObjects)
  .then(function(results) {
    var data = _.map(results, function(r) { return [r.YEAR, r.EMP]; });
    graph(data, $("#employment-by-state").get(0));
  });

}

function buildStateSelect() {
  var states = fipsCodes();
  states.forEach(function(state){
    $(".states").append($("<option value='" + state.fipsCode + "'>" + state.stateName + "</option>"));
  });
  $('.states').on("change", function() {
    graphState($(this).val());
  });

}

function fipsCodes() {
  return [
    { fipsCode: "01", stateName: "Alabama"},
    { fipsCode: "02", stateName: "Alaska"},
    { fipsCode: "04", stateName: "Arizona"},
    { fipsCode: "05", stateName: "Arkansas"},
    { fipsCode: "06", stateName: "California"},
    { fipsCode: "08", stateName: "Colorado"},
    { fipsCode: "09", stateName: "Connecticut"},
    { fipsCode: "10", stateName: "Delaware"},
    { fipsCode: "11", stateName: "District of Columbia"},
    { fipsCode: "12", stateName: "Florida"},
    { fipsCode: "13", stateName: "Geogia"},
    { fipsCode: "15", stateName: "Hawaii"},
    { fipsCode: "16", stateName: "Idaho"},
    { fipsCode: "17", stateName: "Illinois"},
    { fipsCode: "18", stateName: "Indiana"},
    { fipsCode: "19", stateName: "Iowa"},
    { fipsCode: "20", stateName: "Kansas"},
    { fipsCode: "21", stateName: "Kentucky"},
    { fipsCode: "22", stateName: "Louisiana"},
    { fipsCode: "23", stateName: "Maine"},
    { fipsCode: "24", stateName: "Maryland"},
    { fipsCode: "25", stateName: "Massachusetts"},
    { fipsCode: "26", stateName: "Michigan"},
    { fipsCode: "27", stateName: "Minnesota"},
    { fipsCode: "28", stateName: "Mississippi"},
    { fipsCode: "29", stateName: "Missouri"},
    { fipsCode: "30", stateName: "Montana"},
    { fipsCode: "31", stateName: "Nebraska"},
    { fipsCode: "32", stateName: "Nevada"},
    { fipsCode: "33", stateName: "New Hampshire"},
    { fipsCode: "34", stateName: "New Jersey"},
    { fipsCode: "35", stateName: "New Mexico"},
    { fipsCode: "36", stateName: "New York"},
    { fipsCode: "37", stateName: "North Carolina"},
    { fipsCode: "38", stateName: "North Dakota"},
    { fipsCode: "39", stateName: "Ohio"},
    { fipsCode: "40", stateName: "Oklahoma"},
    { fipsCode: "41", stateName: "Oregon"},
    { fipsCode: "42", stateName: "Pennsylvania"},
    { fipsCode: "44", stateName: "Rhode Island"},
    { fipsCode: "45", stateName: "South Carolina"},
    { fipsCode: "46", stateName: "South Dakota"},
    { fipsCode: "47", stateName: "Tennessee"},
    { fipsCode: "48", stateName: "Texas"},
    { fipsCode: "49", stateName: "Utah"},
    { fipsCode: "50", stateName: "Vermont"},
    { fipsCode: "51", stateName: "Virginia"},
    { fipsCode: "53", stateName: "Washington"},
    { fipsCode: "54", stateName: "West Virginia"},
    { fipsCode: "55", stateName: "Wisconsin"},
    { fipsCode: "56", stateName: "Wyoming"}
  ];
}
