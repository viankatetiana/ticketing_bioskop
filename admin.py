import xmlrpc.client

server_ip = "127.0.0.1"
server_port = 17171

server = xmlrpc.client.Server(f'http://{server_ip}:{server_port}')

class BioskopAdmin:
    def __init__(self, server):
        self.server = server
        self.output()

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
    
    def tambah_jadwal(self):
        while True:
            print("\n"*30)
            waktu = input("waktu (DD/MM/YYYY HH:mm) : ")
            
            print("=== Daftar Film ===")
            self.get_film()
            idx_film = input("index film\t: ")

            print()
            print("=== Daftar Theater ===")
            self.get_theater()
            idx_theater = input("index theater\t: ")
            
            harga = input("harga\t\t: ")

            success = self.server.tambah_jadwal(int(idx_film), int(harga), waktu, int(idx_theater))
            if success:
                break
            else:
                print("="*20)
                print("waktu telah berlalu atau theater di waktu tersebut sudah full")
                input("ketik apa saja untuk ulang")

    
    def tambah_film(self):
        judul = input("judul\t\t: ")
        durasi = input("durasi (menit)\t: ")
        self.server.tambah_film(judul, int(durasi))
    
    def update_film(self, idx_film):
        judul = input("judul\t\t: ")
        durasi = input("durasi (menit)\t: ")
        self.server.update_film(idx_film, judul, int(durasi))
    
    def get_film(self):
        for idx, film in enumerate(self.server.get_film()):
            print("index\t:", idx)
            print("judul\t:", film["judul"])
            print("durasi\t:", film["durasi"])
            print("="*20)

    def get_theater(self):
        for idx, theater in enumerate(self.server.get_theater()):
            print("index\t:", idx)
            print("nama\t\t:", theater["nama"])
            print("total kursi\t:", theater["total_kursi"])
            print("="*20)

    def output(self):
        while True:
            print("\n"*30)
            print("=== Jadwal Film ===")
            self.get_jadwal()
            print("1. refresh")
            print("2. lihat detail jadwal")
            print("3. tambah jadwal")
            print("4. lihat daftar film")
            print("5. lihat daftar theater")
            pil = input("pilihan : ")
            if pil == "1":
                continue
            elif pil == "2":
                idx_jadwal = int(input("masukan index jadwal : "))
                while True:
                    print("\n*30")
                    self.get_detail_jadwal(idx_jadwal)
                    print("="*20)
                    print("1. edit waktu")
                    print("2. edit harga")
                    print("3. kembali")
                    pil = input("pilihan : ")
                    if pil == "1":
                        waktu = input("waktu (DD/MM/YYYY HH:mm)\t: ")
                        self.server.update_waktu_jadwal(waktu)
                    elif pil == "2":
                        harga = input("harga\t: ")
                        self.server.update_harga_jadwal(harga)
                    elif pil == "3":
                        break
            elif pil == "3":
                self.tambah_jadwal()
            elif pil == "4":
                while True:
                    print("\n"*30)
                    print("=== Daftar Film ===")
                    self.get_film()
                    print("1. tambah film")
                    print("2. update film")
                    print("3. kembali")
                    pil = input("pilihan : ")
                    if pil == "1":
                        self.tambah_film()
                    elif pil == "2":
                        idx_film = int(input("masukan index film : "))
                        self.update_film(idx_film)
                    elif pil == "3":
                        break
            elif pil == "5":
                print("\n"*30)
                print("=== Daftar Theater ===")
                self.get_theater()
                input("ketik apa saja untuk kembali ")

BioskopAdmin(server)