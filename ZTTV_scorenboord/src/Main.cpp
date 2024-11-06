#include <Arduino.h>
#include <memory>

#include "Display.h"
#include "ScoreServer.h"
#include "WiFiHandler.h"

std::unique_ptr<Display> display = nullptr;
std::unique_ptr<ScoreServer> scoreServer = nullptr;

#define PANEL_RES_X 64      // Number of pixels wide of each INDIVIDUAL panel module. 
#define PANEL_RES_Y 32     // Number of pixels tall of each INDIVIDUAL panel module.
#define PANEL_CHAIN 1      // Total number of panels chained one to another

void setup()
{
	Serial.begin(115200);
	display = std::make_unique<Display>(PANEL_RES_X, PANEL_RES_Y, PANEL_CHAIN);
	WifiHandler::get().setDebugDisplay(display.get());
	WifiHandler::get().start();
	scoreServer = std::make_unique<ScoreServer>(display.get());
}


void loop()
{
	if (scoreServer != nullptr)
		scoreServer->update();
}
