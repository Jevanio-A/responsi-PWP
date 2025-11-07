Website ini adalah aplikasi web portofolio pribadi berbasis Flask yang berfungsi untuk menampilkan informasi tentang diri kamu, proyek-proyek yang telah kamu buat, serta keahlian (skills) yang kamu miliki.

Aplikasi ini memiliki dua sisi:
1. Halaman Publik (User View)
Menampilkan profil, foto, biodata singkat
Menampilkan daftar project dan detailnya
Menampilkan daftar skill beserta levelnya

2. Halaman Admin (Admin Dashboard)
Login untuk admin
Mengedit profil (nama, bio, dan foto)
Menambah, mengedit, dan menghapus project
Menambah, mengedit, dan menghapus skill

Dibangun menggunakan:
Backend: Flask (Python)
Frontend: HTML, CSS (Bootstrap)
Database: MySQL
ORM: SQLAlchemy
Form: Flask-WTF

1. Persiapan Awal
Pastikan sudah terinstal:
Python 3
MySQL
pip (package manager)

2. Clone atau Simpan Proyek
Simpan semua file proyek (misalnya app.py, templates/, static/, dll) di satu folder.
Contoh:
D:\flask_portfolio\

3. Buat Virtual Environment (opsional tapi disarankan)
python -m venv venv
venv\Scripts\activate  # di Windows
# atau
source venv/bin/activate  # di Linux/Mac

4. Instal Dependensi
Jalankan perintah ini di terminal:
pip install -r requirements.txt
Jika belum punya file requirements.txt, kamu bisa install manual:
pip install flask flask_sqlalchemy flask_wtf flask_bcrypt mysqlclient

5. Atur Database MySQL
Masuk ke MySQL dan buat database baru:
CREATE DATABASE portfolio;

6. Jalankan Aplikasi
Di terminal, jalankan:
python app.py
Jika berhasil, akan muncul pesan seperti:
 * Running on http://127.0.0.1:5000/
Buka di browser:
http://localhost:5000

7. Login ke Halaman Admin
Buka:
http://localhost:5000/admin/login
Login dengan akun default:
Username: admin
Password: admin123
Setelah login, kamu bisa mengedit profil, menambah project, dan skill.

8. Upload Foto & Tambah Project
Masuk ke menu Edit Profil untuk upload foto.
Masuk ke Projects untuk tambah proyek baru.
Masuk ke Skills untuk tambah skill baru.

<img width="1919" height="1033" alt="image" src="https://github.com/user-attachments/assets/391e5885-e3bc-4d9e-9f12-bc1c7fc3bc15" />
<img width="1919" height="992" alt="image" src="https://github.com/user-attachments/assets/d4284b90-6c83-4248-8ac7-8d4143da9c04" />
<img width="1919" height="1036" alt="image" src="https://github.com/user-attachments/assets/de36c832-5fb9-4a27-8df1-31fa60621f7f" />
<img width="1919" height="1037" alt="image" src="https://github.com/user-attachments/assets/458f079c-bc83-42e6-b97a-7814e769af82" />
<img width="1919" height="1028" alt="image" src="https://github.com/user-attachments/assets/190c9f02-d629-4595-bcd8-91ebabe96d02" />
<img width="1919" height="998" alt="image" src="https://github.com/user-attachments/assets/8b0c5854-306a-437a-877a-a4138267c44c" />
