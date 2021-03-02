#ifndef SERVER_H_
#define SERVER_H_

#include <ulfius.h>
#include <jansson.h>

void setPort(int newPort);
int applyHistogram (const struct _u_request * request, struct _u_response * response, void * user_data);
int applyClassification (const struct _u_request * request, struct _u_response * response, void * user_data);
int startServer();

#endif