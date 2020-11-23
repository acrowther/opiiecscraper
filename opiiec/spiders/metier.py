# -*- coding: utf-8 -*-
import scrapy


class MetierSpider(scrapy.Spider):
    name = 'metier'
    allowed_domains = ['opiiec.fr']
    ids=[60501, 60501, 60566, 60566, 60604, 60604, 60486, 60486, 60559, 60559, 61330, 61330, 60581, 60581, 60609, 60609, 60597, 60597, 60488, 60488, 60538, 60538, 60547, 60547, 60602, 60602, 60555, 60555, 60553, 60553, 60592, 60592, 60587, 60587, 60590, 60590, 60577, 60577, 60611, 60611, 60557, 60557, 60550, 60550, 60543, 60543, 60533, 60533, 60617, 60617, 60473, 60473, 60563, 60563, 60515, 60515, 60598, 60598, 61122, 61122, 60528, 60528, 60455, 60455, 60462, 60462, 60505, 60505, 60461, 60461, 60601, 60601, 60870, 60870, 60614, 60614, 60606, 60606, 60497, 60497, 60467, 60467, 60466, 60466, 60551, 60551, 60565, 60565, 60608, 60608, 60458, 60458, 60576, 60576, 60459, 60459, 60616, 60616, 60531, 60531, 60572, 60572, 60454, 60454, 60539, 60539, 60580, 60580, 60485, 60485, 60535, 60535, 60472, 60472, 60568, 60568, 60569, 60569, 60480, 60480, 60526, 60526, 60596, 60596, 60544, 60544, 60509, 60509, 60582, 60582, 60558, 60558, 60527, 60527, 60477, 60477, 60478, 60478, 60450, 60450, 60465, 60465, 60471, 60471, 60451, 60451, 60463, 60463, 60540, 60540, 60449, 60449, 60464, 60464, 60470, 60470, 60554, 60554, 60546, 60546, 60595, 60595, 60487, 60487, 60492, 60492, 60457, 60457, 60490, 60490, 60507, 60507, 60579, 60579, 60548, 60548, 60594, 60594, 60481, 60481, 60562, 60562, 60525, 60525, 60600, 60600, 60469, 60469, 60453, 60453, 60529, 60529, 60483, 60483, 60452, 60452, 60567, 60567, 60468, 60468, 60456, 60456, 60484, 60484, 60534, 60534, 60508, 60508, 60573, 60573, 60612, 60612, 60447, 60447, 60493, 60493, 60489, 60489, 60460, 60460, 60545, 60545, 60496, 60496, 60495, 60495, 60560, 60560, 60542, 60542, 60561, 60561, 60871, 60871, 60513, 60513, 60603, 60603, 60504, 60504, 60482, 60482, 60494, 60494, 60523, 60523, 60502, 60502, 60503, 60503, 60584, 60584, 60518, 60518, 60520, 60520, 60552, 60552, 60549, 60549, 60615, 60615, 60448, 60448, 60588, 60588, 60491, 60491, 60536, 60536, 60506, 60506, 60479, 60479, 60570, 60570, 60537, 60537, 60607, 60607, 60591, 60591, 60599, 60599, 60476, 60476, 60578, 60578, 60586, 60586, 60474, 60474, 60500, 60500, 60585, 60585, 60516, 60516, 60475, 60475, 60575, 60575, 60571, 60571, 60541, 60541, 60510, 60510, 60499, 60499, 60511, 60511, 60498, 60498, 60524, 60524, 60514, 60514, 60605, 60605, 60593, 60593, 60530, 60530, 60610, 60610, 60556, 60556, 60574, 60574, 60583, 60583, 60589, 60589, 60521, 60521, 60522, 60522, 60519, 60519, 60517, 60517, 60613, 60613, 60512, 60512, 60564, 60564, 60532, 60532]
    #ids=[60525]
    start_urls = [f'https://www.opiiec.fr/metiers/{id}' for id in ids]

    def parse(self, response):
        famille=response.xpath('//*[@id="info-family"]/text()').get()
        activitesprincipales=response.xpath('//*[@id="collapsePActivity"]/div/ul/li/text()').getall() 
        tailleentreprisesquirecrutent=response.xpath('//*[@id="doughnut4"]/text()').get().split('/')
        tailleentreprisesquirecrutent=[{'name':t.split(':')[0].strip(), 'value':int(t.split(':')[1].strip())} for t in tailleentreprisesquirecrutent]
        metiersproches=[{'ordre':metier.xpath('@data-colonne').get(), 'nom':metier.xpath('@title').get()} for metier in response.xpath('//div[@class="plumb-container"]/div')]
        certifications=response.xpath('//*[@id="collapseCertifications"]/div/div/a/text()').getall()      
        competences=[

        ]
        for tr in response.xpath('//*[@id="collapseTransversalSkills"]/tr'):
            titre=tr.xpath('./td[1]/text()').get()    
            niveau=tr.xpath('./td[2]/span[1]/@title').re_first('\d')  
            description=tr.xpath('./td[3]/p/text()').get()          
            competences.append({'titre':titre,'niveau':int(niveau), 'description':description})
        experience=response.xpath('//*[@id="collapseRequirements"]/div/p[1]/text()').get()   
        offres=int(''.join(response.xpath('//*[@id="bande01"]/div[1]/div/div[1]/div/div[2]/text()').re('\d'))) 
        formations=response.xpath('//*[@id="collapseFormations"]/div/text()').get().split('\n')    
        formations=[f.strip() for f in formations if len(f.strip())>0] 
        
        return {'formations':formations, 'experience':experience,'offres':offres,'competences':competences,'famille':famille, 'activitesprincipales':activitesprincipales,'tailleentreprisesquirecrutent':tailleentreprisesquirecrutent,'metiersproches':metiersproches}