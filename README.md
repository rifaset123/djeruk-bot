# 🤖 Bot Informasi Desa Jeruk

Bot Telegram untuk memberikan informasi tentang Desa Jeruk menggunakan OpenAI API.

## ✨ Fitur

- **Menu Keyboard**: Antarmuka yang user-friendly dengan `ReplyKeyboardMarkup`
- **Powered by OpenAI**: Responses yang intelligent menggunakan GPT
- **Informasi Lengkap**:
  - Profil Desa Jeruk
  - Fasilitas Desa
  - Struktur Pemerintahan
  - Program & Kegiatan
  - Kontak & Lokasi
- **Pertanyaan Custom**: Pengguna dapat mengajukan pertanyaan spesifik
- **Error Handling**: Penanganan error yang baik

## 📋 Prasyarat

- Python 3.8+
- Telegram Bot Token (dari BotFather)
- OpenAI API Key

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone <repository>
cd djeruk-bot-gpt
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Buat file `.env` dan isi dengan:

```
TELEGRAM_TOKEN=your_telegram_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Dapatkan API Keys

**Telegram Bot Token:**

1. Buka Telegram dan cari @BotFather
2. Ketik `/newbot` dan ikuti instruksi
3. Copy token yang diberikan ke `.env`

**OpenAI API Key:**

1. Kunjungi https://platform.openai.com/api-keys
2. Create new API key
3. Copy ke `.env`

## 🎮 Cara Penggunaan

### Menjalankan Bot

```bash
python main.py
```

### Menu Tersedia

- **📍 Profil Desa Jeruk** - Informasi sejarah dan profil desa
- **🏠 Fasilitas Desa** - Info fasilitas umum
- **👥 Struktur Pemerintahan** - Perangkat desa
- **📅 Program & Kegiatan** - Program tahunan desa
- **📞 Kontak** - Kontak dan jam operasional
- **🔍 Pertanyaan Lainnya** - Tanyakan pertanyaan custom
- **⬅️ Kembali ke Menu Utama** - Kembali ke menu

### Commands

- `/start` - Mulai bot
- `/help` - Tampilkan bantuan
- `/menu` - Kembali ke menu utama
- `/cancel` - Hentikan percakapan

## 📁 Struktur File

```
djeruk-bot-gpt/
├── main.py              # Main bot application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (jangan commit)
├── .gitignore          # Git ignore file
└── README.md           # Dokumentasi ini
```

## ⚙️ Konfigurasi

### Mengubah Menu

Edit variable `MAIN_KEYBOARD` dan `INFO_KEYBOARD` di `main.py` untuk menambah/mengurangi menu.

### Mengubah OpenAI Model

Di fungsi `get_openai_response()`, ubah parameter `model`:

```python
model="gpt-3.5-turbo"  # Atau "gpt-4" untuk model yang lebih canggih
```

### Mengubah Sistem Prompt

Edit `system_message` di fungsi `get_openai_response()` untuk mengubah perilaku bot.

## 🔒 Security Tips

1. **JANGAN** commit file `.env`
2. Gunakan `.gitignore` untuk exclude `.env`
3. Rotate API keys secara berkala
4. Jangan bagikan token ke orang lain

## 📊 Monitoring

Bot ini menggunakan logging untuk tracking:

```python
logger.info("Bot is starting...")
```

Check console untuk melihat activity log.

## 🐛 Troubleshooting

### Bot tidak merespons

- Cek TELEGRAM_TOKEN di `.env`
- Pastikan bot sudah distart dengan /start
- Lihat console untuk error messages

### OpenAI API Error

- Verify OPENAI_API_KEY valid
- Check API quota di OpenAI dashboard
- Pastikan ada credit/subscription

### Library Import Error

```bash
pip install --upgrade -r requirements.txt
```

## 🤝 Kontribusi

Untuk menambah fitur atau memperbaiki bug:

1. Create branch baru
2. Make changes
3. Test thoroughly
4. Create pull request

## 📝 License

[Tambahkan license di sini]

## 📧 Kontak

Untuk pertanyaan atau support, hubungi [nama_kontak@email.com]

---

**Created with ❤️ for Desa Jeruk**
