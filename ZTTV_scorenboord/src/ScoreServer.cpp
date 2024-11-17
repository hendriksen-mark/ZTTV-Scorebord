#include "ScoreServer.h"
#include "Display.h"
#include <DebugLog.h>

#include <sstream>
/*
num args: 8, on url: /sbsetting
args: brightness = 255
args: speed = 35
args: clubid = 0
args: reset = 0
args: monochrome = 0
args: mirrored = 1
args: uuid = ef5b052670964771
args: msgid = 0

num args: 3, on url: /sblogo
args: logo = 1
args: uuid = ef5b052670964771
args: msgid = 1

num args: 7, on url: /sbdata
args: players[0][name] = thuis speler
args: players[1][name] = uit speler
args: players[2][name] = thuis partner
args: players[3][name] = uit partner
args: revert = 0
args: uuid = ef5b052670964771
args: msgid = 2

num args: 18, on url: /sbdata
args: game[started] = 0
args: game[score1] = 0
args: game[score2] = 0
args: game[setscore1] = 0
args: game[setscore2] = 0
args: game[serve] = 1
args: game[dbl] = 0
args: game[rotate] = 0
args: game[intimer] = 3
args: game[timerclock] = 120
args: game[timeout1] = 0
args: game[timeout2] = 0
args: game[penalty1] = 0
args: game[penalty2] = 0
args: game[timerule] = 0
args: revert = 0
args: uuid = ef5b052670964771
args: msgid = 4

num args: 5 ,on url: /sbbanner
args: size = 3
args: text = Welkom
args: color = 7
args: uuid = ef5b052670964771
args: msgid = 2
*/

ScoreServer::ScoreServer(Display* display):
	webServer(80),
	display(display)
{
	webServer.on("/sbsetting", [this](){sbsetting();});
	webServer.on("/sblogo", [this](){sblogo();});
	webServer.on("/sbbanner", [this](){sbbanner();});
	webServer.on("/sbdata", HTTPMethod::HTTP_POST, [this](){sbdata();}, [this](){onUpload();});
	webServer.onNotFound([this](){handleNotFound();});
	webServer.begin();
}


void ScoreServer::update()
{
	webServer.handleClient();
}


void ScoreServer::handleNotFound()
{
	LOG_DEBUG("method:", (webServer.method() == HTTP_GET) ? "GET" : "POST", ", num args:", webServer.args(), ",on url:", webServer.uri());
	for (int i = 0; i < webServer.args(); i++) {
		LOG_DEBUG("args:", webServer.argName(i).c_str(), "=" , webServer.arg(i).c_str());
	}
	display->printLine("S: not found");
	webServer.send(200, "text/plain", "test headers");
}


void ScoreServer::sbsetting()
{
	LOG_DEBUG("method:", (webServer.method() == HTTP_GET) ? "GET" : "POST", ", num args:", webServer.args(), ",on url:", webServer.uri());
	for (int i = 0; i < webServer.args(); i++) {
		LOG_DEBUG("args:", webServer.argName(i).c_str(), "=" , webServer.arg(i).c_str());
	}
	display->printLine("S: sbsetting");
	webServer.send(200, "text/plain", "test headers");
}

void ScoreServer::sbbanner()
{
	LOG_DEBUG("method:", (webServer.method() == HTTP_GET) ? "GET" : "POST", ", num args:", webServer.args(), ",on url:", webServer.uri());
	for (int i = 0; i < webServer.args(); i++) {
		LOG_DEBUG("args:", webServer.argName(i).c_str(), "=" , webServer.arg(i).c_str());
	}
	display->printLine("S: sbbanner");
	webServer.send(200, "text/plain", "test headers");
}


void ScoreServer::sblogo()
{
	LOG_DEBUG("method:", (webServer.method() == HTTP_GET) ? "GET" : "POST", ", num args:", webServer.args(), ",on url:", webServer.uri());
	for (int i = 0; i < webServer.args(); i++) {
		LOG_DEBUG("args:", webServer.argName(i).c_str(), "=" , webServer.arg(i).c_str());
	}
	display->logo();
	webServer.send(200, "text/plain", "test headers");
}


void ScoreServer::sbdata()
{
	LOG_DEBUG("method:", (webServer.method() == HTTP_GET) ? "GET" : "POST", ", num args:", webServer.args(), ",on url:", webServer.uri());
	for (int i = 0; i < webServer.args(); i++) {
		LOG_DEBUG("args:", webServer.argName(i).c_str(), "=" , webServer.arg(i).c_str());
	}
	for (int i = 0; i < webServer.args(); i++) 
	{
		if (int pos = webServer.arg(i).indexOf("stand"); pos >= 0)
		{
			display->printWrapped(webServer.arg(i).substring(pos).c_str());
		}

	}
	for (int i = 0; i < webServer.headers(); i++) 
	{
		if (int pos = webServer.header(i).indexOf("stand"); pos >= 0)
		{
			display->printWrapped(webServer.header(i).substring(pos).c_str());
		}		
	}

	webServer.send(200, "text/plain", "test headers");
}


void ScoreServer::onUpload()
{
	auto client = webServer.client();
	if (client.connected())
	{
		int available = webServer.client().available();

		if (available > 0)
		{
			int readMax = min(available, postBufferSize - 1);
			int readCount = client.readBytes(postBuffer, readMax);
			if (readCount > 0)
			{
				postBuffer[readCount] = '\0';
				std::string body(postBuffer, readCount);
				std::size_t offset = 0;
				int score1 = readValue(body, "score1%5D=", offset);
				int score2 = readValue(body, "score2%5D=", offset);
				display->printLine(score1, " - ", score2);
				//delay(5000);
				//display->printWrapped(postBuffer);
			}
		}
	}

}


int ScoreServer::readValue(const std::string& body, const std::string& valueName, std::size_t& offset)
{
	if (auto pos = body.find(valueName, offset); pos != body.npos)
	{
		char* end = nullptr;
		const char* start = &body[pos + valueName.length()];
		int value = strtol(start, &end, 10);
		if (end != nullptr)
		{
			int readCount = end - start;
			offset = pos + valueName.length() + readCount;
		}
		return value;
	}	
	return 0;
}
