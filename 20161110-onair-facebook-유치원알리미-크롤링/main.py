import re
from urllib.parse import urljoin
import mechanicalsoup

browser = mechanicalsoup.Browser()

list_url = 'http://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do'
list_page = browser.get(list_url)

form_tag = list_page.soup.select('form#noticeSearch')[0]
form_tag['action'] = urljoin(list_url, '/kinderMt/kinderSummary.do')        # 요약
# form_tag['action'] = urljoin(list_url, '/kinderMt/kinderChildAndStaff.do')  # 영유아 및 교직원

for tr_tag in form_tag.select('table tbody tr'):
    try:
        detail_a_tag = tr_tag.select('a[href*=fn_detail]')[0]
        map_a_tag = tr_tag.select('a[href*=fn_panTo]')[0]
    except IndexError:
        continue

    # "javascript:fn_panTo(0, 35.2377227705893, 129.015079597986)"
    map_js_url = map_a_tag['href']
    matched = re.search(r'javascript:fn_panTo\(\d+,\s*([\d\.-]+),\s*([\d\.-]+)\)', map_js_url)
    if not matched:
        continue
    lat, lng = matched.groups()

    detail_js_url = detail_a_tag['href']
    matched = re.search(r'([0-9a-f-]{36})', detail_js_url)
    if not matched:
        continue

    name = detail_a_tag.text.strip()
    id = matched.group(1)

    form_tag.select('input[name=ittId]')[0]['value'] = id
    detail_page = browser.submit(form_tag)
    # detail_page.text  # 응답 html, 유니코드
    # detail_page.soup  # beautifulsoup4 인스턴스
    print(name, id, lat, lng)
    open('crawl-{}.html'.format(name), 'w').write(detail_page.text)

