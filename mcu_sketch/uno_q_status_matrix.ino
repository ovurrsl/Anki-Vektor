/*
 * ============================================================================
 * Arduino UNO Q (ABX00173) - Dual-Brain STM32U585 MCU Status Matrix Sketch
 * ============================================================================
 * 
 * Runs on the STMicroelectronics STM32U585 (Cortex-M33) microcontroller.
 * Drives the on-board 8x13 (104 pixels) blue monochrome LED matrix.
 * Listens for RPC status events from the Qualcomm QRB2210 Linux MPU via Arduino Bridge.
 * 
 * Status Codes:
 *   0 = BOOTING / INITIALIZING
 *   1 = STANDBY / PC_OFF (Moon Icon)
 *   2 = ACTIVE / PC_ON (Workstation Monitor Icon)
 *   3 = LISTENING (Microphone Icon)
 *   4 = SPEAKING (Soundwave Icon)
 *   5 = VECTOR_CONNECTED ("V" Robot Icon)
 *   9 = ERROR ("X" Warning Icon)
 */

#include "Arduino_LED_Matrix.h"
#include <ArduinoBridge.h>

ArduinoLEDMatrix matrix;

// 8x13 Matrix Frames (each frame is represented by 3 uint32_t words)

// 1. STANDBY / PC_OFF (Sleep / Moon)
const uint32_t frame_pc_off[3] = {
  0x00000000,
  0x03800440,
  0x04400380
};

// 2. ACTIVE / PC_ON (Monitor Screen)
const uint32_t frame_pc_on[3] = {
  0x0ff80808,
  0x09880888,
  0x0ff80180
};

// 3. LISTENING (Microphone)
const uint32_t frame_listening[3] = {
  0x03800440,
  0x04400380,
  0x01000380
};

// 4. SPEAKING (Soundwave)
const uint32_t frame_speaking[3] = {
  0x04100a20,
  0x11400a20,
  0x04100000
};

// 5. VECTOR_CONNECTED ("V" Letter / Robot Eyes)
const uint32_t frame_vector_ok[3] = {
  0x0c600c60,
  0x0c6006c0,
  0x03800100
};

// 9. ERROR ("X" Cross)
const uint32_t frame_error[3] = {
  0x08200440,
  0x02800100,
  0x02800440
};

// Current status code
volatile int current_status = 0;

// Bridge RPC Handler called from Python on Linux MPU
int onSetStatus(int statusCode) {
  current_status = statusCode;
  switch (statusCode) {
    case 1:
      matrix.loadFrame(frame_pc_off);
      break;
    case 2:
      matrix.loadFrame(frame_pc_on);
      break;
    case 3:
      matrix.loadFrame(frame_listening);
      break;
    case 4:
      matrix.loadFrame(frame_speaking);
      break;
    case 5:
      matrix.loadFrame(frame_vector_ok);
      break;
    case 9:
    default:
      matrix.loadFrame(frame_error);
      break;
  }
  return 1; // Success
}

void setup() {
  // CRITICAL: Arduino UNO Q boot logo shows on matrix for ~20-30s during Linux boot.
  // Wait gracefully before taking control of the matrix.
  delay(1000);
  matrix.begin();

  // Initialize Arduino Bridge to communicate with Qualcomm QRB2210 MPU
  Bridge.begin();
  Bridge.bind("set_status", onSetStatus);

  // Show Standby initial frame
  matrix.loadFrame(frame_pc_off);
}

void loop() {
  // Poll Bridge events from Linux
  Bridge.poll();
  delay(10);
}
