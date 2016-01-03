# create SYSEX strings for initialising native mode
SYSEX_KMK_HEADER = (0xF0, 0x42, 0x40, 0x6E, 0)
SYSEX_NATIVE_ON = SYSEX_KMK_HEADER + (0, 0, 0x01, 0xF7)
SYSEX_NATIVE_OFF = SYSEX_KMK_HEADER + (0, 0, 0, 0xF7)

sysTRANSPOSE = 0x00
sysGLOBAL_CH = 0x00
sysPB_CH = 0x00
# bit fields defining which pads transmit MIDI
# if specified, MIDI is sent as well as sysex (which is always sent)
sysPAD7_1_TRANSMIT = int('0000000',2)
sysPAD14_8_TRANSMIT = int('0000000',2)
sysPAD16_15_TRANSMIT = int('00',2)
# define channel and note for pads 1 -> 16
sysPAD_CH = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
sysPAD_NOTE = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 0xF7)


SYSEX_NATIVE_1 = (SYSEX_KMK_HEADER + (0x3f, 0x27, 0x00,
                                     sysTRANSPOSE,
                                     sysGLOBAL_CH,
                                     sysPB_CH,
                                     sysPAD7_1_TRANSMIT,
                                     sysPAD14_8_TRANSMIT,
                                     sysPAD16_15_TRANSMIT) +
                  sysPAD_CH +
                  sysPAD_NOTE )

# bit fields defining pad LED states
sysPAD7_1_LED = int('0000000',2)
sysPAD14_8_LED = int('0000000',2)
# bit fields defining button (enter, exit, scene, message, setting)
# and pads (16-15) LED states
sysBUTTON_PAD16_15_LED = int('0000000',2)
# bit field ( < red, > red, < green, > green, 0, Tempo, HEX) for LEDs
sysBUTTON_TEMPO_LED = int('0000010',2)
# bit fields for LCDs (bits 4/5 = first LCD, bits 0/1 = 2nd LCD)
# 0,1,2,3 = off/red/green/orange)
sysLCD2_1_COL = int('000000',2)
sysLCD4_3_COL = int('000000',2)
sysLCD6_5_COL = int('000000',2)
sysLCD8_7_COL = int('100010',2)
sysLCD0_COL = int('00',2)
# ASCII strings for each LCD
sysLCD0_ASC = (32, 32, 32, 32, 32, 32, 32, 32, 0xF7)

SYSEX_NATIVE_2 = (SYSEX_KMK_HEADER + (0x3F, 0x12, 0x01,
                                      sysPAD7_1_LED,
                                      sysPAD14_8_LED,
                                      sysBUTTON_PAD16_15_LED,
                                      sysBUTTON_TEMPO_LED,
                                      sysLCD2_1_COL,
                                      sysLCD4_3_COL,
                                      sysLCD6_5_COL,
                                      sysLCD8_7_COL,
                                      sysLCD0_COL) +
                  sysLCD0_ASC)

# ASCII strings for each LCD
sysLCD1_ASC = (32, 32, 32, 32, 32, 32, 32, 32)
sysLCD2_ASC = (32, 32, 32, 32, 32, 32, 32, 32)
sysLCD3_ASC = (32, 32, 32, 32, 32, 32, 32, 32)
sysLCD4_ASC = (32, 32, 32, 32, 32, 32, 32, 32, 0xF7)

SYSEX_NATIVE_3 = (SYSEX_KMK_HEADER + (0x3F, 0x21, 0x02) +
                                      sysLCD1_ASC +
                                      sysLCD2_ASC +
                                      sysLCD3_ASC +
                                      sysLCD4_ASC)

# ASCII strings for each LCD
sysLCD5_ASC = (32, 32, 32, 32, 32, 32, 32, 32)
sysLCD6_ASC = (32, 32, 32, 32, 32, 32, 32, 32)
sysLCD7_ASC = (32, 32, 32, 32, 32, 75, 77, 75)
sysLCD8_ASC = (32, 32, 98, 121, 32, 87, 65, 67, 0xF7)

SYSEX_NATIVE_4 = (SYSEX_KMK_HEADER + (0x3F, 0x21, 0x03) +
                                      sysLCD5_ASC +
                                      sysLCD6_ASC +
                                      sysLCD7_ASC +
                                      sysLCD8_ASC)
                                      
                                     
CHANNEL = 0
# These are MIDI notes
KMK_PAD = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F)
KMK_BUTTON = (16, 17, 18, 19, 21, 20, 100)
# These are MIDI CCs
KMK_FADER = (10, 11, 12, 13, 14, 15, 16, 17)
# The 9th encoder (in the array) is the main/tempo encoder on the KMK
KMK_ENCODER = (0, 1, 2, 3, 4, 5, 6, 7, 8)

KMK_LED_COMMAND = 0x01
KMK_LCD_COMMAND = 0x22
KMK_ENC_COMMAND = 0x43
KMK_SLIDER_COMMAND = 0x44
KMK_PAD_COMMAND = 0x45
KMK_PEDAL_COMMAND = 0x47
KMK_BUTTON_COMMAND = 0x48
KMK_JOYSTICK_COMMAND = 0x4B
