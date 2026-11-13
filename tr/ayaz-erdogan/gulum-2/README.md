# Gülüm 2 — Ayaz Erdoğan (فایل خام آموزشی)

## مسیر و فایل

```text
tr/
└── ayaz-erdogan/
    └── gulum-2/
        ├── gulum-2.rddraft.json   ← فایل خام اصلی (UTF-8، بدون صوت و بدون زمان‌بندی)
        └── README.md              ← همین راهنما
```

- `songId`: `gulum-2`
- `targetLanguage`: `tr` — زبان مقصد آموزش: ترکی استانبولی
- `locale`: `tr-TR`
- `title`: `Gülüm 2`
- `artist`: `Ayaz Erdoğan`
- `level`: **ارائه نشده بود و عمداً حذف شده است** — طبق `AI_CONTENT_AGENT.md` نباید سطح ساختگی گذاشت؛ Windows باید پیش از export آن را تکمیل کند.

## محتوا (صفر تا صد از روی لیریک ارسالی)

| بخش | تعداد |
| --- | --- |
| `lyrics[]` | ۴۶ سطر (`line-1` … `line-46`) — بند ترجیع سه بار به‌صورت سطرهای جدا آمده تا در Windows هر بار جداگانه روی تایم‌لاین سینک شود |
| `vocabulary[]` | ۷۵ واژه با `lexemeId` از نوع `tr:…`، `lemma`، `normalizedKey`، معنی فارسی/انگلیسی، تلفظ فارسی و مثال |
| `grammar[]` | ۱۲ نکته: مفعول `-i` و `de`، امر منفی `-ma`، مجهول/اصطلاح `vurulmak`، نقلی `-miş`، شرطی `-sa + da`، میل `-sI + var`، توانایی `-bil + mi`، سؤال `mi`، التزامی `-sIn`، `-siz` و ناتوانی، زمان گسترده `-r`، انعکاسی `kendi` |
| `idioms[]` | ۸ اصطلاح واقعی: `deliler gibi`، `hasret kalmak`، `vurulmak`، `ne hâle gelmek`، `içine etmek`، `belanı bulmak`، `gölgen olmak`، `bir gecelik olmak` |
| `sentences[]` | ۸ جملهٔ کاربردی با ارجاع `lineId` |
| `vocabularyTables[]` | ۳ جدول: ضمیرها، فعل‌های پرکاربرد، اسم‌های انتزاعی/احساسی |
| `questions[]` | ۱۶ سؤال: ۴ `choice` + ۴ `match` + ۴ `order` + ۴ `typing` |

هر سطر `text` اصلی ترکی با نشانه‌گذاری و حروف ترکی (`ş, ğ, ü, ö, ç, ı, İ`) حفظ شده و برای هر توکن `surface` + ترجمهٔ فارسی/انگلیسی + در صورت وجود `lexemeId` آمده است. ترتیب توکن‌ها دقیقاً با متن سطر سازگار است (`" ".join(surface) == text`).

**محدودیت صریح فایل خام رعایت شده است:** هیچ `media`، `audio`، `cover`، مسیر/URL صوت، Base64، hash صوت، `startMs`/`endMs`، کلید یا امضا در فایل نیست. حجم فایل حدود ۱۲۱ KB است (سقف مجاز ۴ MiB).

## ⚠️ نکتهٔ مهم قرارداد: زبان `tr` در v1 پشتیبانی نمی‌شود

اسناد مرجع در شاخهٔ `arena/e6a6294d-reedance` ریپوی `khodehydro/reedance` (`contracts/v1/draft.schema.json` و `lesson.schema.json`) فقط این‌ها را مجاز می‌دانند:

- `targetLanguage`: فقط `en | es | ko`
- `locale`: فقط `en-* | es-* | ko-*`
- `lexemeId` / `conceptId`: فقط پیشوند `en: | es: | ko:`

این فایل با همان ساختار، دقیقاً با کدهای متناظر ترکی ساخته شده است: `tr`، `tr-TR` و `tr:…`. بنابراین:

- با **schema دست‌نخوردهٔ v1** رد می‌شود — اعتبارسنجی انجام‌شده نشان داد ۲۳۷ خطا، و **همه** فقط از همین سه کد زبان است (صفر خطای ساختاری دیگر).
- با **schema گسترش‌یافته به `tr`** (تغییر سه الگو/مقدار بالا، معادل یک اصلاحیهٔ هماهنگ یا `v2`) **کاملاً معتبر است (صفر خطا)**.

پس پیش از واردکردن در Windows Studio باید قرارداد به `tr` گسترش یابد؛ در غیر این صورت فایل را با برچسب `en` تحویل ندهید — آن کار واژه‌های ترکی را اشتباه برچسب می‌زند. این انحراف در فیلد `notes` داخل خود JSON هم ثبت شده است.

## چرا Windows هنگام واردکردن خطا می‌دهد؟ (بررسی `reedance-desktop`)

بررسی شاخهٔ `arena/132cfe2a-reedance-desktop` ریپوی `khodehydro/reedance-desktop` نشان می‌دهد خطا از **محتوای فایل نیست**؛ Windows فعلاً فقط `en/es/ko` را می‌فهمد و ترکی را رد می‌کند.

### مسیر واردکردن در Windows (`src/main/import.ts` → `importDraftFile`)

