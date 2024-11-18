import sqllite3
from tkinter import Tk, Label, Button, StringVar, messagebox,  ttk, Entry

#fungsi untuk membuat database dan tabel
def create_database() :
    conn = sqllite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXIST nilai_siswa(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT                     
        )
    ''')
    conn.commit()
    conn.close()

def fetch_data() :
    conn = sqllite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")
    rows = cursor.fetchall()
    conn.close()
    return rows

#fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqllite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa(nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
                   VALUES (?, ?, ?, ?)
                   ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

#fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):    
    conn = sqllite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?                      
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

#fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqllite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id))
    conn.commit()
    conn.close()

#fungsi untuk menghitung prediksi fakultas
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris :
        return "kedokteran"
    if fisika > biologi and fisika > inggris :
        return "Teknik"
    if inggris > biologi and inggris > fisika :
        return "Bahasa"
    else :
        return "tidak diketahui"  

#fungsi untuk menangani tombol submit
def submit():
    try:
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama :
            raise Exception("Nama siswa tidak boleh kosong. ")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris)

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas:{prediksi}") 
        clear_input()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

#fungsi untuk menangani tombol update
def update():
    try:
        if not selected_record_id.get():
            raise Exception("pilih data dari tabel untuk diupdate")

        record_id = int(selected_record_id.get())
        nama = nama.var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong. ")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui")
        clear_input()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan : {e}")

#fungsi untuk menangani tombol delete
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("pilih data dari tabel untuk dihapus!")
        
        record_id = int (selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data berhasil dihapus")
        clear_input()
        populate_table()
    except ValueError as e:
       messagebox.showerror("Error", f"Kesalahan: {e}")   

#fungsi mengosongkan input
def clear_input():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id("")

#fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert('', 'end', values=row)

#fungsi untuk mengisi input dengan data dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

#inisialisasi database
create_database()
#membuat GUI dengan tkinker
root = Tk()
root.tittle("Prediksi Fakultas Siswa")
#variabel tkinker
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()    #untuk menyimpan ID record yg dipilih

#elemen GUI
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row = 0 , column = 0, padx = 10, pady = 5 )
Entry(root, textvariable=nama_var).grid (row = 0, column = 1 , padx = 10, pady = 5)

Label(root, text="Nilai Bahasa Inggris").grid(row = 0 , column = 0, padx = 10, pady = 5 )
Entry(root, textvariable=nama_var). grid (row = 0, column = 1 , padx = 10, pady = 5)

Button ( root , text= "add", command = submit  ).grid (row = 4, column = 0, pady = 10)
Button ( root , text= "update", command = update  ).grid (row = 4, column = 1, pady = 10)
Button ( root , text= "delete", command = delete  ).grid (row = 4, column=2, pady=10)

#tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree= ttk.Treeview(root, column=columns, show= 'headings')

#menyesuaikan posisi teks disetiap kolom ke tengah
#mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

#event untuk memilih data dari tabel
tree.bind('<ButtonRelease-1', fill_inputs_from_table)
#mengisi tabel dengan data
populate_table()
#menjalankan aplikasi
root.mainloop()
