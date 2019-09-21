from bs4 import BeautifulSoup
import requests
import re

def get_sustainability_data(ticker):
    if type(ticker) != str:
        raise TypeError('The only valid type is string.')
    ticker = ticker.upper()
    link = 'https://finance.yahoo.com/quote/' + ticker + '/sustainability?p=' + ticker
    """
    GOVERNANCE TOTAL
    <div class="Fz(36px) Fw(600) D(ib) Mend(5px)" data-reactid="20">48</div>
    
    ENVIRONMENT
    <div class="D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)" data-reactid="35">36</div>
    
    SOCIAL
    <div class="D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)" data-reactid="45">47</div>
    
    GOVERNANCE
    <div class="D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)" data-reactid="55">69</div>
    
    CONTROVERSY
    <div class="D(ib) Fz(36px) Fw(500)" data-reactid="133">1</div>
    
    GOVERNANCE TOTAL PERCENTILE
    <span class="Bdstarts(s) Bdstartw(0.5px) Pstart(10px) Bdc($c-fuji-grey-c) Fz(12px) smartphone_Fz(10px) smartphone_Bd(n) Fw(500)" data-reactid="22"><span data-reactid="23">21st percentile</span></span>   
     
    ENVIRONMENT PERCENTILE
    <span class="Bdstarts(s) Bdstartw(0.5px) Pstart(5px) Mstart(5px) smartphone_Mstart(0px) smartphone_Pstart(0px) Bdc($c-fuji-grey-c) Fz(12px) smartphone_Fz(10px) smartphone_Bd(n) Fw(500)" data-reactid="37"><span data-reactid="38">3rd percentile</span></span>
    
    SOCIAL PERCENTILE
    <span class="Bdstarts(s) Bdstartw(0.5px) Pstart(5px) Mstart(5px) smartphone_Mstart(0px) smartphone_Pstart(0px) Bdc($c-fuji-grey-c) Fz(12px) smartphone_Fz(10px) smartphone_Bd(n) Fw(500)" data-reactid="47"><span data-reactid="48">29th percentile</span></span>
     
    GOVERNANCE PERCENTILE
    <span class="Bdstarts(s) Bdstartw(0.5px) Pstart(5px) Mstart(5px) smartphone_Mstart(0px) smartphone_Pstart(0px) Bdc($c-fuji-grey-c) Fz(12px) smartphone_Fz(10px) smartphone_Bd(n) Fw(500)" data-reactid="57"><span data-reactid="58">66th percentile</span></span>
    
     """
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')


    results = {}
    category_names = ['Environment', 'Social', 'Governance']
    names = ['Environment Score', 'Social Score', 'Governance Score']
    pgov = []
    esg = []

    gov_percentile_data = soup.find_all(class_='Bdstarts(s) Bdstartw(0.5px) Pstart(10px) Bdc($c-fuji-grey-c) Fz(12px) smartphone_Fz(10px) smartphone_Bd(n) Fw(500)')
    gov_percentile = re.findall(r"data-reactid=\"22\"><span data-reactid=\"23\">(.*)</span></span>", str(gov_percentile_data))
    for j in range(len(gov_percentile[0])):
        if gov_percentile[0][j] not in '0123456789':
            pgov.append(gov_percentile[0][:j])
            break

    gov_total = soup.find(class_='Fz(36px) Fw(600) D(ib) Mend(5px)')

    gov_score = re.match(r"<div class=\"Fz\(36px\) Fw\(600\) D\(ib\) Mend\(5px\)\" data-reactid=(.*)</div>", str(gov_total))
    gov_score_re = gov_score.group(1)

    for k in range(len(gov_score_re)):
        if gov_score_re[k] == '>':
            results.update({"ESG": [{"ESG Score": int(gov_score_re[k + 1:])}, {"Percentile" : int(pgov[0])}]})

    esg_scores = soup.find_all(class_='D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)')
    esg_percentiles = soup.find_all(class_='Bdstarts(s) Bdstartw(0.5px) Pstart(5px) Mstart(5px) smartphone_Mstart(0px) smartphone_Pstart(0px) Bdc($c-fuji-grey-c) Fz(12px) smartphone_Fz(10px) smartphone_Bd(n) Fw(500)')

    for rating in range(len(esg_scores)):
        score = re.match(r"<div class=\"D\(ib\) Fz\(23px\) smartphone_Fz\(22px\) Fw\(600\)\" data-reactid=(.*)</div>", str(esg_scores[rating]))
        percentile = re.match(r"<span class=\"Bdstarts\(s\) Bdstartw\(0\.5px\) Pstart\(5px\) Mstart\(5px\) smartphone_Mstart\(0px\) smartphone_Pstart\(0px\) Bdc\(\$c-fuji-grey-c\) Fz\(12px\) smartphone_Fz\(10px\) smartphone_Bd\(n\) Fw\(500\)\" data-reactid=(.*)</span></span>", str(esg_percentiles[rating]))
        score_re = score.group(1)
        percentile_re = percentile.group(1)
        for x in range(len(score_re)):
            if score_re[x] == '>':
                esg.append({names[rating]: int(score_re[x + 1:])})
        for y in range(len(percentile_re)):
            if percentile_re[y] == '>':
                p_slc = percentile_re[y + 1:]
                for v in range(len(p_slc)):
                    if p_slc[v] not in '0123456789':
                        esg.append({'Percentile' : p_slc[:v]})
                        break
        esg.pop(1)
        results.update({category_names[rating] : esg})
        esg = []

    controversy = soup.find_all(class_='D(ib) Fz(36px) Fw(500)')
    controversy_score = re.findall(r"<div class=\"D\(ib\) Fz\(36px\) Fw\(500\)\" data-reactid=\"133\">(.*)</div>", str(controversy))
    results.update({"Controversy Score": int(controversy_score[0])})

    return results

def get_profile_data(ticker):
    if type(ticker) != str:
        raise TypeError('The only valid type is string.')
    url = 'https://finance.yahoo.com/quote/' + ticker + '/profile?p=' + ticker

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    raw_data = []
    results = {}

    executives = soup.find_all(class_="C($primaryColor) BdB Bdc($seperatorColor) H(36px)")

    for i in range(len(executives)):
        execs = re.findall(r"-->(.*)<!--", str(executives[i]))
        raw_data.append(execs)
    print(raw_data)

    """
    EXECUTIVES
    <tr class="C($primaryColor) BdB Bdc($seperatorColor) H(36px)" data-reactid="50">"
    
    """

get_profile_data('IT')