1. خواندن فایل (سقف ۴ MiB، رد BOM، UTF-8 سخت‌گیرانه) — این فایل پاس می‌کند (۱۲۱ KB، بدون BOM).
2. `parseStrictJson` (رد کلید تکراری و دادهٔ اضافی) — پاس می‌کند.
3. `findForbiddenKeys` (رد `media`/`startMs`/`audio`/…) — پاس می‌کند؛ در فایل هیچ‌کدام نیست.
4. **`validateDraftStructure` (Ajv روی `contracts/draft.schema.json` + `lesson.schema.json`) — اینجا رد می‌شود.** پیام کاربر چیزی شبیه این است (فقط ۶ خطای اول نمایش داده می‌شود):

   ```text
   draft failed schema validation:
   $.grammar[0].conceptId: 'tr:accusative-de' does not match '^(?:en|es|ko):...'
   $.targetLanguage: must be equal to one of the allowed values
   $.locale: 'tr-TR' does not match '^(?:en|es|ko)...'
   $.vocabulary[0].lexemeId: 'tr:ben' does not match '^(?:en|es|ko):...'
   ```

   در مجموع ۲۳۷ خطای schema، همه فقط از کدهای `tr`/`tr-TR`/`tr:…` — صفر خطای دیگر.
5. حتی اگر فقط schema را دستی patch کنید، دو لایهٔ بعدی هم رد می‌کنند:
   - `src/main/validation.ts` خط ۹۳: `LEXEME_RE = /^(?:en|es|ko):[a-z0-9]+(?:-[a-z0-9]+)*$/` (هر ۷۵ `lexemeId` و ۱۲ `conceptId` را رد می‌کند).
   - `src/main/db.ts` خط ۲۴: `CHECK(target_language IN ('en','es','ko'))` در جدول `songs` — درج پروژه در SQLite می‌خورد به خطای constraint.

### همهٔ جاهایی که در Windows به `en/es/ko` قفل شده‌اند

| فایل | مورد |
| --- | --- |
| `contracts/lesson.schema.json` | `language` enum، الگوی `locale` و `lexemeId` (‏`draft.schema.json` از طریق `urn:reedance:lesson:v1` به همین تعریف‌ها ارجاع می‌دهد) |
| `src/shared/types.ts:9` | `TargetLanguage = "en" \| "es" \| "ko"` |
| `src/main/validation.ts:93` | `LEXEME_RE` |
| `src/main/import.ts:73` | الگوی `LOCALE` (مسیر ساخت پروژهٔ خالی) |
| `src/main/db.ts:24` | `CHECK(target_language IN ('en','es','ko'))` — نیازمند migration برای دیتابیس‌های موجود |
| `src/main/ipc.ts:192,420,433` | فهرست مجاز زبان در IPC |
| `src/main/stats.ts:17` | `LANGUAGES = ["en","es","ko"]` |
| `src/renderer/App.tsx:37` | `LOCALES = { en:"en-GB", es:"es-ES", ko:"ko-KR" }` — باید `tr:"tr-TR"` اضافه شود |
| `src/renderer/components/LibraryPage.tsx` | فهرست زبان‌ها/پرچم‌ها در کتابخانه |

### راه‌حل درست

گسترش هماهنگ قرارداد به `tr` در همهٔ مصرف‌کننده‌ها (Windows + Android + contracts) — طبق `contracts/v1/README.md` تغییر ناسازگار باید با نسخهٔ جدید (`v2`) یا اصلاحیهٔ هماهنگ هر دو تیم انجام شود، نه patch محلیِ فقط یک schema. پس از آن، همین فایل بدون هیچ تغییری وارد می‌شود (با schema گسترش‌یافته صفر خطا دارد).

**راه‌حل غلط (انجام ندهید):** تغییر `targetLanguage` به `en` و `lexemeId`ها به `en:…` فقط برای ردشدن از import. آن کار واژه‌های ترکی را به‌عنوان انگلیسی ثبت می‌کند، رجیستری lexeme و آمار زبان را خراب می‌کند و خروجی Android را اشتباه می‌سازد.

## حقوق و گام بعدی

- متن لیریک توسط مدیر در همین تسک ارسال شد و **مدرک مجوز همراه آن نبود**؛ در `sources` هر دو بخش `rightsStatus: "unverified"` ثبت شده است. هیچ مجوز/URL/کلیدی ساخته نشده است.
- گام بعدی (طبق `PACKAGE_V1.md` و `WINDOWS_AGENT.md`): پس از گسترش قرارداد به `tr`، فایل را در Windows Studio وارد کنید، صوت را از سیستم خودتان انتخاب کنید، هر ۴۶ سطر را روی تایم‌لاین سینک کنید، `level` و حقوق صوت/متن را تکمیل و تأیید انسانی بگیرید؛ فقط آن‌وقت `lesson.json` زمان‌دار و `.rdpack` ساخته می‌شود. این فایل خام به‌تنهایی خروجی انتشار نیست.

## اعتبارسنجی

```bash
# JSON معتبر و بدون فیلد ممنوعه
python3 -m json.tool tr/ayaz-erdogan/gulum-2/gulum-2.rddraft.json > /dev/null

# اعتبارسنجی با draft.schema.json + lesson.schema.json
# (با ثبت urn:reedance:lesson:v1 در validator محلی، بدون شبکه)
# نتیجه با schema اصلی v1: فقط خطاهای کد زبان tr
# نتیجه با schema گسترش‌یافته به tr: صفر خطا
```
