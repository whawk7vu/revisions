#Authors: Andrea Julca, William Hawk

library(data.table)
library(googleVis)
library(httr)
library(rvest)
library(RCurl)
library(gdata)

histUrl <- 'http://www.bea.gov/histdata/histChildLevels.cfm?HMI=7'

beaDescr <- read_html(histUrl) %>%
  html_nodes('table') %>%
    html_table()



beaLinks <- read_html(histUrl) %>%
  html_nodes('a') %>%
    html_attr('href')

cleanLinks <- paste0(
  'http://www.bea.gov/histdata/',
  beaLinks[
    grepl('HMI=7', beaLinks, fixed = TRUE)
  ]
)

library(parallel)

cl <- makePSOCKcluster(detectCores(), timeout=360000)

clusterEvalQ(cl, library(rvest))
clusterEvalQ(cl, library(gdata))
clusterEvalQ(cl, library(data.table))
clusterEvalQ(cl, library(readxl))

clusterExport(cl, c('cleanLinks'))

histUrls <- parLapply(cl, cleanLinks, function(url){
  thisPg <- read_html(url) %>%
    html_nodes('a') %>%
      html_attr('href')
  url <- paste0(
    'http://www.bea.gov',
    thisPg[grepl(
      toupper('/Section1all_xls'),
      toupper(thisPg),
      fixed=T
    )]
  )
  #thisDF <- read.xls(url)
  return(url)
})

goodUrls <- unlist(histUrls[
  grepl(
    'Releases',
    unlist(histUrls),
    fixed = TRUE
  )])

clusterExport(cl, c('goodUrls'))


histData <- parLapply(cl, 1:length(goodUrls),
  function(urlNo){
  #urlNo <- 43
    temp <- paste0('C:/Users/Swan/Documents/histData',
      urlNo,
      '.xls'
    );
    ##NOTE: MUST UNSUPPRESS IF NEED TO DOWNLOAD
    if(urlNo < 166){
      download.file(
        goodUrls[urlNo],
        temp,
        mode = 'wb'
      );
    }

  }
)

