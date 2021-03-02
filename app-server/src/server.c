#include <stdio.h>
#include "server.h"

int port = 1717;

/**
 * Function to assign the port read in the file
 */
void setPort(int newPort) {
    port = newPort;
    return;
}

/**
 * Post function in charge of receiving the images to apply the histogram to them
 */
int applyHistogram (const struct _u_request * request, struct _u_response * response, void * user_data) {
    json_t * jsonImages = ulfius_get_json_body_request(request, NULL);

    if (jsonImages != NULL) {
        json_dump_file(jsonImages, "images.json", 0);
        system("python3 out/handler.py 0");
    } else {
        printf("Error in the JSON sent!\n");
    }

    ulfius_set_string_body_response(response, 200, "Ok");
    return U_CALLBACK_CONTINUE;
}

/**
 * Post function in charge of receiving the images to apply the color classification to them
 */
int applyClassification (const struct _u_request * request, struct _u_response * response, void * user_data) {
    json_t * jsonImages = ulfius_get_json_body_request(request, NULL);

    if (jsonImages != NULL) {
        json_dump_file(jsonImages, "images.json", 0);
        system("python3 out/handler.py 1");
    } else {
        printf("Error in the JSON sent!\n");
    }

    ulfius_set_string_body_response(response, 200, "Ok");
    return U_CALLBACK_CONTINUE;
}

/**
 * Function to start the server
 */
int startServer() {
    struct _u_instance instance;

    if (ulfius_init_instance(&instance, port, NULL, NULL) != U_OK) {
        fprintf(stderr, "Error ulfius_init_instance, abort\n");
        return(1);
    }

    ulfius_add_endpoint_by_val(&instance, "POST", "/ImageServer/Histogram", NULL, 0, &applyHistogram, NULL);
    ulfius_add_endpoint_by_val(&instance, "POST", "/ImageServer/ColorClassification", NULL, 0, &applyClassification, NULL);

    if (ulfius_start_framework(&instance) == U_OK) {
        printf("Start framework on port %d\n", instance.port);

        getchar();
    } else {
        fprintf(stderr, "Error starting framework\n");
    }
    printf("End framework\n");

    ulfius_stop_framework(&instance);
    ulfius_clean_instance(&instance);

    return 0;
}