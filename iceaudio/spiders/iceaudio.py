import scrapy
import re
import os
import pandas as pd


class IceSpider(scrapy.Spider):
    """This class performs the data scraping of IceAudio.no""" 

    name = "simple_ice_audio"
    allowed_domains = ["iceaudio.no"]
    start_urls = ["https://www.iceaudio.no/"]


    def parse(self, response):

        text = response.xpath('//ul[@id="treemenu1"]/li/a/text()').getall()
        anchors = response.xpath('//ul[@id="treemenu1"]/li/a/@href').getall()

        for count in range(0,len(anchors)):
            yield  response.follow  (anchors[count], 
                                     callback = self.parse_product,
                                     meta = {'Main_categories' : text[count]}
                                    )


    def parse_product(self, response):

        products = response.xpath('//div[@id="container"]//div[@id="sub_content"]//tr[1]/td/a/@href').getall()
        anchors = response.xpath("//div[@id='sub_content']//a/@href").getall()
        sub_category = []
        category = response.xpath("//div[@id='sub_content']//a/img/@alt").getall()
        for i in range(0,len(category)):
            
            if category[i].isdigit() or category[i] == "6,5" or category[i] == "6x9" or category[i] == "5,25" or category[i] == "18 - 33":
                sub_category.append(category[i]+'"')
            else:
                sub_category.append(category[i])

        if products:
            if products is not None:
                yield from response.follow_all  (
                            products,
                            callback = self.parse_product_scraping ,
                            dont_filter = True,
                            meta={
                            'Main_categories':response.meta.get('Main_categories')}
                                                )

        elif anchors:
            for count in range(0,len(anchors)):
                yield  response.follow  ( 
                    anchors[count],
                    callback=self.parse_product_item, 
                    meta={
                        'Main_categories':response.meta.get('Main_categories'),
                        'Category_1':sub_category[count]
                        }
                                        )


    def parse_product_item(self, response):
     
        anchors = response.xpath('//div[@id="container"]//div[@id="sub_content"]//tr[1]/td/a/@href').getall()
        yield from response.follow_all  (
            anchors,
            callback = self.parse_product_scraping ,
            dont_filter = True,
            meta={
                'Main_categories':response.meta.get('Main_categories'),
                'Category_1':response.meta.get('Category_1'),
                'Category_2':response.meta.get('Category_2')
                }
                                        )

        pagination_links = response.xpath('//div[@id="container"]/div[@id="left"]/div[@id="sub_content"]/a/@href').getall()
        category = response.xpath('//div[@id="container"]/div[@id="left"]/div[@id="sub_content"]/a/img/@alt').getall()
        sub_category = []
        for i in range(0,len(category)):

            try:
                
                if category[i].isdigit() or category[i] == "6,5" or category[i] == "6x9" or category[i] == "5,25" or category[i] == "18 - 33":
                    sub_category.append(category[i]+'"')
                else:
                    sub_category.append(category[i])

            except Exception as ex:
               sub_category.append(category[i])

        if pagination_links is not None:
            for counter in range(0,len(pagination_links)):
                yield  response.follow  (
                        pagination_links[counter], 
                        callback = self.parse_product_item,
                        meta={
                            'Main_categories':response.meta.get('Main_categories'),
                            'Category_1':response.meta.get('Category_1'),
                            'Category_2':sub_category[counter]
                            }
                                        )
            

    def parse_product_scraping(self, response):
         
        price=response.xpath("//div[@id='PInfo_Right']//tr[3]/td[@align='right']/text()").get()
        if price != None:
            product_images = []
            file_pdf = []
            images = []

            img =  response.xpath("//div[@id='PInfo_Left_bilder']/a/@href").getall()
            for i in img:

                try:
                    check_img = i.replace('./','http://iceaudio.no/',1)

                    if check_img.endswith(".jpg"):
                        images.append(check_img)
                    elif check_img.endswith(".pdf"):
                        file_pdf.append(check_img)

                except Exception as ex: 
                    print("Error")
            
            for i in range(0,17):

                try:
                    product_images.append(images[i])

                except Exception as ex: 
                    product_images.append("")

            brand_names = [
                '4 Connect',
                '4 Power',
                '4Connect',
                '4POWER',
                '5 Connect',
                'ACV',
                'ACX',
                'AH',
                'AI-SONIC',
                'Alpine',
                'Alpine',
                'Ampire',
                'Antenne (DAB)',
                'Antenne adapter',
                'Antennepisk',
                'Antennesplitter',
                'Asuka',
                'Audio/Video interface',
                'Audison',
                'Aura',
                'AutoDAB',
                'Axton',
                'BeatSonic',
                'BLACKVUE',
                'Blam',
                'Blam',
                'BLAM',
                'Blaupunkt',
                'BOSS',
                'Boss',
                'Brax',
                'Cadence',
                'Caliber',
                'CarAudio Systems',
                'CDS',
                'Cerwin Vega',
                'Clarion',
                'Comfort Modul',
                'ConnectED',
                'Connection',
                'Connects2',
                'Continental',
                'Crunch',
                'DAB integrering',
                'DAB-antenne',
                'DASHCAM',
                'DD Audio',
                'DEFA',
                'Dension',
                'Diamond Audio',
                'DIRECTOR',
                'Dynamat',
                'EMPHASER',
                'ESX',
                'Eton',
                'Fiamm',
                'Firefly',
                'Focal',
                'FOUR Audio',
                'FOUR Connect',
                'G4Audiio',
                'Garmin',
                'Gladen',
                'GLADEN',
                'Ground  Zero',
                'Ground Zero',
                'Halo',
                'Hardstone',
                'Harman/Kardon',
                'Helix',
                'HELIX Q',
                'Hertz',
                'Hertz Marine',
                'Hifonics',
                'In2digi',
                'JBL',
                'Jensen',
                'JL Audio',
                'JL Audio',
                'JVC',
                'JVC',
                'Kenwood',
                'Kicker',
                'Kicker',
                'Kram Telecom',
                'Kufatec',
                'Lukas',
                'MAGNAT',
                'Match',
                'MB Quart',
                'Metra',
                'MOSCONI',
                'MTX',
                'MTX Audio',
                'MUSWAY',
                'Nextbase',
                'NVX',
                'PAC',
                'PAC',
                'Parrot',
                'PEXMAN',
                'PhoenixGold',
                'Pioneer',
                'Polk Audio',
                'Power',
                'Prime',
                'Punch',
                'Pure',
                'Pyle',
                'QVIA',
                'Renegade',
                'RetroSound',
                'Roberts',
                'Rockford Fosgate',
                'Sangean',
                'Scosche',
                'Sony',
                'Sound Marine',
                'SounDigital',
                'Soundmagus',
                'SoundQubed',
                'SoundQuest',
                'Stinger',
                'Stinger',
                'Strands',
                'TARAMPS',
                'Teleskopantenne',
                'TFT',
                'Toma Carparts',
                'uniDAB',
                'VCAN',
                'Video in motion',
                'Xplore',
                'Xzent',
                'Zenec'
            ]
            
            heading= response.xpath("//div[@id='PInfo_Top']/h3/strong/text()").get()
            company_brand = ""
            for brand in brand_names:

                try:

                    if brand.upper() in heading.upper():
                        if brand:
                            company_brand = brand
                            break

                except Exception as ex:
                    company_brand = ""
                
            if response.meta.get('Main_categories') != "Biltilpasset":

                response_obj = dict({
                            "product Id" : response.xpath("//div[@id='PInfo_Right']//tr[1]/td[@align='right']/text()").get().strip(),
                            "Main Category" : response.meta.get('Main_categories'),
                            "Category 1" : response.meta.get('Category_1'),
                            "Category 2" : response.meta.get('Category_2'),
                            "Category 3" : "",
                            "Category 4" : "",
                            "Category 5" : "",
                            "Product Brand" :company_brand,
                            "Product Name" : response.xpath("//div[@id='PInfo_Top']/h3/strong/text()").get().strip(),
                            "Product Information" : response.xpath("//div[@id='PInfo_Top']/text()").get().replace("\r\n",'').strip(),
                            "url":response.url,
                            "Main Price" : response.xpath("//div[@id='PInfo_Right']//tr[3]/td[@align='right']/text()").get().strip(),
                            "Discount Price" : "",
                            "product Discription":response.xpath('//div[@id="PInfo"]//ul').get(),
                            "file pdf":file_pdf,
                            "source" : "www.iceaudio.no",
                    })

                for i in range(1, 18):
                    response_obj["Picture {}".format(i)] = product_images[i-1]
                
                yield response_obj

                