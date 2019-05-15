/* Display triangle (written for arduino mega with newhaven display)

   This program is going to draw a triangle on the display.
   You can choose the colour, placing, size and flip (45° * n)

   Written by J. Sarrazyn

   Based on the 
*/

// Setting the pins for the display
#define   SDI_PIN    51    // SDI (serial mode) signal connected to (pin 11 for uno // pin 51 for mega)
#define   SCL_PIN    52    // SCL (serial mdoe) signal connected to (pin 13 for uno // pin 52 for mega)
#define    RS_PIN    4    // RS signal connected to pin 4
#define    CS_PIN   5    // /CS signal connected to pin 5

// Setting the colours for the triangles
#define   ROSE  0xBAE2FF
#define    RED  0x0000FF
#define MAROON  0x0000F0
#define  GREEN  0x00FF00
#define   LILA  0xFF00FF
#define   BLUE  0xFF0000
#define   CYAN  0xFFFF00

// Setting background colours
#define  WHITE  0xFFFFFF
#define  BLACK  0x000000
#define   GRAY  0xF0F0F0

// Setting the coordinates (for a 128x128 display)
// Change these to place the triangle and size him
byte upperCoord = 34;
byte lowerCoord = 94;
byte midPoint = 64;

// Set column address start + end
void OLED_SetColumnAddress(unsigned char x_start, unsigned char x_end)
{
  OLED_Data(0x15, 2);
  OLED_Data(x_start, 1);
  OLED_Data(x_end, 1);
}

// Fill screen with a given color
void OLED_FillScreen(unsigned long color)
{
  unsigned int i, j;
  OLED_SetColumnAddress(0x00, 0x7F);
  OLED_SetRowAddress(0x00, 0x7F);
  OLED_WriteMemoryStart();

  for (i = 0; i < 128; i++)
  {
    for (j = 0; j < 128; j++)
    {
      OLED_Pixel(color);
    }
  }
}

// Write one pixel of a given color
void OLED_Pixel(unsigned long color)
{
  OLED_Data((color >> 16), 1);
  OLED_Data((color >> 8), 1);
  OLED_Data(color, 1);
}

// Send data to OLED
void OLED_Data(unsigned char d, byte c)
{
  unsigned char i;
  unsigned char mask = 0x80;

  digitalWrite(CS_PIN, LOW);

  if ( c == 1)
  {
    digitalWrite(RS_PIN, HIGH);
  }
  else if ( c == 2)
  {
    digitalWrite(RS_PIN, LOW);
  }


  for (i = 0; i < 8; i++)
  {
    digitalWrite(SCL_PIN, LOW);

    if ((d & mask) >> 7 == 1)
    {
      digitalWrite(SDI_PIN, HIGH);
    }
    else
    {
      digitalWrite(SDI_PIN, LOW);
    }
    digitalWrite(SCL_PIN, HIGH);
    d = d << 1;
  }
  digitalWrite(CS_PIN, HIGH);

}

// Write to RAM command
void OLED_WriteMemoryStart(void)
{
  OLED_Data(0x5C, 2);
}

// Set row address start + end
void OLED_SetRowAddress(unsigned char y_start, unsigned char y_end)
{
  OLED_Data(0x75, 2);
  OLED_Data(y_start, 1);
  OLED_Data(y_end, 1);
}

