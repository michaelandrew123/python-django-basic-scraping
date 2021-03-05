from django.shortcuts import render 
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def home(request):
    context = {}    

    return render(request, './home.html', context)


def qoutes(request):
    context = {}
    URL = "http://www.values.com/inspirational-quotes"

    uClient = uReq(URL)
    page_html = uClient.read()
    uClient.close()
    
    page_soup = soup(page_html, "html.parser")

    table = page_soup.find('div', attrs = {'id':'all_quotes'})  

    context['quotes'] = []
    #qoutes = page_soup.findAll("div", {"class":"velaProBlock"}) 

    for row in table.findAll('div', attrs = {'class':'col-6 col-lg-3 text-center margin-30px-bottom sm-margin-30px-top'}): 
        # quote = {} 
        theme= row.h5.text 
        url = row.a['href'] 
        img = row.img['src'] 
        lines = row.img['alt'].split(" #")[0] 
        author = row.img['alt'].split(" #")[1] 

        context['quotes'].append({
            'theme': theme, 
            'url': url,
            'img': img,
            'lines': lines,
            'author': author
        }) 
 
    page = request.GET.get('page', 1)

    paginator = Paginator(context['quotes'], 8)
    
    try:
        context['quots_paginators'] = paginator.page(page)
    except PageNotAnInteger:
        context['quots_paginators'] = paginator.page(1)
    except EmptyPage:
        context['quots_paginators'] = paginator.page(paginator.num_pages)

    
 
    # context['paginator'] = paginator.count;
    
    return render(request, './quotes.html', context)


#     filename = 'inspirational_quotes.csv'
# with open(filename, 'w', newline='') as f: 
#     w = csv.DictWriter(f,['theme','url','img','lines','author']) 
#     w.writeheader() 
#     for quote in quotes: 
#         w.writerow(quote) 

def contact_view(request):
    context = {}
    
    return render(request, './contact.html', context)



def vitascribe(request):
    context = {}
    
    # context['message'] = "Hello home page!"

    my_url = "https://vitascribe.ca/collections/gluten-free"

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    
    page_soup = soup(page_html, "html.parser")
 

    velaProBlocks = page_soup.findAll("div", {"class":"velaProBlock"}) 
    # filename = "products.csv"

    # headers = "title\n"
    
    # f = open(filename, "w")

    # f.write(headers)
    context['messages']=[] 

    for velaproblock in velaProBlocks: 
        title = velaproblock.findAll('div', {"class":"proContent"})
        img = velaproblock.findAll('div', {"class":"proHImage"})
        # price = velaproblock.findAll('div', {"class":"proPrice"})

        product_img = img[0].a.img['src']
        product_title = title[0].h5.text.strip() 
        product_price = velaproblock.find(class_='proPrice').text.strip() 


        context['messages'].append({'product_img': product_img, 'product_name': product_title, 'price': product_price}) 




    
    page = request.GET.get('page', 1)

    paginator = Paginator(context['messages'], 8)
    
    try:
        context['message_paginators'] = paginator.page(page)
    except PageNotAnInteger:
        context['message_paginators'] = paginator.page(1)
    except EmptyPage:
        context['message_paginators'] = paginator.page(paginator.num_pages)

    


        # f.write(product_title.replace(",","|") + "\n") 
    # f.close() 

    return render(request, './vitascribe.html', context)
