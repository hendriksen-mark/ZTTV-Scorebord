#pragma once

#include <WebServer.h>

class Display;

class ScoreServer
{
public:
	ScoreServer(Display* display);

	void update();

private:
	void handleNotFound();
	void sbsetting();
	void sblogo();
	void sbdata();
	void onUpload();

	int readValue(const std::string& body, const std::string& valueName, std::size_t& offset);
private:	
	WebServer webServer;
	Display* display;

	static constexpr int postBufferSize = 1437;

	char postBuffer[postBufferSize] = {};
};