// OLED initialization
void OLED_Init(void)
{
  OLED_Data(0xFD, 2); // Command lock setting
  OLED_Data(0x12, 1);    // unlock
  OLED_Data(0xFD, 2); // Command lock setting
  OLED_Data(0xB1, 1);    // unlock
  OLED_Data(0xAE, 2);
  OLED_Data(0xB3, 2); // clock & frequency
  OLED_Data(0xF1, 1);    // clock=Diviser+1 frequency=fh
  OLED_Data(0xCA, 2); // Duty
  OLED_Data(0x7F, 1);    // OLED _END+1
  OLED_Data(0xA2, 2);   // Display offset
  OLED_Data(0x00, 1);
  OLED_Data(0xA1, 2); // Set display start line
  OLED_Data(0x00, 1);    // 0x00 start line
  OLED_Data(0xA0, 2); // Set Re-map, color depth
  OLED_Data(0xA0, 1);    // 8-bit 262K
  OLED_Data(0xB5, 2); // set GPIO
  OLED_Data(0x00, 1);    // disabled
  OLED_Data(0xAB, 2); // Function Set
  OLED_Data(0x01, 1);    // 8-bit interface, internal VDD regulator
  OLED_Data(0xB4, 2); // set VSL
  OLED_Data(0xA0, 1);    // external VSL
  OLED_Data(0xB5, 1);
  OLED_Data(0x55, 1);
  OLED_Data(0xC1, 2); // Set contrast current for A,B,C
  OLED_Data(0x8A, 1);    // Color A
  OLED_Data(0x70, 1);    // Color B
  OLED_Data(0x8A, 1);    // Color C
  OLED_Data(0xC7, 2); // Set master contrast
  OLED_Data(0x0F, 1);    //
  OLED_Data(0xB9, 2); // use linear grayscale LUT
  OLED_Data(0xB1, 2); // Set pre & dis-charge
  OLED_Data(0x32, 1);    // pre=1h, dis=1h
  OLED_Data(0xBB, 2); // Set precharge voltage of color A,B,C
  OLED_Data(0x07, 1);    //
  OLED_Data(0xB2, 2);       // display enhancement
  OLED_Data(0xa4, 1);
  OLED_Data(0x00, 1);
  OLED_Data(0x00, 1);
  OLED_Data(0xB6, 2); // precharge period
  OLED_Data(0x01, 1);
  OLED_Data(0xBE, 2); // Set VcomH
  OLED_Data(0x07, 1);
  OLED_Data(0xA6, 2); // Normal display
  OLED_Data(0xAF, 2); // Display on
}

void setup()
{
  DDRD = 0xFF;                  // configure PORTD as output

  pinMode(RS_PIN, OUTPUT);          // configure RS_PIN as output
  pinMode(CS_PIN, OUTPUT);      // configure CS_PIN as output

  digitalWrite(CS_PIN, HIGH);   // set CS_PIN

  pinMode(SDI_PIN, OUTPUT);        // configure SDI_PIN as output
  pinMode(SCL_PIN, OUTPUT);         // configure SCL_PIN as output

  PORTD = 0x00;                 // reset SDI_PIN and SCL_PIN, ground DB[5..0] of the display

  OLED_Init();                  // initialize the screen
  OLED_FillScreen(WHITE);       // fill screen by a given color

  // Draw a triangle (red) with these coord and flip 1 (0°)
  MakeTriangle(RED, upperCoord, lowerCoord, 1);
}

