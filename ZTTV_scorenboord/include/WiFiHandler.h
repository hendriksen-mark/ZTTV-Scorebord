#pragma once

#include <memory>
#include <WiFi.h>

class Display;

class WifiHandler
{
	WifiHandler();
	~WifiHandler();
	WifiHandler(const WifiHandler&) = delete;
	WifiHandler(WifiHandler&&) = delete;

public:
	void start();
	void setDebugDisplay(Display* display);

	static WifiHandler& get();

private:
	static void staticEventHandler(arduino_event_t* event);
	void eventHandler(arduino_event_t* event);
	static const char* eventIdToString(arduino_event_id_t id);

private:
	static std::unique_ptr<WifiHandler> instance;
	Display* debugDisplay;

	friend std::unique_ptr<WifiHandler> std::make_unique<WifiHandler>();
	friend std::default_delete<WifiHandler>;
};