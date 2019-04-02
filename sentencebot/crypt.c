#include "crypt.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

char * xorencrypt(char * message, int message_len, char * key, int key_len) {
    char * encrypted = calloc(message_len + 1, sizeof(char));

    for(int i = 0; i < message_len; i++) {
        encrypted[i] = message[i] ^ key[i % key_len];
    }

    return encrypted;
}