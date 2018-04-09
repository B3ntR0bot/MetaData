from bs4 import BeautifulSoup, SoupStrainer
import requests
import requests.exceptions
from urlparse import urlsplit
from collections import deque
import re
import code
import argparse

#---------------Created By Flef -- BentRobotLabs
#---------------Date 2/22/2018


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-o', '--output',dest='output', help='Define path to output file')
	parser.add_argument('-m', dest='bad', action='store_true', help='Output only URLs of pages within domain, no broken links')
	parser.add_argument('-l', '--limit', dest='limit', help='limit search to the given domain instead of URL derived domain')
	parser.add_argument('-s', '--shell', dest='shell', action='store_true', help='Creates interactive python shell after ctrl-c')
	parser.add_argument('-d', '--depth', dest='depth', type=int, default=1, help='Depth of links to follow, default is 1')
	parser.add_argument('-a', '--all', dest='all', action='store_true', help='Turn on to save ALL good links regardless of domain')
	parser.add_argument(dest='url', help='Add url you want to find links of')
	args = parser.parse_args()

	if not str(args.output) in "None":
		file = open(str(args.output), "w")

	# Define a queue of urls to crawl through
	urls = deque([str(args.url)]) #always put a '/' after your link!!!
	
	# Define next depth of urls
	new_urls = deque([])
	
	# Keep urls we have already crawled through
	used_urls = set()
	
	# set of broken links
	broken = set()
	
	# Takes care of ctrl c by user. Placing interactive shell
	kill = 1
	
	# This defines how many iterations of "link follows" you want to do. (Only tested with 1)
	depth = args.depth
	depth_count = 0
	#Define Domain limitation
	if str(args.limit) in "None":
		domain = str(args.url)[10:]
	else:
		domain = str(args.limit)

	# Start processing URLS
	while len(urls) and kill and (depth>=0):
		
		try:
			#Move new url to processed url's
			url = urls.popleft()
			used_urls.add(url)
	
			#Extracting base url to resolve relative links
			parts = urlsplit(url)
			base_url = "{0.scheme}://{0.netloc}".format(parts)
			path = url[:url.rfind('/')+1] if '/' in parts.path else url
	
			#get url's content
			try:
				response = requests.get(url)
			except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
				#if url is broken add to broken url set, else continue
				if not url in broken:
					broken.add(url)
					if not str(args.output) in "None" and (args.bad == False):
						file.write("Bad -- %s\n" % url)
						print("Bad -- %s" % url)
				continue

			if not str(args.output) in "None":
				file.write("Good -- %s\n" % url)
			print("Good -- %s" % url)
	
			#create Beautiful Soup for html document
			soup = BeautifulSoup(response.text, 'lxml')
		
			#find and process all the anchors in the document
			for anchor in soup.find_all("a"):
				#extract link url from anchor
				link = anchor.attrs["href"] if "href" in anchor.attrs else ''
	
				#resolve relative links
				if link.startswith('/'):
					link = base_url + link
				elif not link.startswith('http'):
					link = path + link
	
				# save all links into new_urls queue
				if not link in urls and not link in used_urls and not link in new_urls:
					
					if domain in link:
						new_urls.append(link)

					continue
	
			if len(urls) == 0:
				depth -=  1
				#Copy new urls into urls queue
				while len(new_urls):
					temp = new_urls.popleft()
					urls.append(temp)
				
				print("Found New Links!!!! Depth = %i" % depth_count)
				depth_count += 1

		except KeyboardInterrupt:
			kill = 0
			if not str(args.output) in "None":
				file.close()
			if args.shell:
				code.interact(local=locals())

	print("\nGOod By3!!")
	if not str(args.output) in "None":
		file.close()
