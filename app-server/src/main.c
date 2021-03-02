#include <stdio.h>
#include <stdlib.h>
#include "server.h"

/**
 * Function in charge of reading the desired port in the config.conf file
 */
void readFile() {
    char ch[80], file_name;
    FILE * fp;
    int port;

    fp = fopen("./config.conf", "r");

    if (fp == NULL)
    {
        perror("Error opening the file\n");
        exit(EXIT_FAILURE);
    }

    fgets(ch, 80, fp);

    fclose(fp);

    sscanf(ch, "%*[^0123456789]%d", &port);
    setPort(port);
    return;
}

/**
 * Main function of the program
 */
int main() {
    readFile();
    startServer();

    return 0;
}