#Authors: Andrea Julca, William Hawk

library(data.table)
library(googleVis)
library(httr)
library(rvest)

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

histPg <- content(GET(histUrl), as = 'text')

beaLines <- strsplit(histPg, '<')[[1]]


beaLinks <- beaLines[
    grepl('a href=', beaLines, fixed = TRUE),
]

xlsLinks <- beaLinks[grepl('HMI=7', beaLinks, fixed = TRUE)]



 strsplit(
  as.character(
    beaLinks[grepl('HMI=7', beaLinks, fixed = TRUE)]
  ),
  '\'
  )

'http://www.bea.gov/histdata/'

#beaLinks <- #paste0(
#  #'http://www.bea.gov/histdata/',
#  #strsplit(
#    beaLines[
#      grepl('a href=', beaLines, fixed = T)
#    ]#,
#    #'\')[[1]]
#    #)


myData <- read.csv2('C:/users/swan/documents/output2.csv', sep = ',')



myDF <- data.frame(
  sapply(
    myData, as.character
  ),
  stringsAsFactors = F
)

beaDT <- as.data.table(myDF)
beaDT[, RIL := as.numeric(diff_1to3)]

gCols <- gvisColumnChart(
  as.data.frame(
    beaDT[TimePd >= '1977 Q1']
  ),
  yvar='RIL',
  xvar = 'TimePd'
)
plot(gCols)

beaDT[, Qtr := as.numeric(
  gsub(' Q', '.', TimePd, fixed=TRUE)
)]

gDots <- gvisScatterChart(
   as.data.frame(
     beaDT[Qtr >= 1977.1, .(Qtr, RIL) ]
   ),
)
plot(gDots)

sink('C:/users/Swan/Documents/gDots.html')
gDots
sink()
