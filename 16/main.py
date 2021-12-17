#!/usr/bin/env python3

from typing import Tuple, List, Union
from functools import reduce, wraps
import dataclasses
import math


def log_reads(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        data, idx0 = args[:2]
        res = fn(*args, **kwargs)
        idx1 = res[1]
        # print(f'{fn.__name__:20} idx: {idx0} -> {idx1}, read: {data[idx0:idx1]}')
        return res
    return inner


@dataclasses.dataclass
class PacketHeader:
    ver: int
    typ: int

    def PacketType(self) -> Union['OperatorPacket', 'DataPacket']:
        if self.typ == 4:
            return DataPacket
        return OperatorPacket


@dataclasses.dataclass
class DataPacket:
    header: PacketHeader
    packets: List[int]

    def packets_val(self) -> int:
        if len(self.packets) == 1:
            return self.packets[0]

        return reduce(lambda acc, e: (acc << 4) + e, self.packets)

    def __repr__(self) -> str:
        return f'DataPacket({self.header}, packet_val: {self.packets_val()})'

    def sum_ver(self) -> int:
        return self.header.ver

    def eval(self) -> int:
        return self.packets_val()


@dataclasses.dataclass
class OperatorPacket:
    header: PacketHeader
    length: int
    packets: List[Union['OperatorPacket', DataPacket]]

    def sum_ver(self) -> int:
        return self.header.ver + sum([p.sum_ver() for p in  self.packets])

    def eval(self) -> int:
        htyp = self.header.typ
        if htyp == 0:
            return sum([p.eval() for p in self.packets])
        elif htyp == 1:
            return math.prod([p.eval() for p in self.packets])
        elif htyp == 2:
            return min([p.eval() for p in self.packets])
        elif htyp == 3:
            return max([p.eval() for p in self.packets])
        elif htyp == 5:
            return 1 if self.packets[0].eval() > self.packets[1].eval() else 0
        elif htyp == 6:
            return 1 if self.packets[0].eval() < self.packets[1].eval() else 0
        elif htyp == 7:
            return 1 if self.packets[0].eval() == self.packets[1].eval() else 0


def get_version(data: str, idx: int) -> Tuple[int, int]:
    ver = int(data[idx:idx+3], 2)
    return ver, idx+3


def get_type(data: str, idx: int) -> Tuple[int, int]:
    typ = int(data[idx:idx+3], 2)
    return typ, idx+3


@log_reads
def get_packet_count(data: str, idx: int) -> Tuple[int, int]:
    v, idx = data[idx:idx+11], idx+11
    return int(v, 2), idx

@log_reads
def get_bit_count(data: str, idx: int) -> Tuple[int, int]:
    v, idx = data[idx:idx+15], idx+15
    return int(v, 2), idx


@log_reads
def read_packet_header(data: str, idx: int) -> Tuple[PacketHeader, int]:
    ver, idx = get_version(data, idx)
    typ, idx = get_type(data, idx)
    return PacketHeader(ver, typ), idx


def read_packet(data: str, idx: int) -> Tuple[int, int, bool]:
    last = int(data[idx], 2) == 0
    v = int(data[idx+1:idx+5], 2)
    return v, idx+5, last


@log_reads
def read_packets_data(data: str, idx: int) -> Tuple[List[int], int]:
    packets = []
    while True:
        v, idx, last = read_packet(data, idx)
        packets.append(v)
        if last:
            return packets, idx


@log_reads
def parse_packet(data: str, idx: int) -> Tuple[Union[DataPacket, OperatorPacket], int]:
    # print(f'idx: {idx}, len: {len(data)}')
    header, idx = read_packet_header(data, idx)
    typ = header.PacketType()
    if typ == DataPacket:
        packets, idx = read_packets_data(data, idx)
        return DataPacket(header, packets), idx
    else:
        return read_operator_packet(data, idx, header)


@log_reads
def get_len(data: str, idx: int) -> Tuple[int, int]:
    return int(data[idx], 2), idx+1


@log_reads
def read_operator_packet(data: str, idx: int, header: PacketHeader) -> Tuple[OperatorPacket, int]:
    ln, idx = get_len(data, idx)
    sub_packets: Union[DataPacket, OperatorPacket] = []

    if ln == 0:
        bit_cnt, idx = get_bit_count(data, idx)
        final_idx = idx + bit_cnt
        while idx != final_idx:
            # print(idx, final_idx)
            p, idx = parse_packet(data, idx)
            sub_packets.append(p)
    else:
        packet_cnt, idx = get_packet_count(data, idx)

        for _ in range(packet_cnt):
            p, idx = parse_packet(data, idx)
            sub_packets.append(p)

    return OperatorPacket(header, ln, sub_packets), idx


def hex_to_bit_arr(data: str) -> str:
    return reduce(lambda x, e: x + e, ['{:04b}'.format(int(c, 16)) for c in data])


if __name__ == '__main__':
    with open('input', 'r') as h:
        data = hex_to_bit_arr(h.readline().strip())

    t1 = 'D2FE28'
    t2 = '38006F45291200'
    t3 = 'EE00D40C823060'
    t4 = '8A004A801A8002F478'
    t5 = '620080001611562C8802118E34'
    t6 = 'C0015000016115A2E0802F182340'
    t7 = 'A0016C880162017C3686B18A3D4780'

    if False:
        for t in [
                t1,
                t2,
                t3,
                t4,
                t5,
                t6,
                t7,
        ]:
            bits = hex_to_bit_arr(t)
            print(t)
            print(f'Bit count: {len(bits)}; {bits}')
            print(parse_packet(bits, 0))

    parsed, _ = parse_packet(data, 0)
    print(f'Part 1 -> ', parsed.sum_ver())
    print(f'Part 2 -> ', parsed.eval())
