#include "server.h"

int port = 1717;
char * imagesJsonPath;
char * histogramCommand;
char * classificationCommand;
char * dataJsonPath;
char * logPath;

/**
 * Función encargada de escribir la fecha y hora en ellog
 */
void addDateTimeToLog() {
    time_t rawtime;
    struct tm * timeinfo;
    char todayDateStr [100];

    time (&rawtime);
    timeinfo = localtime (&rawtime);

    strftime(todayDateStr, strlen("YYY-DD-MMM HH:MM") + 2, "%Y-%d-%b %H:%M", timeinfo);
    writeToLog(", DateTime: ");
    writeToLog(todayDateStr);
    writeToLog("\n");
    return;
}

/**
 * Función encargada de escribir un mensaje en el log
 */
void writeToLog(char* message) {
    FILE * f;
    f = fopen(logPath, "a");
    if (f != NULL) {
        fputs(message, f);
        fclose(f);
        return;
    } else {
        printf("Error writing to log\n");
        return;
    }
}

/**
 * Función encargada de asignar el puerto leído en el archivo de configuración
 */
void setPort(int newPort) {
    port = newPort;
    return;
}

/**
 * Función encargada de asignar todos los paths que se utilizan en este proyecto
 */
void setPaths(char* root, char* nLogPath) {
    imagesJsonPath = malloc(strlen(root) + strlen("/images.json") + 1);
    imagesJsonPath[0] = '\0'; 
    strcat(imagesJsonPath, root);
    strcat(imagesJsonPath, "/images.json");

    dataJsonPath = malloc(strlen(root) + strlen("/data.json") + 1);
    dataJsonPath[0] = '\0'; 
    strcat(dataJsonPath, root);
    strcat(dataJsonPath, "/data.json");

    histogramCommand = malloc(strlen("python3 ") + strlen(root) + strlen("/out/handler.py 0") + 1);
    histogramCommand[0] = '\0'; 
    strcat(histogramCommand, "python3 ");
    strcat(histogramCommand, root);
    strcat(histogramCommand, "/out/handler.py 0");

    classificationCommand = malloc(strlen("python3 ") + strlen(root) + strlen("/out/handler.py 1") + 1);
    classificationCommand[0] = '\0'; 
    strcat(classificationCommand, "python3 ");
    strcat(classificationCommand, root);
    strcat(classificationCommand, "/out/handler.py 1");

    logPath = nLogPath;

    return;
}

/**
 * Función encargada de recibir las images a las que se les aplicará un histograma
 */
int applyHistogram (const struct _u_request * request, struct _u_response * response, void * user_data) {
    json_t * jsonImages = ulfius_get_json_body_request(request, NULL);

    if (jsonImages != NULL) {
        json_dump_file(jsonImages, imagesJsonPath, 0);
        system(histogramCommand);
    } else {
        printf("Error in the JSON received\n");
        writeToLog("Status: Error in the JSON received");
        addDateTimeToLog();
    }

    ulfius_set_string_body_response(response, 200, "Ok");
    return U_CALLBACK_CONTINUE;
}

/**
 * Función encargada de recibir las images que se clasificarán por color
 */
int applyClassification (const struct _u_request * request, struct _u_response * response, void * user_data) {
    json_t * jsonImages = ulfius_get_json_body_request(request, NULL);

    if (jsonImages != NULL) {
        json_dump_file(jsonImages, imagesJsonPath, 0);
        system(classificationCommand);
    } else {
        printf("Error in the JSON received\n");
        writeToLog("Status: Error in the JSON received");
        addDateTimeToLog();
    }

    ulfius_set_string_body_response(response, 200, "Ok");
    return U_CALLBACK_CONTINUE;
}

/**
 * Función encargada de reiniciar el contador de las imágenes
 */
int resetCounter (const struct _u_request * request, struct _u_response * response, void * user_data) {
    if (!remove(dataJsonPath)){
        printf("Restarted image counter\n");
        writeToLog("Status: Restarted image counter");
    } else {
        printf("Error, couldn't delete data file\n");
        writeToLog("Status: Error, couldn't delete data file");
    }

    addDateTimeToLog();
    ulfius_set_string_body_response(response, 200, "Ok");
    return U_CALLBACK_CONTINUE;
}

/**
 * Función encargada de iniciar el servidor
 */
int startServer() {
    struct _u_instance instance;

    if (ulfius_init_instance(&instance, port, NULL, NULL) != U_OK) {
        fprintf(stderr, "Error ulfius_init_instance, abort\n");
        return(1);
    }

    ulfius_add_endpoint_by_val(&instance, "POST", "/ImageServer/Histogram", NULL, 0, &applyHistogram, NULL);
    ulfius_add_endpoint_by_val(&instance, "POST", "/ImageServer/ColorClassification", NULL, 0, &applyClassification, NULL);
    ulfius_add_endpoint_by_val(&instance, "GET", "/ImageServer/Reset", NULL, 0, &resetCounter, NULL);

    if (ulfius_start_framework(&instance) == U_OK) {
        printf("Start framework on port: %d\n", instance.port);

        writeToLog("Status: Start framework on port: ");
        char strPort[4];
        sprintf(strPort, "%d", port);
        writeToLog(strPort);
        addDateTimeToLog();
        getchar();
    } else {
        fprintf(stderr, "Error starting framework\n");

        writeToLog("Status: Error starting framework");
        addDateTimeToLog();
    }
    printf("Framework ended\n");
    writeToLog("Status: Framework ended");
    addDateTimeToLog();

    ulfius_stop_framework(&instance);
    ulfius_clean_instance(&instance);

    return 0;
}