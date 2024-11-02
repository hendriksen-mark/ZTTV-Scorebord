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

		//std::stringstream argStream;
		//argStream << webServer.argName(i) << " = ";
		//display->printLine(argStream.str().c_str());
		//display->printLine(webServer.arg(i).c_str());
		//Serial.printf("args: %s = %s\n", webServer.argName(i).c_str(), webServer.arg(i).c_str());
	}
	for (int i = 0; i < webServer.headers(); i++) 
	{
		if (int pos = webServer.header(i).indexOf("stand"); pos >= 0)
		{
			display->printWrapped(webServer.header(i).substring(pos).c_str());
		}		
	}
	display->printLine("sb: ", webServer.clientContentLength());
	//delay(500);
	//int contentLength = webServer.clientContentLength();
	//if (contentLength > 0)
	//{
	//	char buffer[1024] = {};
	//	while (contentLength > 0)
	//	{
	//		unsigned int readSize = min(1023, contentLength);
	//		webServer.client().read((uint8_t*)buffer, readSize);
	//		buffer[readSize] = '\0';
	//		contentLength -= readSize;
	//		display->printWrapped(buffer);
	//	}
	//}
	webServer.send(200, "text/plain", "test headers");
}


void ScoreServer::onUpload()
{
	//const auto& upload = webServer.upload();
	//if (&upload == nullptr)
	//{
	//	display->printLine("upl == null");
	//	delay(500);
	//	if (&webServer.raw() == nullptr)
	//		display->printLine("raw == null");
	auto client = webServer.client();
	if (client.connected())
	{
		//display->printLine("cl conn.");
		//delay(500);
		int available = webServer.client().available();
		//display->printLine("av: ", available);
		if (available > 0)
		{
			int readMax = min(available, 1436);
			int readCount = client.readBytes(postBuffer, readMax);
			if (readCount > 0)
			{
				postBuffer[readCount] = '\0';
				std::string body(postBuffer, readCount);
				std::size_t offset = 0;
				int score1 = readValue(body, "score1%5D=", offset);
				offset = 0;
				int score2 = readValue(body, "score2%5D=", offset);
				display->printLine(score1, " - ", score2);
				//delay(5000);
				//display->printWrapped(postBuffer);
			}
		}
	}
	//	delay(500);
	//	return;
	//}

	//delay(2000);
	//switch (upload.status)
	//{
	//	case HTTPUploadStatus::UPLOAD_FILE_START:	display->printLine("File Start"); break;
	//	case HTTPUploadStatus::UPLOAD_FILE_END:		display->printLine("File End"); break;
	//	case HTTPUploadStatus::UPLOAD_FILE_WRITE:	display->printLine("File Write"); break;
	//	case HTTPUploadStatus::UPLOAD_FILE_ABORTED:	display->printLine("File Abort"); break;
	//}
	//unsigned int uploadSize = upload.currentSize;
	//display->printLine("s: ", uploadSize);
	//delay(2000);
	//memcpy(postBuffer, upload.buf, uploadSize);
	//display->printLine("mcpy Done");
	//delay(2000);
	//postBuffer[uploadSize] = '\0';
	//display->printLine("Print Wrap");
	//display->printWrapped(postBuffer);
}


int ScoreServer::readValue(const std::string& body, const std::string& valueName, std::size_t& offset)
{
	if (auto pos = body.find(valueName, offset); pos != body.npos)
	{
		char* end = nullptr;
		int value = strtol(&body[pos + valueName.length()], &end, 10);
		if (end != nullptr)
		{
			int readCount = end - &body[offset];
			offset = offset + valueName.length() + readCount;
		}
		return value;
	}	
	return 0;
}
