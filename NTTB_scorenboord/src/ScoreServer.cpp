#include "ScoreServer.h"
#include "Display.h"

#include <sstream>

ScoreServer::ScoreServer(Display* display):
	webServer(80),
	display(display)
{
	webServer.on("/sbsetting", [this](){sbsetting();});
	webServer.on("/sblogo", [this](){sblogo();});
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
	display->printLine("S: not found");
	webServer.send(200, "text/plain", "test headers");
}


void ScoreServer::sbsetting()
{
	display->printLine("S: sbsetting");
	webServer.send(200, "text/plain", "test headers");
}


void ScoreServer::sblogo()
{
	display->printLine("S: sblogo");
	webServer.send(200, "text/plain", "test headers");
}


void ScoreServer::sbdata()
{
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
