import requests
from bs4 import BeautifulSoup
import json

def parse_wildberries_product(url):
    headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
     "Access-Control-Allow-Credentials": "true",
 "Access-Control-Allow-Headers":"Authorization,Accept,Origin,DNT,User-Agent,Content-Type,Wb-AppType,Wb-AppVersion,Xwbuid,Site-Locale,X-Clientinfo,Storage-Type,Data-Version,Model-Version,__wbl, x-captcha-id",
 "Access-Control-Allow-Methods":"GET,OPTIONS",
 "Access-control-Allow-Origin":"https://www.wildberries.ru",
 "Content-Encoding":"gzip",
 "Content-Type":"application/json charset=utf-8"
 }
    
    try:
        # Получаем HTML страницы
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем JSON-данные с информацией о товаре
        script_tag = soup.find('script', {'type': 'application/ld+json'})
        if not script_tag:
            return {"error": "Product data not found"}
        
        product_data = json.loads(script_tag.string)
        
        # Извлекаем основную информацию
        result = {
            'name': product_data.get('name', ''),
            'brand': product_data.get('brand', {}).get('name', ''),
            'description': product_data.get('description', ''),
            'price': product_data.get('offers', {}).get('price', ''),
            'price_currency': product_data.get('offers', {}).get('priceCurrency', ''),
            'availability': product_data.get('offers', {}).get('availability', ''),
            'url': product_data.get('url', ''),
            'image': product_data.get('image', ''),
            'sku': product_data.get('sku', ''),
            'rating': product_data.get('aggregateRating', {}).get('ratingValue', ''),
            'review_count': product_data.get('aggregateRating', {}).get('reviewCount', '')
        }
        
        # Дополнительная информация из других тегов
        seller_info = soup.find('span', {'class': 'seller-info__name'})
        if seller_info:
            result['seller'] = seller_info.get_text(strip=True)
        
        # Цена со скидкой (если есть)
        final_price = soup.find('ins', {'class': 'price-block__final-price'})
        if final_price:
            result['final_price'] = final_price.get_text(strip=True)
        
        # Старая цена (если есть скидка)
        old_price = soup.find('del', {'class': 'price-block__old-price'})
        if old_price:
            result['old_price'] = old_price.get_text(strip=True)
        
        return result
    
    except Exception as e:
        return {"error": str(e)}

# Пример использования
if __name__ == "__main__":
    product_url = "https://www.wildberries.ru/catalog/10321375/detail.aspx"
    product_info = parse_wildberries_product(product_url)
    print(json.dumps(product_info, indent=2, ensure_ascii=False))