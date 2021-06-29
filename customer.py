import xmlrpc.client
import numpy as np
server_ip = "127.0.0.1"
server_port = 17171

server = xmlrpc.client.Server(f'http://{server_ip}:{server_port}')

class BioskopCustomer:
    def __init__(self, server):
        self.server = server
        self.output()

    def login(self):
        while True:
            username = input("username : ")
            password = input("password : ")
            
            self.idx = self.server.login_customer(username, password)
            if self.idx is None:
                print("username atau password salah")
            else:
                break
    
    def daftar(self):
        while True:
            username = input("username : ")
            password = input("password : ")
            
            success = self.server.tambah_customer(username, password)
            if success:
                break
            else:
                print("username sudah ada")

    def print_kursi(self, daftar_kursi):
        idx_col = ["{:3s}".format(str(kursi)) for kursi in range(len(daftar_kursi[0]))]
        print(f'     {"".join(idx_col)}')
        for idx_row, col in enumerate(daftar_kursi):
            rows = [f"[{' ' if kursi == -1 else 'X'}]" for kursi in col]
            print(f'{idx_row:3}: {"".join(rows)}')

    def get_jadwal(self):
        for jadwal in self.server.get_jadwal():
            print("index\t:", jadwal["idx"])
            print("judul\t:", jadwal["judul"])
            print("waktu\t:", jadwal["waktu"])
            print("harga\t:", jadwal["harga"])
            print("="*20)
        
    def get_detail_jadwal(self, idx_jadwal):
        jadwal = self.server.get_jadwal_by_idx(idx_jadwal)
        print("index\t:", jadwal["idx"])
        print("judul\t:", jadwal["judul"])
        print("waktu\t:", jadwal["waktu"])
        print("harga\t:", jadwal["harga"])
        print("kursi\t:")
        self.print_kursi(jadwal["daftar_kursi"])
    
    def pesan(self, idx_jadwal):
        jumlah = int(input("jumlah tiket : "))
        daftar_kursi = []

        for i in range(jumlah):
            print("tiket ke-", i+1)
            while True:
                row, col = input("masukan lokasi kursi (row col) : ").split()
                kursi = (int(row), int(col))

                if kursi in daftar_kursi:
                    print("harap memasukan kursi yang berbeda")
                    continue

                tersedia = self.server.check_kursi_kosong(idx_jadwal, kursi)
                if tersedia:
                    daftar_kursi.append(kursi)
                    break
                else:
                    print("kursi sudah diisi")
            print("="*20)
        
        harga = self.server.get_jadwal_by_idx(idx_jadwal)["harga"]
        print("harga satuan\t:", harga)
        print("total harga\t:", harga * jumlah)
        print("="*20)
        print("silahkan menyelesaikan pembayaran")
        input("ketik apa saja jika sudah membayar")
        print("="*20)
        self.server.pesan(idx_jadwal, self.idx, daftar_kursi)
        print("pembelian berhasil")
        input("ketik apa saja untuk kembali")
    
    def get_pesanan(self):
        print("\n"*40)
        for pesanan in self.server.get_pesanan(self.idx):
            jadwal = self.server.get_jadwal_by_idx(pesanan["idx_jadwal"])
            print("index\t:", jadwal["idx"])
            print("judul\t:", jadwal["judul"])
            print("waktu\t:", jadwal["waktu"])
            print("harga\t:", jadwal["harga"])
            print("jumlah\t:", len(pesanan["nomor_kursi"]))
            print("jumlah\t:", len(pesanan["nomor_kursi"]) * jadwal["harga"])
            print("kursi\t:", pesanan["nomor_kursi"])
            print("="*20)
        input("ketik apa saja untuk kembali")

    def output(self):
        while True:
            print("\n"*30)
            print("1. login")
            print("2. daftar")
            pil = input("pilihan : ")
            if pil == "1":
                self.login()
                break
            elif pil == "2":
                self.daftar()

        while True:
            print("\n"*30)
            print("=== Jadwal Film ===")
            self.get_jadwal()
            print("1. refresh")
            print("2. lihat detail jadwal")
            print("3. lihat pesanan")
            pil = input("pilihan : ")
            if pil == "1":
                continue
            elif pil == "2":
                idx_jadwal = int(input("masukan index jadwal : "))
                while True:
                    print("\n"*30)
                    self.get_detail_jadwal(idx_jadwal)
                    print("="*20)
                    print("1. pesan")
                    print("2. kembali")
                    pil = input("pilihan : ")
                    if pil == "1":
                        self.pesan(idx_jadwal)
                    elif pil == "2":
                        break
            elif pil == "3":
                self.get_pesanan()

BioskopCustomer(server)