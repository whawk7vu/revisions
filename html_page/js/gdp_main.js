// http://api.census.gov/data/timeseries/asm/industry?get=NAICS_TTL,EMP,PAYANN,GEO_TTL&for=us:*&time=2014&NAICS=31-33&key=81cdc733d3ac0f3496a88eebbed0a31478c403c6
// http://api.census.gov/data/timeseries/asm/state?get=NAICS_TTL,EMP,PAYANN,GEO_TTL&for=state:*&YEAR=2014&NAICS=31-33&key=81cdc733d3ac0f3496a88eebbed0a31478c403c6

$(document).ready(function() {
    $('#example').DataTable( {
        "ajax": 'gdp_main.json'
    } );
} );
