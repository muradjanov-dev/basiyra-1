# O'zbekcha → Ruscha tarjimon Telegram bot

Bot o'zbekcha matnni rus tiliga tarjima qiladi (aiogram 3 + deep-translator, bepul Google Translate, API kalit kerak emas).

## Imkoniyatlar
- `/start` — salomlashish
- Har qanday matn → faqat ruscha tarjima
- 4500 belgidan uzun matn bo'laklab tarjima qilinadi, 4000 belgidan uzun javob bir nechta xabarga bo'linadi
- Tarjima vaqtida "yozmoqda..." holati ko'rsatiladi
- Rasm, stiker, ovoz va h.k. uchun: "✍️ Iltimos, o'zbekcha matn yuboring."
- Xatolar logga yoziladi, bot to'xtamaydi

## Lokal ishga tushirish
1. Python 3.10+ o'rnatilgan bo'lsin.
2. [@BotFather](https://t.me/BotFather) orqali bot yarating va tokenni oling.
3. Shu papkada `.env` faylini oching va tokenni yozing:
   ```
   BOT_TOKEN=123456789:AA...
   ```
4. Paketlarni o'rnating:
   ```bash
   pip install -r requirements.txt
   ```
5. Botni ishga tushiring:
   ```bash
   python bot.py
   ```
   Logda `Bot ishga tushdi: @bot_nomi` chiqsa — hammasi joyida.

## Railway'ga joylash (24/7)
1. Kod GitHub'da bo'lsin (`.env` `.gitignore` orqali yuklanmaydi).
2. [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo** → shu repozitoriyni tanlang.
3. Servis **Settings** → **Root Directory** = `telegram-bot`.
4. **Variables** bo'limiga `BOT_TOKEN` qo'shing.
5. **Settings** → **Deploy** → **Custom Start Command**: `python bot.py` (Procfile'dagi `worker` ham shuni bajaradi).
6. Deploy tugagach **Deployments → Logs** da `Bot ishga tushdi` yozuvini tekshiring.

> Muhim: bitta token bilan bir vaqtda faqat bitta nusxa polling qilishi mumkin. Railway'da ishga tushirganda lokal botni to'xtating, aks holda `TelegramConflictError` chiqadi.

## GitHub Actions'da ishlatish (Railway o'rniga)
Repo public bo'lgani uchun Actions bepul. Workflow: `.github/workflows/telegram-bot.yml`.

1. Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:
   nomi `BOT_TOKEN`, qiymati — bot tokeni.
2. **Actions** → **Telegram translator bot** → **Run workflow** (yoki `telegram-bot/` ga push qiling).
3. Logda `Bot ishga tushdi: @...` chiqadi.

Bitta job ko'pi bilan 6 soat ishlaydi, shuning uchun har 5 soatda (`cron`) yangi run boshlanib, eskisini bekor qiladi.
Almashinuv paytida bot bir necha soniya/daqiqa javob bermasligi mumkin — xabarlar yo'qolmaydi, keyin javob beriladi.
Eslatma: `schedule` faqat asosiy (`main`) branchda ishlaydi — workflow `main` ga merge qilinishi kerak.
