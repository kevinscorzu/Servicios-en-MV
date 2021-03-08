#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "server.h"

char* root = "/home/skryfall/Projects/Servicios-en-MV/app-server";
char* logPath;

/**
 * Function in charge of reading the desired port in the config.conf file
 */
void readConfigFile() {
    char ch[80], file_name;
    FILE * fp;
    int port;

    char * filepath = malloc(strlen(root) + strlen("/config.conf") + 1);
    filepath[0] = '\0'; 
    strcat(filepath,root);
    strcat(filepath, "/config.conf");

    fp = fopen(filepath, "r");

    if (fp == NULL)
    {
        perror("Error opening the file\n");
        exit(EXIT_FAILURE);
    }

    fgets(ch, 80, fp);

    sscanf(ch, "%*[^0123456789]%d", &port);
    setPort(port);
    free(filepath);

    fgets(ch, 80, fp);
    fgets(ch, 80, fp);
    fgets(ch, 80, fp);

    char * dirL = strtok(ch, " ");
    dirL = strtok(NULL, "\0");

    logPath = malloc(strlen(root) + strlen(dirL) + strlen("/log.txt") + 1);
    logPath[0] = '\0'; 
    strcat(logPath,root);
    strcat(logPath, dirL);
    strcat(logPath, "/log.txt");

    fclose(fp);

    return;
}

/**
 * Main function of the program
 */
int main() {
    readConfigFile();
    setPaths(root, logPath);
    startServer();
    return 0;
}