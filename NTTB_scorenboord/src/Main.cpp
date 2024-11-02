#include <Arduino.h>
#include <memory>

#include "Display.h"
#include "ScoreServer.h"
#include "WiFiHandler.h"


std::unique_ptr<Display> display = nullptr;
std::unique_ptr<ScoreServer> scoreServer = nullptr;


void setup()
{
	Serial.begin(115200);
	display = std::make_unique<Display>(62, 32, 1);
	WifiHandler::get().setDebugDisplay(display.get());
	WifiHandler::get().start();
	scoreServer = std::make_unique<ScoreServer>(display.get());
}


void loop()
{
	if (scoreServer != nullptr)
		scoreServer->update();
}
