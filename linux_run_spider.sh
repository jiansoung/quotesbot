#!/bin/sh

# Run sequential spiders.
# Usage: run_spider.sh [spider ...]

LOG_PATH=./log
RESULTS_PATH=./downloads/results

if [ ! -d $RESULTS_PATH ]; then
    mkdir -p $RESULTS_PATH
fi

if [ ! -d $LOG_PATH ]; then
    mkdir $LOG_PATH
fi

SPIDERS=$@
if [ $# -eq 0 ]; then
    SPIDERS=`scrapy list`
fi
echo `date`
for SPIDER in $SPIDERS; do
    echo "Spider \`$SPIDER\` starting ..."
    spider_id=$SPIDER-`date "+%Y%m%d%H%M%S"`
    fullcmd="scrapy crawl $SPIDER -o $RESULTS_PATH/$spider_id.json --logfile $LOG_PATH/$spider_id.log"
    echo "$fullcmd"
    $fullcmd
done

echo
echo `date`
echo 'All spiders have completed'
