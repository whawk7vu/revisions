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
    if(urlNo > 163){
      download.file(
        goodUrls[urlNo],
        temp,
        mode = 'wb'
      );
    }

    thisDF <- ifelse(
      "10105 Qtr" %in% readxl::excel_sheets(temp),
      #readxl::read_excel(temp, sheet="10105 Qtr", skip = 8),
      #readxl::read_excel(temp, sheet="101 Qtr", skip = 8)
      gdata::read.xls(file.path(temp), sheet="10105 Qtr", header = FALSE, perl = 'C:\\Users\\Swan\\Documents\\Strawberry\\perl\\bin\\perl.exe'),
      #gdata::read.xls(file.path(temp), sheet="10105 Qtr"),
      gdata::read.xls(file.path(temp), sheet="101 Qtr", header = FALSE, perl = 'C:\\Users\\Swan\\Documents\\Strawberry\\perl\\bin\\perl.exe')
      )

    thisDFmeta <- try(ifelse(
      "10105 Qtr" %in% readxl::excel_sheets(temp),
      readxl::read_excel(temp, sheet="10105 Qtr", col_names = FALSE),
      readxl::read_excel(temp, sheet="101 Qtr", col_names = FALSE)
      ))

    #  attributes(thisDF)$metadata <- thisDFmeta[[1]][1:6]

    return(thisDF)
  }
)

save(list = c('histData', 'goodUrls'), file = 'C:/Users/Swan/Documents/beaData.RData')
#load('C:/Users/Swan/Documents/beaData.RData')

stopCluster(cl)

metadata <- fread('C:/users/swan/OneDrive/econ_projects/revisions/urls.csv')

beaData <- lapply(
    1:length(goodUrls),
    function(tabNo) {
      filePath <- paste0(
        'C:/Users/Swan/OneDrive/econ_projects/revisions/GDP',
        tabNo,
        '.csv'
      );

      #Read Data
      thisData <- fread(filePath, drop = 1, header = TRUE);

      #Get names as numeric, add .1 qtr
      theseNames <- as.numeric(
        attributes(thisData)$names
      ) + 0.1


      #Sub in names turned to NA by as.numeric
      theseNames[is.na(theseNames)] <- attributes(thisData)$names[is.na(theseNames)]

      #Rename Unnameds
      if("Unnamed: 0" %in% attributes(thisData)$names){
        theseNames <- gsub('Unnamed: 0', 'LineDescription', theseNames, fixed = TRUE)
      } else {
        theseNames <- gsub('Unnamed: 1', 'LineDescription', theseNames, fixed = TRUE)
      }

      theseNames <- gsub('Unnamed: 2', 'SeriesCode', theseNames, fixed = TRUE)

      #Set col names
      attributes(thisData)$names <- theseNames

      theseNames <- as.numeric(
        attributes(thisData)$names
      )

      lastQ <- max(theseNames[!is.na(theseNames)])
      firstQ <- min(theseNames[!is.na(theseNames)])

      if(lastQ < 2015.4){
      lapply(floor(lastQ):2015, function(yr){
        lapply(1:4, function(qtr){
          if (!(as.numeric(paste0(yr, '.', qtr)) %in% theseNames)){
            evalStr <- paste0('thisData[ , `', yr, '.', qtr, '`:= NA]')
            eval(parse(text=evalStr))
          }
          })
        })
      }

      if(firstQ > 1947.1){
      lapply(1947:floor(firstQ-1), function(yr){
        lapply(1:4, function(qtr){
          if (!(as.numeric(paste0(yr, '.', qtr)) %in% theseNames)){
            evalStr <- paste0('thisData[ , `', yr, '.', qtr, '`:= NA]')
            eval(parse(text=evalStr))
          }
          })
        })
      }

      return(thisData)
    }
  )

  beaAll <- rbindlist(beaData, fill = TRUE, use.names = TRUE)

  beaAll[, pdate := as.Date(date_pub, 'Data published %B %d, %Y')]

  metadata[, pdate := as.Date(date, '%B-%d-%Y')]

  beaAll[, pmy := format(pdate, '%Y%m')]

  metadata[, pmy := format(pdate, '%Y%m')]

  data.table::setkey(metadata, key=pmy)

  data.table::setkey(beaAll, key=pmy)


  beaRev <- beaAll[metadata]

  beaAdv <- beaRev[est == 'ADVANCE']
  data.table::setkey(beaAdv, key = year, quarter, SeriesCode)

  beaSec <- beaRev[est == 'SECOND' | est == 'PRELIMINARY']
  data.table::setkey(beaSec, key = year, quarter, SeriesCode)

  beaThr <- beaRev[est == 'THIRD' | est == 'FINAL']
  data.table::setkey(beaThr, key = year, quarter, SeriesCode)

  beaDiff <- beaThr[beaAdv]
  data.table::setkey(beaDiff, key=SeriesCode)
beaQtrsA <- attributes(beaAdv)$names
beaQtrsS <- attributes(beaSec)$names
beaQtrsT <- attributes(beaThr)$names

  beaQtrs <- beaQtrsA[!is.na(as.numeric(beaQtrsA))]


test<- lapply(
  unique(beaAdv[,paste0(year, quarter)]),
  function(qtr){
    thisCol <- gsub('Q', '.', qtr);
    #x <- lapply(unique(beaAdv[, SeriesCode]), function(thisCode){
      y <- eval(
        parse(
          text = paste0(
            'beaAdv[SeriesCode == \"', thisCode,
            '\"',',`', thisCol,'`]')
        )
      )
      return(y)
    });
  return(x)
  }
)

  diffCatcher <- lapply(beaQtrs, function(qtr) {
    eval(
      parse(
#   print(paste0(
        text=paste0(
          'beaDiff[, diff.',
          qtr,
          ' := as.numeric(gsub(',
          '\"',
          ',',
          '\"',
          ',',
          '\"',
          '\"',
          ',',
          qtr ,
          ',fixed=TRUE))-as.numeric(gsub(",","",i.',
          qtr,
          ', fixed = TRUE))]'
        )
      )
    )

  })



  allColNames <- attributes(beaDiff)$names
  diffCols <- allColNames[grep('diff', allColNames)]
  colsToUse <- c('Line', 'LineDescription', 'SeriesCode', diffCols)

  #save(list = c('metadata', 'goodUrls', 'beaData', 'beaAll'), file = 'C:/Users/Swan/Documents/bea.RData')
  #load('C:/Users/Swan/Documents/bea.RData')



  seriesDiff <- lapply(unique(beaDiff[,SeriesCode]), function(code){
    revDF <- as.data.frame(beaDiff[SeriesCode == code])[diffCols]
#    y <- beaDiff[SeriesCode == code];
    return(revDF);
  })

  attributes(seriesDiff)$names <- unique(beaDiff[,SeriesCode])

#Vis demo
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
