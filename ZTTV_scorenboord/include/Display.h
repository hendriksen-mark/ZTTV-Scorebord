
#pragma once

#include <ESP32-HUB75-MatrixPanel-I2S-DMA.h>
#include <memory>
#include <sstream>
#include "qrcodedisplay.h"

class Display : public QRcodeDisplay
{
public:
	Display(unsigned int resX, unsigned int resY, unsigned int numPanels);

	// Input a value 0 to 255 to get a color value.
	// The colours are a transition r - g - b - back to r.
	// From: https://gist.github.com/davidegironi/3144efdc6d67e5df55438cc3cba613c8	
	uint16_t colorWheel(uint8_t pos);
	
	void clear();
	void printLine(const char* text);
	void print(String msg, uint16_t color);
	void logo();
	void drawXbm565(int x, int y, int width, int height, const char *xbm, uint16_t color);

	template<typename ...LogParameterT>
	void printLine(LogParameterT&& ...parameters)
	{
		std::ostringstream stream;
		(stream << ... << parameters);
		printLine(stream.str().c_str());
	}

	void printWrapped(const char* text);
	void drawPixel(int x, int y, int color);
	void screenwhite();
	void screenupdate();

	struct Colors
	{
		uint16_t black;
		uint16_t white;
		uint16_t red;
		uint16_t green;
		uint16_t blue;
	} colors;

private:
	void redrawConsole();

private:
	HUB75_I2S_CFG::i2s_pins pins;
	std::unique_ptr<MatrixPanel_I2S_DMA> panel;

	static constexpr unsigned int consoleBufferLines = 4;
	static constexpr unsigned int consoleBufferWidth = 11;

	unsigned int currentConsoleLine;
	char consoleTextBuffer[consoleBufferLines][consoleBufferWidth];
};