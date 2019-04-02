#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>

#include "net.h"

const char * dir_search = "/sys/class/net";
const char * file = "address";

char * getMac() {
    char * foundDir = NULL;
    struct dirent *pDirent = NULL;

    DIR * pDir = opendir(dir_search);
    if (pDir == NULL) {
        printf ("Cannot open directory '%s'\n", dir_search);
        return NULL;
    }

    while ((pDirent = readdir(pDir)) != NULL) {
        if (strcmp(pDirent->d_name, ".") == 0) {
            continue;
        } else if (strcmp(pDirent->d_name, "..") == 0) {
            continue;
        } else {
            foundDir = strdup(pDirent->d_name);
            break;
        }
    }
    closedir(pDir);

    if (foundDir) {
        FILE * pFile;
        int size = strlen(dir_search) + strlen(foundDir) + strlen(file) + 3;
        char * fullPath = calloc(size, sizeof(char));
        snprintf(fullPath, size, "%s/%s/%s", dir_search, foundDir, file);
        free(foundDir);

        pFile = fopen(fullPath, "r");
        if (pFile == NULL) {
            printf("Cannot open file '%s'\n", fullPath);
            free(fullPath);
            return NULL;
        }

        // Just allocate a bunch. I'm tired of doing exact crap.
        char * mac = calloc(80, sizeof(char));
        fscanf(pFile, "%s", mac);
        fclose(pFile);
        free(fullPath);
        return mac;
    } else {
        printf("Could not find any network devices in '%s'\n", dir_search);
    }

    return NULL;
}
