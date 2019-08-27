from bs4 import BeautifulSoup
import requests
import time
import csv

class Product():
	def __init__(self,typee,name,promo,cur_price,shipping,moneysaved,percentsaved,total,link): #COMMENT THE PROGRAM
		self.typee = typee
		self.name = name
		self.promo = promo
		self.cur_price = cur_price
		self.shipping = shipping
		self.moneysaved = moneysaved
		self.percentsaved = percentsaved 
		self.total = total
		self.link = link

def mergeSort(arr): 
	if len(arr) >1: 
		mid = len(arr)//2 #Finding the mid of the array 
		L = arr[:mid] # Dividing the array elements 
		R = arr[mid:] # into 2 halves 

		mergeSort(L) # Sorting the first half 
		mergeSort(R) # Sorting the second half 

		i = j = k = 0
		
		# Copy data to temp arrays L[] and R[] 
		while i < len(L) and j < len(R): 
			if L[i].percentsaved < R[j].percentsaved: 
				arr[k] = L[i] 
				i+=1
			else: 
				arr[k] = R[j] 
				j+=1
			k+=1
		
		# Checking if any element was left 
		while i < len(L): 
			arr[k] = L[i] 
			i+=1
			k+=1
		
		while j < len(R): 
			arr[k] = R[j] 
			j+=1
			k+=1
file = 'products.csv'
f = open(file,'w')
columns = 'Type, Name, Percent Saved, Total Cost, Money Saved, Price, Shipping, Promo, Link\n'
f.write(columns)
products = []
links = {
	'https://www.newegg.ca/p/pl?N=100007670%208000&ActiveSearchResult=True&order=BESTMATCH&Order=BESTMATCH':'CPU',
	'https://www.newegg.ca/p/pl?N=100007708%208000&d=gpu':'GPU',
	'https://www.newegg.ca/Store/EventSaleStore/ID-2041598?cm_sp=SubCat_Desktop-Graphics-Cards-_-vga%252f17-3569-_-%2f%2fpromotions.newegg.ca%2fvga%2f17-3569%2f160x360.jpg&icid=398368':'GPU',
	'https://www.newegg.ca/p/pl?d=ram&N=100007610&name=Desktop%20Memory&isdeptsrh=1':'RAM'	
}
for linktosite, typeofproduct in links.items():
	site = requests.get(linktosite).text
	soup = BeautifulSoup(site, 'lxml')

	for item in soup.find_all('div',class_='item-container'):
		try:
			iteminfo = item.find('div',class_='item-info')
			name = iteminfo.find('a', class_ ='item-title')
			promo = iteminfo.p
			price = iteminfo.find('div', class_='item-action') 
			price = price.ul
			pricecurrent = price.find('li', class_='price-current')
			shipping = price.find('li',class_='price-ship')
			shipping = shipping.text.strip()
			shipping = shipping.replace(' Shipping','')
			if(shipping == 'Free'):
				shipping = 0.0
			else:
				shipping = float(shipping.replace('$',''))
			try:
				moneysaved = float(price.li.span.text.replace(',','')) - float((pricecurrent.strong.text+pricecurrent.sup.text).replace(',',''))
			except:
				moneysaved = 0.0
			try:
				percentsaved = price.find('span',class_='price-save-percent').text
				percentsaved = percentsaved.replace('%','')
				percentsaved = int(percentsaved)
			except:
				percentsaved = 0
			total = float((pricecurrent.strong.text+pricecurrent.sup.text).replace(',',''))+shipping
			link = item.a['href']
			x = Product(typeofproduct,name.text,promo.text,pricecurrent.strong.text+pricecurrent.sup.text,shipping,moneysaved,percentsaved,total,link)
			products.append(x)
		except:
			pass
		
	time.sleep(3)
mergeSort(products)

for y in range(len(products)-1,-1,-1):
	f.write(products[y].typee + ',' + products[y].name.replace(',','|') + ',' 
			+ str(products[y].percentsaved) + ',' + str(products[y].total) + ',' 
			+ str(products[y].moneysaved) + ',' + str(products[y].cur_price).replace(',','') + ',' 
			+ str(products[y].shipping) + ',' + products[y].promo.replace(',',' ') + ',' + products[y].link + '\n')
f.close()

