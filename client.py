#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket, os

def wyslij(gniazdo, plik_sciezka):
    """do wysylania plikow"""
    rozmiar = os.path.getsize(filepath)
    gniazdo.send(str(rozmiar))
    gniazdo.recv(1024)
    gniazdo.send(os.path.split()[1])
    gniazdo.recv(1024)
    with open(plik_sciezka, 'rb') as plik:
        while True:
            plik_bin = plik.read(1024)
            plik_sciezka.send(plik_bin)
            if not plik_bin: break

def odbierz(gniazdo):
    rozmiar = gniazdo.recv(1024)
    gniazdo.send(rozmiar)
    rozmiar = int(rozmiar)
    plik_nazwa = gniazdo.recv(1024)
    gniazdo.send(plik_nazwa)
    with open(plik_nazwa+"odebrany", 'wb+') as plik:
        rozmiar_recv = 0
        while rozmiar_recv < rozmiar:
            part = gniazdo.recv(1024)
            plik.write(part)
            rozmiar_recv += len(part)

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wybor = raw_input("chcesz odbierać [o], czy wysylac [w] plik?: ")
    if wybor == 'o': wybor=True
    while wybor:
        plik = raw_input("Podaj nazwe pliku: ")
        addr = raw_input("Podaj adres ip lub host: ")
        port = int(raw_input("Podaj port: "))
        s.connect((addr, port))
        wyslij(s, plik)
    else:
        odbierz(s)
        
