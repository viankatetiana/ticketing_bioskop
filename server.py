from xmlrpc.server import SimpleXMLRPCServer
from datetime import datetime
import numpy as np
import threading

server_ip = "0.0.0.0"
server_port = 17171

with SimpleXMLRPCServer((server_ip, server_port), allow_none=True) as server:
    server.register_introspection_functions()

    class BioskopServer:
        def __init__(self):
            self.theater = [
                {
                    "nama": "theater 1",
                    "total_kursi": (10, 20)
                },
                {
                    "nama": "theater 2",
                    "total_kursi": (10, 30)
                },
                {
                    "nama": "theater 3",
                    "total_kursi": (15, 20)
                },
            ]

            self.film = [
                {
                    "judul": "Avengers Endgame",
                    "durasi": 180
                },
                {
                    "judul": "Doctor Strange",
                    "durasi": 100
                },
            ]

            self.jadwal = [
                {
                    "idx_film": 0,
                    "harga": 50000,
                    "waktu": datetime.strptime("1/7/2021 18:00", "%d/%m/%Y %H:%M"),
                    "idx_theater": 0,
                    "daftar_kursi": np.full(self.theater[0]["total_kursi"], -1, dtype="int").tolist()
                }
            ]

            self.customer = [
                {
                    "username": "abc",
                    "password": "abc",
                    "pesanan": [],
                }
            ]

        def tambah_film(self, judul, durasi):
            self.film.append({
                "judul": judul,
                "durasi": durasi
            })

        def tambah_jadwal(self, idx_film, harga, waktu, idx_theater):
            new = {
                "idx_film": idx_film,
                "harga": harga,
                "waktu": datetime.strptime(waktu, "%d/%m/%Y %H:%M"),
                "idx_theater": idx_theater,
                "daftar_kursi": np.full(self.theater[idx_theater]["total_kursi"], -1, dtype="int").tolist()
            }

            if new["waktu"] < datetime.now():
                return False
            
            durasi = self.film[idx_film]["durasi"]
            
            for jadwal in self.jadwal:
                if jadwal["idx_theater"] == idx_theater:
                    selisih = abs((new["waktu"]-jadwal["waktu"]).total_seconds()) / 60

                    if selisih < durasi:
                        return False
                    

            self.jadwal.append(new)
            return True

        def tambah_customer(self, username, password):
            for cust in self.customer:
                if cust["username"] == username:
                    return False

            self.customer.append(
                {
                    "username": username,
                    "password": password,
                    "pesanan": []
                }
            )

            return True

        def login_customer(self, username, password):
            for idx, cust in enumerate(self.customer):
                if cust["username"] == username and cust["password"] == password:
                    return idx
            return None
        
        def update_film(self, idx_film, judul, durasi):
            self.film[idx_film] = {
                "judul": judul,
                "durasi": durasi
            }
        
        def update_waktu_jadwal(self, idx_jadwal, waktu):
            self.jadwal[idx_jadwal]["waktu"] = datetime.strptime(waktu, "%d/%m/%Y %H:%M")
        
        def update_harga_jadwal(self, idx_jadwal, harga):
            self.jadwal[idx_jadwal]["harga"] = harga

        def get_theater(self):
            return self.theater
        
        def get_film(self):
            return self.film

        def get_jadwal(self):
            return [self.get_jadwal_by_idx(idx) for idx in range(len(self.jadwal)) if self.get_jadwal_by_idx(idx)["waktu_datetime"] >= datetime.now()]

        def get_jadwal_by_idx(self, idx_jadwal):
            jadwal = self.jadwal[idx_jadwal].copy()
            jadwal["idx"] = idx_jadwal
            jadwal["waktu_datetime"] = jadwal["waktu"]
            jadwal["waktu"] = datetime.strftime(jadwal["waktu"], "%d/%m/%Y %H:%M")
            jadwal["theater"] = self.theater[jadwal["idx_theater"]]["nama"]
            jadwal["judul"] = self.film[jadwal["idx_film"]]["judul"]

            return jadwal

        def edit_jadwal(self, idx_jadwal, jadwal):
            self.jadwal[idx_jadwal] = jadwal

        def check_kursi_kosong(self, idx_jadwal, kursi):
            return self.jadwal[idx_jadwal]["daftar_kursi"][kursi[0]][kursi[1]] == -1

        def pesan(self, idx_jadwal, idx_customer, daftar_kursi):
            self.customer[idx_customer]["pesanan"].append({
                "idx_jadwal": idx_jadwal,
                "nomor_kursi": daftar_kursi
            })

            for kursi in daftar_kursi:
                self.jadwal[idx_jadwal]["daftar_kursi"][kursi[0]][kursi[1]] = idx_customer
        
        def get_pesanan(self, idx_customer):
            return self.customer[idx_customer]["pesanan"][::-1]

    server.register_instance(BioskopServer())
    server.serve_forever()
