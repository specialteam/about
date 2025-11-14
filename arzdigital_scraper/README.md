# ArzDigital Cryptocurrency Scraper

یک اسکرپر حرفه‌ای برای استخراج اطلاعات ارزهای دیجیتال از سایت ArzDigital.com

## ویژگی‌ها

- ✅ اسکرپینگ بدون نیاز به مرورگر (headless)
- ✅ شبیه‌سازی رفتار کاربر واقعی با User-Agent های متنوع
- ✅ پشتیبانی از صفحه‌بندی (Pagination)
- ✅ مدیریت خطا و تلاش مجدد (Retry Logic)
- ✅ تاخیر تصادفی بین درخواست‌ها (Rate Limiting)
- ✅ ذخیره‌سازی در فرمت JSON و CSV
- ✅ لاگ‌گیری کامل از عملیات
- ✅ ساختار شی‌گرا و حرفه‌ای

## پیش‌نیازها

- Python 3.7 یا بالاتر
- pip (مدیریت بسته‌های Python)

## نصب

### 1. کلون کردن پروژه

```bash
cd arzdigital_scraper
```

### 2. نصب کتابخانه‌های مورد نیاز

```bash
pip install -r requirements.txt
```

یا نصب دستی:

```bash
pip install requests beautifulsoup4 lxml
```

## استفاده

### اجرای ساده

برای اسکرپ کردن صفحات 1 تا 5:

```bash
python scraper.py
```

### استفاده برنامه‌نویسی

```python
from scraper import ArzDigitalScraper

# ایجاد نمونه از اسکرپر
scraper = ArzDigitalScraper()

# اسکرپ صفحات 1 تا 5
scraper.scrape_multiple_pages(start_page=1, end_page=5)

# ذخیره داده‌ها
scraper.save_to_json()
scraper.save_to_csv()

# دریافت خلاصه
summary = scraper.get_summary()
print(f"تعداد کل ارزها: {summary['total_coins']}")
```

### اسکرپ تک صفحه

```python
from scraper import ArzDigitalScraper

scraper = ArzDigitalScraper()
coins = scraper.scrape_page(page_number=1)
print(f"تعداد ارزها در صفحه اول: {len(coins)}")
```

### تنظیم محل ذخیره فایل‌ها

```python
scraper = ArzDigitalScraper(
    output_dir="my_data",
    log_dir="my_logs"
)
```

## ساختار پروژه

```
arzdigital_scraper/
├── scraper.py          # فایل اصلی اسکرپر
├── requirements.txt    # کتابخانه‌های مورد نیاز
├── README.md          # مستندات
├── data/              # فایل‌های خروجی (JSON & CSV)
└── logs/              # فایل‌های لاگ
```

## داده‌های استخراج شده

برای هر ارز، اطلاعات زیر استخراج می‌شود:

- `name`: نام ارز
- `symbol`: نماد ارز
- `price_irr`: قیمت به تومان
- `price_usd`: قیمت به دلار
- `change_24h`: تغییرات 24 ساعته
- `change_direction`: جهت تغییرات (up/down)
- `market_cap`: ارزش بازار
- `volume_24h`: حجم معاملات 24 ساعته
- `rank`: رتبه ارز
- `url`: لینک صفحه ارز
- `scraped_at`: زمان استخراج داده

## خروجی

پس از اجرا، دو فایل ایجاد می‌شود:

1. **JSON File**: `data/arzdigital_coins_YYYYMMDD_HHMMSS.json`
2. **CSV File**: `data/arzdigital_coins_YYYYMMDD_HHMMSS.csv`

همچنین فایل لاگ در مسیر `logs/` ذخیره می‌شود.

## ویژگی‌های امنیتی و اخلاقی

- تاخیر تصادفی 1-3 ثانیه بین درخواست‌ها
- استفاده از User-Agent های متنوع
- محدودیت تعداد درخواست‌ها
- احترام به robots.txt (در صورت نیاز)

## مشکلات متداول

### خطای نصب کتابخانه‌ها

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### خطای encoding در Windows

از Python 3.7+ استفاده کنید و اطمینان حاصل کنید که terminal شما از UTF-8 پشتیبانی می‌کند.

### خطای timeout

اینترنت خود را بررسی کنید. در صورت لزوم، timeout را افزایش دهید:

```python
response = self.session.get(url, timeout=60)  # 60 seconds
```

## توسعه

برای افزودن قابلیت‌های جدید:

1. متدهای جدید به کلاس `ArzDigitalScraper` اضافه کنید
2. لاگ‌گذاری مناسب را فراموش نکنید
3. مدیریت خطا را پیاده‌سازی کنید

## مجوز

این پروژه تحت مجوز MIT منتشر شده است.

## هشدار

این ابزار صرفاً برای اهداف آموزشی طراحی شده است. لطفاً:

- از قوانین و مقررات سایت مقصد پیروی کنید
- از اسکرپینگ افراطی خودداری کنید
- حریم خصوصی و شرایط استفاده سایت را رعایت کنید

## پشتیبانی

در صورت بروز مشکل یا سوال، لطفاً یک Issue ایجاد کنید.

---

**نویسنده**: AI Assistant
**نسخه**: 1.0.0
**تاریخ**: 2025
