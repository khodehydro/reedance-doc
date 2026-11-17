# reedance-doc

پیش‌نویس‌های آموزش ترکی استانبولی با لیریک ارسالی کاربر؛ هر آهنگ پوشه و فایل خام مستقل دارد.

| خواننده و آهنگ | راهنما | فایل آموزشی |
| --- | --- | --- |
| Ayaz Erdoğan — Gülüm 2 (نمونهٔ قبلی) | [راهنما](tr/ayaz-erdogan/gulum-2/README.md) | [پیش‌نویس](tr/ayaz-erdogan/gulum-2/gulum-2.rddraft.json) |
| Ayaz Erdoğan — Adını Meze Etmem | [راهنما](tr/ayaz-erdogan/adini-meze-etmem/README.md) | [پیش‌نویس](tr/ayaz-erdogan/adini-meze-etmem/adini-meze-etmem.rddraft.json) |
| Ayaz Erdoğan ft. Mengelez — Baba | [راهنما](tr/ayaz-erdogan/baba/README.md) | [پیش‌نویس](tr/ayaz-erdogan/baba/baba.rddraft.json) |
| Ayaz Erdoğan — Bu Gece | [راهنما](tr/ayaz-erdogan/bu-gece/README.md) | [پیش‌نویس](tr/ayaz-erdogan/bu-gece/bu-gece.rddraft.json) |
| Ayaz Erdoğan — Desene Günaydın | [راهنما](tr/ayaz-erdogan/desene-gunaydin/README.md) | [پیش‌نویس](tr/ayaz-erdogan/desene-gunaydin/desene-gunaydin.rddraft.json) |
| Ayaz Erdoğan — Döndüm o Yollardan | [راهنما](tr/ayaz-erdogan/dondum-o-yollardan/README.md) | [پیش‌نویس](tr/ayaz-erdogan/dondum-o-yollardan/dondum-o-yollardan.rddraft.json) |

## پنج درس جدید

برای هر درس، سطرهای تکراری مستقل باقی مانده‌اند تا بعداً جداگانه زمان‌بندی شوند؛ برچسب بخش‌های آهنگ و پیشنهادهای نامربوط حذف شده‌اند. هر سطر ترجمهٔ فارسی/انگلیسی و توکن‌بندی دارد. **مثال‌های واژگان مستقل از لیریک‌اند**؛ واژه‌ها، گرامر، اصطلاحات، جدول‌های مرتبط و ۱۶ تمرین در خود JSON هستند. صرف هر فعل شامل شش شخص در زمان/وجه و قطبیتِ متن و حال گستردهٔ مثبت است. امر اول‌شخص ندارد و فعل‌قیدها و صفت‌فعلی‌ها به‌دروغ فعل شخص‌دار شمرده نمی‌شوند. عددهای یک تا ده و واژه‌های مرتبط با موضوعات متن به‌صورت جداگانه آموزش داده شده‌اند. نمونهٔ قبلی Gülüm 2 بازنویسی نشده است.

فایل‌های جدید صوت، تصویر، زمان‌بندی و سطح ادعایی ندارند و بستهٔ نهایی نیستند. متن توسط کاربر ارسال شده و مجوزی همراه آن نبوده است؛ `rightsStatus` برابر `unverified` است. پیش از انتشار باید حقوق متن/صوت بررسی، سطح تعیین، صوت انتخاب و تک‌تک سطرها در Studio همگام شود.

## سازگاری ترکی با قرارداد

قرارداد اصلی v1 فقط `en/es/ko` را تعریف می‌کند و فایل `tr` را بدون گسترش رد می‌کند. در کد Studio شاخهٔ `arena/132cfe2a-reedance-desktop` در commit `6707874dec5c8dcd874279238a5abd1c5eaecbb0`، ترکی به‌صورت آزمایشی پشتیبانی و schema در حافظه گسترش داده می‌شود؛ هر پنج فایل با اعتبارسنج ساختاری و معنایی همان نسخه بدون خطا یا هشدار بررسی شده‌اند. این آزمون **به معنی تست واردکردن یا انتشار در نسخهٔ نصب‌شده نیست**؛ سازگاری Studio و Android مقصد را جداگانه تأیید کنید. برای دورزدن محدودیت، زبان یا شناسه‌های ترکی را به انگلیسی تغییر ندهید.

## آزمون‌ها

```bash
# بررسی محتوا، توکن‌ها، ارجاع‌ها، مثال‌های مستقل، صرف‌ها و تمرین‌ها
python3 scripts/validate-new-drafts.py

# اختیاری: بررسی schemaهای محلی با گسترش tr در حافظه
python3 -m pip install -r tests/requirements.txt
python3 scripts/validate-new-drafts.py --schema
```

schemaهای آزمون، کپی بدون تغییر قرارداد v1 با منبع و نسخهٔ ثبت‌شده در [راهنمای fixtureها](tests/contracts/v1/README.md) هستند. آزمون‌ها جای بازبینی انسانی ترجمه‌ها یا کنترل حقوق را نمی‌گیرند.
