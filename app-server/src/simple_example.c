/**
 * test.c
 * Small Hello World! example
 * to compile with gcc, run the following command
 * gcc -o test test.c -lulfius
 */
#include <stdio.h>
#include <ulfius.h>
#include <jansson.h>

#define PORT 1717

/**
 * Callback function for the web application on /helloworld url call
 */
int callback_hello_world (const struct _u_request * request, struct _u_response * response, void * user_data) {
  ulfius_set_string_body_response(response, 200, "Hello World!");
  return U_CALLBACK_CONTINUE;
}

/**
 * Callback function for the web application on test post url call
 */
int callback_test (const struct _u_request * request, struct _u_response * response, void * user_data) {
  json_t * jsonImage = ulfius_get_json_body_request(request, NULL);

  char* image;

  if (jsonImage != NULL) {
    image = (char*) json_string_value(json_object_get(jsonImage,"id"));
    printf("%s\n", image);
  } else {
    image = (char*) " ";
    printf("Error in the JSON sent!\n");
  }

  ulfius_set_string_body_response(response, 200, "Recibido!");
  return U_CALLBACK_CONTINUE;
}

/**
 * main function
 */
int main(void) {
  struct _u_instance instance;

  // Initialize instance with the port number
  if (ulfius_init_instance(&instance, PORT, NULL, NULL) != U_OK) {
    fprintf(stderr, "Error ulfius_init_instance, abort\n");
    return(1);
  }

  // Endpoint list declaration
  ulfius_add_endpoint_by_val(&instance, "GET", "/ImageServer/helloworld", NULL, 0, &callback_hello_world, NULL);

  ulfius_add_endpoint_by_val(&instance, "POST", "/ImageServer/test", NULL, 0, &callback_test, NULL);

  // Start the framework
  if (ulfius_start_framework(&instance) == U_OK) {
    printf("Start framework on port %d\n", instance.port);

    // Wait for the user to press <enter> on the console to quit the application
    getchar();
  } else {
    fprintf(stderr, "Error starting framework\n");
  }
  printf("End framework\n");

  ulfius_stop_framework(&instance);
  ulfius_clean_instance(&instance);

  return 0;
}