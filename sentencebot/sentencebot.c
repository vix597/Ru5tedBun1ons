#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include <ctype.h>

#include "net.h"
#include "sentence.h"
#include "crypt.h"

// 200 is plenty of room
#define SEN_LEN 200

const char FLAG[] = {
    0x02, 0x09, 0x5b, 0x06, 0x1f, 0x0b,
    0x51, 0x56, 0x0d, 0x3a, 0x2e, 0x7a,
    0x1e, 0x51, 0x48, 0x19, 0x1f, 0x1e,
    0x1f, 0x40, 0x1c
};

int SEED = 0;

bool found = false;
bool search = false;
bool user_seed = false;

char * getFlag() {
    char * mac = getMac();
    if (!mac) {
        return NULL;
    } else {
        // Should be de:ad:be:ef:fa:ce
        if (strcmp(mac, "de:ad:be:ef:fa:ce") == 0 && user_seed) {
            printf("You win!\n");
        }

        printf("Mac Address: %s\n", mac);

        char * flag = xorencrypt((char*)&FLAG, sizeof(FLAG), mac, strlen(mac));
        free(mac);
        return flag;
    }
}

char* generateSentence() {
    char* sentence = calloc((SEN_LEN+1), sizeof(char));

    //Build Sentence
    strcat(sentence, ARTICLES[rand()%ARTICLES_SIZE]);

    strcat(sentence, " ");
    strcat(sentence, NOUNS[rand()%NOUNS_SIZE]);

    strcat(sentence, " ");
    strcat(sentence, VERBS[rand()%VERBS_SIZE]);

    if (strcmp(sentence, "the flag is") == 0 && (search == true || user_seed == true)) {
        strcat(sentence, " ");
        char * flag = getFlag();
        if (!flag) {
            strcat(sentence, "not the flag");
        } else {
            strcat(sentence, flag);
            free(flag);
        }
        found = true;
    } else {
        strcat(sentence, " ");
        strcat(sentence, PREPOSITIONS[rand()%PREPOSITIONS_SIZE]);

        strcat(sentence, " ");
        strcat(sentence, PROPER_NOUNS[rand()%PROPER_NOUNS_SIZE]);
    }

    //Capitalize first letter
    sentence[0] = toupper(sentence[0]);

    return sentence;
}

int main(int argc, char* argv[]) {
    // Default to system time for random seed
    SEED = time(NULL);

    // Parse args
    if (argc >= 2) {
        if (strcmp(argv[1], "--set-seed") == 0 && argc >= 3) {
            user_seed = true;
            SEED = atoi(argv[2]);
        } else if (strcmp(argv[1], "--debug") == 0) {
            printf("Searching...\n");
            search = true;
            SEED = 0;
        }
    }

    while (!found) {
        srand(SEED);

        char* sentence = generateSentence();
        if (found) {
            if (user_seed) {
                printf("%s.\n", sentence);
            }
            free(sentence);
            break;
        } else if (!search) {
            printf("%s.\n", sentence);
            free(sentence);
            break;
        } else {
            SEED += 1;
        }
    }

    if (search) {
        printf("Seed: %d\n", SEED);
    }

    return 0;
}
