#include "Display.h"
#include "ScoreboardPins.h"
#include "qrencode.h"
#include "ZTTV_64X32.h"

using namespace Pins;

Display::Display(unsigned int resX, unsigned int resY, unsigned int numPanels):
	pins{Display_R1, Display_G1, Display_B1, Display_R2, Display_G2, Display_B2, Display_A, Display_B, Display_C, Display_D, Display_E, Display_LAT, Display_OE, Display_CLK},
	currentConsoleLine(-1),
	consoleTextBuffer{}
{
	HUB75_I2S_CFG mxconfig(
		resX,			// module width
		resY,			// module height
		numPanels,			// Chain length
		pins,					// pin mapping
		HUB75_I2S_CFG::ICN2038S // driver chip
	);
	panel = std::make_unique<MatrixPanel_I2S_DMA>(mxconfig);
	panel->begin();
	panel->setBrightness8(30); // 0-255
	panel->clearScreen();

	colors = {
		panel->color565(0, 0, 0),
		panel->color565(255, 255, 255),
		panel->color565(255, 0, 0),
		panel->color565(0, 255, 0),
		panel->color565(0, 0, 255)
	};

	this->screenwidth = resX;
    this->screenheight = resY;
    int min = screenwidth;
    if (screenheight<screenwidth)
        min = screenheight;
    multiply = min/WD;
    offsetsX = (screenwidth-(WD*multiply))/2;
    offsetsY = (screenheight-(WD*multiply))/2;
}


uint16_t Display::colorWheel(uint8_t pos)
{
	if (pos < 85)
	{
		return panel->color565(pos * 3, 255 - pos * 3, 0);
	}
	else if (pos < 170)
	{
		pos -= 85;
		return panel->color565(255 - pos * 3, 0, pos * 3);
	}
	else
	{
		pos -= 170;
		return panel->color565(0, pos * 3, 255 - pos * 3);
	}
}


void Display::clear()
{
	panel->fillScreen(colors.black);
}


void Display::printLine(const char* text)
{
	// Scroll text if printing beyond the bottom of the display.
	if (currentConsoleLine + 1 >= consoleBufferLines)
	{
		for (int i = 0; i < consoleBufferLines - 1; ++i)
			memcpy(&consoleTextBuffer[i], &consoleTextBuffer[i + 1], consoleBufferWidth);
	}
	if (currentConsoleLine + 1 < consoleBufferLines)
		currentConsoleLine++;

	std::size_t textLength = strlen(text);
	if (textLength >= consoleBufferWidth)
	{
		memcpy(consoleTextBuffer[currentConsoleLine], text, consoleBufferWidth - 1);
		consoleTextBuffer[currentConsoleLine][consoleBufferWidth - 1] = '\0';
	}
	else
	{
		memcpy(consoleTextBuffer[currentConsoleLine], text, textLength);
		consoleTextBuffer[currentConsoleLine][textLength] = '\0';
	}

	redrawConsole();
}


void Display::printWrapped(const char* text)
{
	char line[consoleBufferWidth] = {};
	std::size_t textLength = strlen(text);
	if (textLength == 0)
		return;
	unsigned int lineWidth = consoleBufferWidth - 1;
	unsigned int numLines = (textLength - 1) / lineWidth + 1;

	for (int i = 0; i < numLines; ++i)
	{
		unsigned int offset = i * lineWidth;\
		unsigned int end = min(offset + lineWidth, textLength);
		unsigned int length = end - offset;
		if (length == 0)
			break;
		memcpy(line, &text[offset], length);
		line[length] = '\0';

		printLine(line);
		if (i >= consoleBufferLines)
			delay(500);
	}
}

void Display::screenwhite()
{
    panel->fillScreen(colors.white);
}

void Display::screenupdate()
{
}

void Display::redrawConsole()
{
	clear();
	panel->setTextSize(1);
	panel->setTextWrap(false);
	panel->setTextColor(colors.red);
	panel->setCursor(0, 0);
	for (unsigned int i = 0; i < consoleBufferLines; ++i)
	{
		panel->println(consoleTextBuffer[i]);
	}	
}

void Display::print(String msg, uint16_t color)
{
	clear();
	panel->setTextSize(1);
	panel->setTextWrap(true);
	panel->setTextColor(color);
	panel->setCursor(0, 0);
	panel->print(msg);
}

void Display::drawXbm565(int x, int y, int width, int height, const char *xbm, uint16_t color) 
{
  if (width % 8 != 0) {
      width =  ((width / 8) + 1) * 8;
  }
    for (int i = 0; i < width * height / 8; i++ ) {
      unsigned char charColumn = pgm_read_byte(xbm + i);
      for (int j = 0; j < 8; j++) {
        int targetX = (i * 8 + j) % width + x;
        int targetY = (8 * i / (width)) + y;
        if (bitRead(charColumn, j)) {
          panel->drawPixel(targetX, targetY, color);
        }
      }
    }
}

void Display::logo()
{
	clear();
	drawXbm565(0,0,64,32, ZTTV_64X32_bits, (uint16_t)panel->color565(22,102,255));
}

void Display::drawPixel(int x, int y, int color) {
    if(color==1) {
        color = colors.black;
    } else {
        color = colors.white;
    }
    //panel->drawPixel(x, y, color);
	panel->fillRect(x,y,multiply,multiply,color);
}