// To make a triangle
void MakeTriangle(unsigned long color, byte upperCoor, byte lowerCoor, byte flip)
{
  /*
     1: 0°

     2: 45°

     3: 90°

     4: 135°

     5: 180°

     6: 225°

     7: 270°

     8: 315°

  */

  /* Making a triangle

     First is checks what the flip is.
     Than using the upper and lower coord draws a triangle.
     The midpoint is used as starting place.
     The point of the triangle is the pixel at the midpoint.
     Than it does midpoint -1 and +1 for the next line.
     And so on until you are at the lower coord.
  */
  if (flip == 1) {

    byte lengthHor1 = 0;

    for (int y = lowerCoor; y >= upperCoor; y = y - 1) { //coord of the vertical starting place

      OLED_SetRowAddress( y, y); //vertical

      for (int i = (midPoint - lengthHor1); i <= (midPoint + lengthHor1); i++) { //length of the horizontal line

        OLED_SetColumnAddress( i, i); //horizontal
        OLED_WriteMemoryStart();
        OLED_Pixel(color);
      }
      lengthHor1 += 1;
    }
  }

  else if (flip == 2) {

    int dev;
    int len;

    dev = (lowerCoor - upperCoor) / 2;
    len = lowerCoor - upperCoor;

    for (int i = len; i >= 0; i = i - 1) {

      OLED_SetColumnAddress( (upperCoord + i), (upperCoord + i)); //horizontal

      for (int y = 1; y <= i; y++) {

        OLED_SetRowAddress( (midPoint + dev - y), (midPoint + dev - y)); //vertical
        OLED_WriteMemoryStart();
        OLED_Pixel(color);
      }
    }
  }

  else if (flip == 3) {

    byte lengthHor3 = 0;

    for (int y = lowerCoor; y >= upperCoor; y = y - 1) { //coord of the vertical starting place

      OLED_SetColumnAddress( y, y); //horizontal

      for (int i = (midPoint - lengthHor3); i <= (midPoint + lengthHor3); i++) { //length of the horizontal line

        OLED_SetRowAddress( i, i); //vertical
        OLED_WriteMemoryStart();
        OLED_Pixel(color);
      }
      lengthHor3 += 1;
    }
  }

  else if (flip == 4) {

    int dev;
    int len;

    dev = (lowerCoor - upperCoor) / 2;
    len = lowerCoor - upperCoor;

    for (int i = len; i >= 0; i = i - 1) {

      OLED_SetColumnAddress( (upperCoord + i), (upperCoord + i)); //horizontal

      for (int y = 1; y <= i; y++) {

        OLED_SetRowAddress( (midPoint - dev + y), (midPoint - dev + y)); //vertical
        OLED_WriteMemoryStart();
        OLED_Pixel(color);
      }
    }
  }

  else if (flip == 5) {

    byte lengthHor5 = 0;

    for (int y = upperCoor; y <= lowerCoor; y++) { //coord of the vertical starting place

      OLED_SetRowAddress( y, y); //vertical

      for (int i = (midPoint - lengthHor5); i <= (midPoint + lengthHor5); i++) { //length of the horizontal line

        OLED_SetColumnAddress( i, i); //horizontal
        OLED_WriteMemoryStart();
        OLED_Pixel(color);

      }
      lengthHor5 += 1;
    }
  }

  else if (flip == 6) {

    int dev;
    int len;

    dev = (lowerCoor - upperCoor) / 2;
    len = lowerCoor - upperCoor;

    for (int i = len; i >= 0; i = i - 1) {

      OLED_SetRowAddress( (lowerCoord - i), (lowerCoord - i)); //vertical

      for (int y = i; y >= 0; y = y - 1) {

        OLED_SetColumnAddress( (midPoint - dev + y), (midPoint - dev + y)); //horizontal
        OLED_WriteMemoryStart();
        OLED_Pixel(color);
      }
    }
  }

  else if (flip == 7) {

    byte lengthHor7 = 0;

    for (int y = upperCoor; y <= lowerCoor; y++) { //coord of the vertical starting place

      OLED_SetColumnAddress( y, y); //horizontal

      for (int i = (midPoint - lengthHor7); i <= (midPoint + lengthHor7); i++) { //length of the horizontal line

        OLED_SetRowAddress( i, i); //vertical
        OLED_WriteMemoryStart();
        OLED_Pixel(color);

      }
      lengthHor7 += 1;
    }
  }

  else if (flip == 8) {

    int dev;
    int len;

    dev = (lowerCoor - upperCoor) / 2;
    len = lowerCoor - upperCoor;

    for (int i = len; i >= 0; i = i - 1) {

      OLED_SetRowAddress( (upperCoord + i), (upperCoord + i)); //vertical

      for (int y = i; y >= 0; y = y - 1) {

        OLED_SetColumnAddress( (midPoint - dev + y), (midPoint - dev + y)); //horizontal
        OLED_WriteMemoryStart();
        OLED_Pixel(color);
      }
    }
  }
}

void loop()
{
  // Nothing here because the triangle only needs to be drawn ones
}

