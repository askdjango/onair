import re
from urllib.parse import urljoin
import mechanicalsoup

browser = mechanicalsoup.Browser()

list_url = 'http://e-childschoolinfo.moe.go.kr/kinderMt/combineFind.do'
list_page = browser.get(list_url)

form_tag = list_page.soup.select('form#noticeSearch')[0]
# form_tag['action'] = urljoin(list_url, '/kinderMt/kinderSummary.do')        # 요약
form_tag['action'] = urljoin(list_url, '/kinderMt/kinderChildAndStaff.do')  # 영유아 및 교직원

for a_tag in form_tag.select('a[href*=fn_detail]'):
    url = a_tag['href']
    matched = re.search(r'([0-9a-z-]{36})', url)
    if not matched:
        continue

    name = a_tag.text.strip()
    id = matched.group(1)

    form_tag.select('input[name=ittId]')[0]['value'] = id
    detail_page = browser.submit(form_tag)
    print(name, id)
    open('crawl-{}.html'.format(name), 'w').write(detail_page.text)

