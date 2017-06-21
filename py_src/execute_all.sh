#!/bin/bash

#while true; do
#	[[ $(python 0_crawl doctor | tail -1) == "Crawling done." ]] && break
#done
while true; do
	[[ $(python 0_crawl faq | tail -1) == "Crawling done." ]] && break
done
python 1_parse
python 2_intermediate
python 31_pagerank
python 32_qscore
python 4_index
