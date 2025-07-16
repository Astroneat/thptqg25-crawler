import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import csv

region = '04'
num_ids = 14548

fieldnames = ["SBD", "Toán", "Ngữ văn", "Ngoại ngữ", "Lịch sử", "Địa lý", "Sinh học", "Vật lý", "Hóa học", "Tin học", "Công nghệ Công nghiệp", "Công nghệ Nông nghiệp", "Giáo dục kinh tế và pháp luật", "Giáo dục công dân"]

csvfile = open('results.csv', 'w+', newline='')
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

def search(start, end):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    for i in range(start, end):
        sbd = '\'' + region + '0' * (6 - len(str(i))) + str(i)
        url = f'https://diemthi.vnexpress.net/index/detail/sbd/{sbd}/year/2025'
        response = session.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            score_div = soup.find("div", {"class": "o-detail-thisinh__diemthi"})
            if score_div is None:
                print(sbd, ": NULL")
                continue
            scores_raw = score_div.find("table").find("tbody").find_all("tr")
            scores = {"SBD": sbd}
            for tr in scores_raw:
                tmp = tr.find_all("td")
                subject = tmp[0].text.strip()
                score = tmp[1].text.strip()
                scores[subject] = score

            print(scores)
            writer.writerow(scores)

def main():
    search(1, num_ids + 1)

if __name__ == '__main__':
    main()
