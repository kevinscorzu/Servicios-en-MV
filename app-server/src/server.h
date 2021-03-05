#ifndef SERVER_H_
#define SERVER_H_

#include <ulfius.h>
#include <jansson.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

void addDateTimeToLog();
void writeToLog(char* message);
void setPort(int newPort);
void setPaths(char* root, char* nLogPath);
int applyHistogram (const struct _u_request * request, struct _u_response * response, void * user_data);
int applyClassification (const struct _u_request * request, struct _u_response * response, void * user_data);
int resetCounter (const struct _u_request * request, struct _u_response * response, void * user_data);
int startServer();

#endif