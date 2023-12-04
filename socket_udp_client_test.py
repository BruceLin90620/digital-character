#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ("127.0.0.1", 6000)

while True:
	response, addr = s.recvfrom(1024)
	print(response.decode())

s.close()