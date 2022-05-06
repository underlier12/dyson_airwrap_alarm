from bs4 import BeautifulSoup

import requests

class CargoStatus:
    URL = "https://www.dyson.co.kr/products/hair-care/airwrap/shop-all"

    def __init__(self):
        self.CODE_TABLE = {
            "309796-01": "다이슨 에어랩™ 스타일러 볼륨 앤 쉐이프",
            "310737-01": "다이슨 에어랩™ 스타일러 컴플리트(니켈/푸시아)",
            "333121-01": "다이슨 에어랩™ 스타일러 컴플리트(블랙/퍼플)",
            "371717-01": "다이슨 에어랩™ 스타일러 컴플리트 롱",
            "335314-01": "다이슨 에어랩™ 스타일러 커스텀 블랙/퍼플 (*5개 스타일링 툴 선택)",
            "335311-01": "다이슨 에어랩™ 스타일러 커스텀 니켈/푸시아 (*5개 스타일링 툴 선택)"
        }
        self.inventory = {
            "309796-01": "Close",
            "310737-01": "Close",
            "333121-01": "Close",
            "371717-01": "Close",
            "335314-01": "Close",
            "335311-01": "Close"
        }
    
    def _extract_info(self, card_list):
        alert_candidate = []
        for card in card_list:
            card_id = card['id']
            card_action_open = card.find('div', {'class': 'card__action'})
            card_action_close = card.find('div', {'class': 'card__action__items'})

            if card_action_open != None:
                candidate = self._compare_open(card_id, card_action_open)
                alert_candidate.append(candidate)
            
            if card_action_close != None:
                candidate = self._compare_close(card_id, card_action_close)
                alert_candidate.append(candidate)

        return alert_candidate

    def _compare_open(self, card_id, card_action_open):
        try:
            card_action_text = card_action_open.div.form.button.span.text
        except:
            return "Error - transforming card action text at open"
        
        if "장바구니" in card_action_text:
            if self.inventory[card_id] != "Open":
                self.inventory[card_id] = "Open"
                return f"{self.CODE_TABLE[card_id]} - Open"

    def _compare_close(self, card_id, card_action_close):
        try:
            card_action_text = card_action_close.a.span.text
        except:
            return "Error - transforming card action text at close"
        
        if "입고 알림" in card_action_text:
            if self.inventory[card_id] != "Close":
                self.inventory[card_id] = "Close"
                return f"{self.CODE_TABLE[card_id]} - Close"

    def check_inventory(self):
        res = requests.get(self.URL)
        if res.status_code == 200:
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')
            card_list = soup.select('.slider__item')
            alert_candidate = self._extract_info(card_list)
            print(alert_candidate)
            return alert_candidate
