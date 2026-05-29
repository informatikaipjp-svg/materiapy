import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime, timedelta

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SISTEMA PERPUSTAKAAN ELITE v3.3")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f0f2f5")
        
        self.conn = sqlite3.connect("perpustakaan_ultimate.db")
        self.cursor = self.conn.cursor()
        self.setup_db()
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.apply_styles()
        self.show_login()

    def apply_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TNotebook", background="#f0f2f5", borderwidth=0)
        self.style.configure("TNotebook.Tab", padding=[15, 8], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", "#3498db")], foreground=[("selected", "white")])
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#ecf0f1")

    def setup_db(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS buku (id INTEGER PRIMARY KEY AUTOINCREMENT, judul TEXT, penulis TEXT, stok INTEGER)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS pinjam (id INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT, buku_id INTEGER, tgl_pinjam TEXT, tgl_deadline TEXT, status TEXT DEFAULT 'Dipinjam', denda INTEGER DEFAULT 0, status_denda TEXT DEFAULT '-')")
        self.conn.commit()

    def show_login(self):
        self.login_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        card = tk.Frame(self.login_frame, bg="white", padx=40, pady=40, highlightbackground="#dcdde1", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(card, text="ADMIN LOGIN", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))
        self.create_input(card, "Username", "user")
        self.ent_user = self.last_entry
        self.create_input(card, "Password", "admin", show="*")
        self.ent_pass = self.last_entry
        tk.Button(card, text="LOGIN AGORA", bg="#3498db", fg="white", font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2", width=25, command=self.check_login).pack(ipady=10, pady=20)

    def create_input(self, parent, label_text, default_val="", show=""):
        tk.Label(parent, text=label_text, bg="white", fg="#7f8c8d", font=("Segoe UI", 9)).pack(anchor="w")
        entry = tk.Entry(parent, font=("Segoe UI", 11), width=30, bd=0, highlightbackground="#dcdde1", highlightthickness=1)
        entry.pack(pady=(5, 15), ipady=8)
        entry.insert(0, default_val)
        self.last_entry = entry

    def check_login(self):
        if self.ent_user.get() == "user" and self.ent_pass.get() == "admin":
            self.login_frame.destroy()
            self.init_main_ui()
        else:
            messagebox.showerror("Error", "Username ka Password sala!")

    def init_main_ui(self):
        self.main_container = tk.Frame(self.root, bg="#f0f2f5")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(1, weight=1)

        header = tk.Frame(self.main_container, bg="#2c3e50", height=70)
        header.grid(row=0, column=0, sticky="ew")
        tk.Label(header, text="SISTEMA JESTAUN PERPUSTAKAAN ELITE", bg="#2c3e50", fg="white", font=("Segoe UI", 16, "bold")).pack(pady=20)

        self.tabs = ttk.Notebook(self.main_container)
        self.tabs.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)

        self.tab1 = tk.Frame(self.tabs, bg="white")
        self.tab2 = tk.Frame(self.tabs, bg="white")
        self.tab3 = tk.Frame(self.tabs, bg="white")
        
        self.tabs.add(self.tab1, text="  LIVRU & EMPRESTIMO  ")
        self.tabs.add(self.tab2, text="  ENTREGA & DENDA  ")
        self.tabs.add(self.tab3, text="  RELATORIU JERAL  ")

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()
        self.refresh_all()

    def setup_tab1(self):
        self.tab1.rowconfigure(2, weight=1)
        self.tab1.columnconfigure(0, weight=1)
        f_input = tk.Frame(self.tab1, bg="#ecf0f1", pady=10, padx=15)
        f_input.grid(row=0, column=0, sticky="ew")
        tk.Label(f_input, text="TITULU:", bg="#ecf0f1").grid(row=0, column=0, padx=5)
        self.e_judul = tk.Entry(f_input, width=25)
        self.e_judul.grid(row=0, column=1, padx=5)
        tk.Label(f_input, text="STOK:", bg="#ecf0f1").grid(row=0, column=2, padx=5)
        self.e_stok = tk.Entry(f_input, width=10)
        self.e_stok.grid(row=0, column=3, padx=5)
        tk.Button(f_input, text="ADISIONA", bg="#2ecc71", fg="white", bd=0, padx=10, command=self.add_book).grid(row=0, column=4, padx=10)

        f_search = tk.Frame(self.tab1, bg="white", pady=10, padx=15)
        f_search.grid(row=1, column=0, sticky="ew")
        self.e_search = tk.Entry(f_search, width=30)
        self.e_search.pack(side="left", padx=10)
        tk.Button(f_search, text="BUKA", bg="#3498db", fg="white", bd=0, padx=15, command=self.search_buku).pack(side="left", padx=5)
        tk.Button(f_search, text="MOSTRAR HOTU", bg="#95a5a6", fg="white", bd=0, padx=15, command=self.refresh_all).pack(side="left", padx=5)

        self.tree_buku = ttk.Treeview(self.tab1, columns=("id", "judul", "stok"), show="headings")
        self.tree_buku.heading("id", text="ID"); self.tree_buku.heading("judul", text="TITULU"); self.tree_buku.heading("stok", text="STOK")
        self.tree_buku.grid(row=2, column=0, sticky="nsew", padx=15, pady=5)

        f_borrow = tk.Frame(self.tab1, bg="#f8f9fa", pady=15, padx=15)
        f_borrow.grid(row=3, column=0, sticky="ew")
        self.e_nama = tk.Entry(f_borrow, width=20); self.e_nama.pack(side="left", padx=5)
        self.e_bid = tk.Entry(f_borrow, width=8); self.e_bid.pack(side="left", padx=5)
        tk.Button(f_borrow, text="EMPRESTA", bg="#9b59b6", fg="white", bd=0, padx=20, command=self.do_borrow).pack(side="right")

    def setup_tab2(self):
        self.tab2.rowconfigure(0, weight=1); self.tab2.columnconfigure(0, weight=1)
        self.tree_pinjam = ttk.Treeview(self.tab2, columns=("id", "nama", "bid", "dead", "status", "denda", "sdenda"), show="headings")
        for c in ("id", "nama", "bid", "dead", "status", "denda", "sdenda"): self.tree_pinjam.heading(c, text=c.upper()); self.tree_pinjam.column(c, anchor="center")
        self.tree_pinjam.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        btn_f = tk.Frame(self.tab2, bg="white"); btn_f.grid(row=1, column=0, pady=20)
        tk.Button(btn_f, text="FO FILA", bg="#e67e22", fg="white", bd=0, width=20, command=self.do_return).pack(side="left", padx=10, ipady=10)
        tk.Button(btn_f, text="SELU DENDA", bg="#f1c40f", fg="#2c3e50", bd=0, width=20, command=self.do_pay).pack(side="left", padx=10, ipady=10)

    def setup_tab3(self):
        """SUB-MENU RELATORIO GERAL"""
        self.tab3.rowconfigure(1, weight=1)
        self.tab3.columnconfigure(0, weight=1)

        header_rep = tk.Frame(self.tab3, bg="white", pady=10)
        header_rep.grid(row=0, column=0, sticky="ew")
        self.lbl_last_borrower = tk.Label(header_rep, text="EMPRESTADOR IKUS LIU: -", font=("Segoe UI", 12, "bold"), bg="white", fg="#e74c3c")
        self.lbl_last_borrower.pack()

        # Kriar Notebook foun iha Tab Relatoriu laran (Sub-menu)
        self.sub_tabs_rep = ttk.Notebook(self.tab3)
        self.sub_tabs_rep.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Frame ba Sub-tabs
        self.sub_f_tuir = tk.Frame(self.sub_tabs_rep, bg="white")
        self.sub_f_uluk = tk.Frame(self.sub_tabs_rep, bg="white")

        self.sub_tabs_rep.add(self.sub_f_tuir, text="  DADOS FOUN (FOTI TUIR)  ")
        self.sub_tabs_rep.add(self.sub_f_uluk, text="  DADOS ANTIGU (FOTI ULUK)  ")

        # Treeview ba Relatoriu Foun (DESC)
        self.tree_rep_tuir = ttk.Treeview(self.sub_f_tuir, columns=("id", "nama", "buku", "tgl", "status", "denda"), show="headings")
        # Treeview ba Relatoriu Antigu (ASC)
        self.tree_rep_uluk = ttk.Treeview(self.sub_f_uluk, columns=("id", "nama", "buku", "tgl", "status", "denda"), show="headings")

        for tree in (self.tree_rep_tuir, self.tree_rep_uluk):
            for c in ("id", "nama", "buku", "tgl", "status", "denda"):
                tree.heading(c, text=c.upper())
                tree.column(c, anchor="center")
            tree.pack(expand=True, fill="both", padx=5, pady=5)

    def search_buku(self):
        key = self.e_search.get()
        for i in self.tree_buku.get_children(): self.tree_buku.delete(i)
        self.cursor.execute("SELECT id, judul, stok FROM buku WHERE judul LIKE ?", (f'%{key}%',))
        for r in self.cursor.fetchall(): self.tree_buku.insert('', 'end', values=r)

    def refresh_all(self):
        self.e_search.delete(0, 'end')
        
        # Refresh Buku
        for i in self.tree_buku.get_children(): self.tree_buku.delete(i)
        self.cursor.execute("SELECT id, judul, stok FROM buku")
        for r in self.cursor.fetchall(): self.tree_buku.insert('', 'end', values=r)
        
        # Refresh Emprestimo Ativu
        for i in self.tree_pinjam.get_children(): self.tree_pinjam.delete(i)
        self.cursor.execute("SELECT id, nama, buku_id, tgl_deadline, status, denda, status_denda FROM pinjam WHERE status='Dipinjam'")
        for r in self.cursor.fetchall(): self.tree_pinjam.insert('', 'end', values=r)
        
        # REFRESH RELATORIU (SUB-MENU)
        # 1. Foti Tuir (DESC)
        for i in self.tree_rep_tuir.get_children(): self.tree_rep_tuir.delete(i)
        self.cursor.execute("SELECT id, nama, buku_id, tgl_deadline, status, denda FROM pinjam ORDER BY id DESC")
        rows_tuir = self.cursor.fetchall()
        for r in rows_tuir: self.tree_rep_tuir.insert('', 'end', values=r)
        
        # 2. Foti Uluk (ASC)
        for i in self.tree_rep_uluk.get_children(): self.tree_rep_uluk.delete(i)
        self.cursor.execute("SELECT id, nama, buku_id, tgl_deadline, status, denda FROM pinjam ORDER BY id ASC")
        rows_uluk = self.cursor.fetchall()
        for r in rows_uluk: self.tree_rep_uluk.insert('', 'end', values=r)

        if rows_tuir:
            self.lbl_last_borrower.config(text=f"EMPRESTADOR IKUS LIU: {rows_tuir[0][1].upper()}")

    def add_book(self):
        if self.e_judul.get() and self.e_stok.get():
            self.cursor.execute("INSERT INTO buku (judul, stok) VALUES (?,?)", (self.e_judul.get(), int(self.e_stok.get())))
            self.conn.commit()
            self.refresh_all()
            self.e_judul.delete(0, 'end'); self.e_stok.delete(0, 'end')

    def do_borrow(self):
        n, bid = self.e_nama.get(), self.e_bid.get()
        if not (n and bid): return
        self.cursor.execute("SELECT stok FROM buku WHERE id=?", (bid,))
        res = self.cursor.fetchone()
        if res and res[0] > 0:
            dead = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            self.cursor.execute("INSERT INTO pinjam (nama, buku_id, tgl_deadline) VALUES (?,?,?)", (n, bid, dead))
            self.cursor.execute("UPDATE buku SET stok = stok - 1 WHERE id=?", (bid,))
            self.conn.commit()
            self.refresh_all()
            messagebox.showinfo("Sucesso", f"Livru empresta ba {n}")

    def do_return(self):
        sel = self.tree_pinjam.focus()
        if not sel: return
        items = self.tree_pinjam.item(sel)['values']
        pid, bid, dead = items[0], items[2], items[3]
        d_obj = datetime.strptime(dead, "%Y-%m-%d")
        denda = 0
        s_denda = "-"
        if datetime.now() > d_obj:
            atrasu_loron = (datetime.now() - d_obj).days
            denda = atrasu_loron * 10 
            s_denda = "SEIDANK SELE"
        self.cursor.execute("UPDATE pinjam SET status='Filadu', denda=?, status_denda=? WHERE id=?", (denda, s_denda, pid))
        self.cursor.execute("UPDATE buku SET stok = stok + 1 WHERE id=?", (bid,))
        self.conn.commit()
        self.refresh_all()
        if denda > 0: messagebox.showwarning("Denda", f"Tenke selu: ${denda}")

    def do_pay(self):
        sel = self.tree_pinjam.focus()
        if not sel: return
        pid = self.tree_pinjam.item(sel)['values'][0]
        self.cursor.execute("UPDATE pinjam SET status_denda='LUNAS' WHERE id=?", (pid,))
        self.conn.commit()
        self.refresh_all()
        messagebox.showinfo("Sucesso", "Denda LUNAS!")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()