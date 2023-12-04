#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 6000))
print("UDP bound on port 6000...")
addr = ("127.0.0.1", 6000)
while True:


	s.sendto(b"Hello %s!\n", addr)